#include "opengaze.hpp"

#include <iostream>
#include <time.h>

using namespace std;
using namespace cv;

namespace opengaze {

double clockToMilliseconds(clock_t ticks){
    // units/(units/time) => time (seconds) * 1000 = milliseconds
    return (ticks/(double)CLOCKS_PER_SEC)*1000.0;
}

OpenGaze::OpenGaze(int argc, char** argv){
    namespace fs = boost::filesystem;
    namespace po = boost::program_options;

    // default value of parameters
    camera_id_ = 0;
    input_type_ = InputHandler::InputType::Camera;
    is_face_model_ = true;
    string gaze_method;
    string gpu_id;
    string temp;
    int number_user;
    fs::path calib_camera, calib_screen, cnn_param_path, cnn_model_path;

    // parse command line options for input/output paths
    po::options_description command_line("Command line options");
    command_line.add_options()
            ("root_dir,r", po::value<string>(), "configuration file")
            ("input_type,t", po::value<string>(), "input type (camera, video file, directory)")
            ("gaze_method,g", po::value<string>(), "gaze estimation method, could be MPIIGaze or OpenFace")
            ("input,i", po::value<string>(), "parameter for input")
            ("output,o", po::value<string>(), "output directory")
            ("calib_camera", po::value<string>(), "camera calibration file")
            ("calib_screen", po::value<string>(), "camera-screen calibration file")
            ("gpu_id,p", po::value<string>(), "gpu id number, default is 0")
            ("debug,d", "show debug output")
            ("face_model,f", "to use face model or not")
            ("save_video,s", "save output visualization or not")
            ("number_user,n", "the maximum number of users in the input image")
            ;

    cout << "Parsing command line options..." << endl;
    po::variables_map vm_command;
    po::store(po::parse_command_line(argc, argv, command_line), vm_command);
    po::notify(vm_command);

    // parse config file for data paths
    po::options_description config_file("Config file options");
    config_file.add_options()
            ("root_dir,r", po::value<string>(), "configuration file")
            ("input_type, t", po::value<string>(), "input type (camera, video file, directory)")
            ("input, i", po::value<string>(), "parameter for input")
            ("output,o", po::value<string>(), "output directory")
            ("cnn_param_path", po::value<string>(), "Caffe prototxt path")
            ("cnn_model_path", po::value<string>(), "Caffe model path")
            ("calib_camera", po::value<string>(), "camera calibration file")
            ("calib_screen", po::value<string>(), "camera-screen calibration file")
            ("gaze_method", po::value<string>(), "gaze estimation method, could be cnn or openface")
            ("gpu_id,p", po::value<string>(), "gpu id number, default is 0")
            ("face_model", po::value<bool>(), "face model or not")
            ("save_video", po::value<bool>(), "save output visualization or not")
            ("number_user", po::value<string>(), "the maximum number of users in the input image")
            ;

    fs::path root_dir, config_path;

    if(vm_command.count("root_dir")) root_dir = vm_command["root_dir"].as<string>();
    else {
        root_dir = OPENGAZE_CON_DIR;
        cout << "No root directory is found, default value " << root_dir << " will be use" << endl;
    }

    config_path = root_dir / "default.cfg";
    cout << "Reading config from \"" << config_path.string() << "\""<< endl;
    if(!fs::exists(config_path)){
        cout << "Config file does not exist" << endl;
        exit(EXIT_FAILURE);
    }
    ifstream settings_file(config_path.string());
    po::variables_map vm_config;
    po::store(po::parse_config_file(settings_file , config_file), vm_config);
    po::notify(vm_config);

    if(vm_command.count("gpu_id")) gpu_id = vm_command["gpu_id"].as<string>();
    else if (vm_config.count("gpu_id")) gpu_id = vm_config["gpu_id"].as<string>();
    else gpu_id = "0";

    // CNN paramters
    if(vm_command.count("cnn_param_path")) cnn_param_path = vm_command["cnn_param_path"].as<string>();
    else if (vm_config.count("cnn_param_path")) cnn_param_path = vm_config["cnn_param_path"].as<string>();
    else cnn_param_path = root_dir / "content/caffeModel/alexnet_face.prototxt";

    if(vm_command.count("cnn_model_path")) cnn_model_path = vm_command["cnn_model_path"].as<string>();
    else if (vm_config.count("cnn_model_path")) cnn_model_path = vm_config["cnn_model_path"].as<string>();
    else cnn_model_path = root_dir / "content/caffeModel/alexnet_face.caffemodel";

    // check input requirements
    if(vm_command.count("gaze_method")) gaze_method = vm_command["gaze_method"].as<string>();
    else if (vm_config.count("gaze_method")) gaze_method = vm_config["gaze_method"].as<string>();
    else gaze_method = "MPIIGaze";

    if(vm_command.count("calib_screen")) calib_screen = vm_command["calib_screen"].as<string>();
    else if (vm_config.count("calib_screen")) calib_screen = vm_config["calib_screen"].as<string>();
    else calib_screen = root_dir / "content/calib/monitor_laptop.yml";

    if(vm_command.count("calib_camera")) calib_camera = vm_command["calib_camera"].as<string>();
    else if (vm_config.count("calib_camera")) calib_camera = vm_config["calib_camera"].as<string>();
    else calib_camera = root_dir / "content/calib/calibration.yml";

    // read calibration file
    if(!fs::exists(calib_camera)){
        cout << "Camera calibration file does not exist: " << calib_camera <<endl;
        exit(EXIT_FAILURE);
    }
    else input_handler_.readCameraConfiguration(calib_camera.string());

    if(!fs::exists(calib_screen)){
        cout << "Camera-screen calibration file does not exist: " << calib_screen << endl;
        exit(EXIT_FAILURE);
    }
    else input_handler_.readScreenConfiguration(calib_screen.string());

    if(vm_command.count("input_type")) temp = vm_command["input_type"].as<string>();
    else if (vm_config.count("input_type")) temp = vm_config["input_type"].as<string>();
    else temp = "";
    if (temp == "camera") {input_type_ = InputHandler::InputType::Camera;}
    else if (temp == "video") {input_type_ = InputHandler::InputType::Video;}
    else if (temp == "directory") {input_type_ = InputHandler::InputType::Directory;}
    else cout<<"No input type specified, default value (camera) will be use" << endl;

    if (vm_command.count("input")) temp = vm_command["input"].as<string>();
    else if (vm_config.count("input")) temp = vm_config["input"].as<string>();
    else temp = "0";

    if (input_type_ == InputHandler::InputType::Camera) camera_id_ = stoi(temp);
    else if (input_type_ == InputHandler::InputType::Video || input_type_ == InputHandler::InputType::Directory)  input_dir_ = temp;
    else cout<<"No input parameter specified, default value will be use" << endl;

    if(vm_command.count("face_model")) is_face_model_ = true;
    else if(vm_config.count("face_model")) is_face_model_ = vm_config["face_model"].as<bool>();
    else is_face_model_ = true;

    if(vm_command.count("save_video")) is_save_video_ = true;
    else if(vm_config.count("save_video")) is_save_video_ = vm_config["save_video"].as<bool>();
    else is_save_video_ = false;

    if(vm_command.count("debug")) show_debug_ = true;
    else if(vm_config.count("debug")) show_debug_ = vm_config["debug"].as<bool>();
    else show_debug_ = false;

    if(vm_command.count("output")) output_dir_ = vm_command["output"].as<string>();
    else if(vm_config.count("output")) output_dir_ = vm_config["output"].as<string>();
    else {
        if (input_type_ == InputHandler::InputType::Video) output_dir_ = input_dir_.parent_path();
        else if (input_type_ == InputHandler::InputType::Directory) output_dir_ = input_dir_.parent_path();
        else if (input_type_ == InputHandler::InputType::Camera)
            output_dir_ = root_dir;
    }

    string face_detector_root_path;
    if(vm_command.count("openface_path")) face_detector_root_path = vm_command["openface_path"].as<string>();
    else if(vm_config.count("openface_path")) face_detector_root_path = vm_config["openface_path"].as<string>();
    else cout<< "No face detector root specified, default detector will be use" << endl;

    if(vm_command.count("per_model_save_path")) per_model_save_path_ = vm_command["per_model_save_path"].as<string>();
    else if (vm_config.count("per_model_save_path")) per_model_save_path_ = vm_config["per_model_save_path"].as<string>();
    else per_model_save_path_ = root_dir.string() + "/content/calib/user0.txt";

    if(vm_command.count("number_user")) temp = vm_command["number_user"].as<string>();
    else if (vm_config.count("number_user")) temp = vm_config["number_user"].as<string>();
    else temp = "5";
    number_user = stoi(temp);

    // initial class instance
    if (input_type_ == InputHandler::InputType::Camera){ // Camera as input
        input_handler_.setInputType(InputHandler::InputType::Camera);// set input type
        input_handler_.setInput(camera_id_); // set Camera id
    }
    else if (input_type_ == InputHandler::InputType::Video) {
        input_handler_.setInputType(InputHandler::InputType::Video);// set input type
        input_handler_.setInput(input_dir_.string()); // set camera file
    }
    else if (input_type_ == InputHandler::InputType::Directory){
        input_handler_.setInputType(InputHandler::InputType::Directory);
    }
    // initialize other classes
    gaze_estimator_.setCameraParameters(input_handler_.camera_matrix_, input_handler_.camera_distortion_);
    gaze_estimator_.setRootPath(root_dir.string());
    gaze_estimator_.initialFaceDetector(number_user);

    vector<std::string> arguments;
    if (gaze_method == "MPIIGaze") {
        arguments.push_back(cnn_param_path.string());
        arguments.push_back(cnn_model_path.string());
        if (is_face_model_)
            arguments.emplace_back("face");
        else
            arguments.emplace_back("eye");
        arguments.push_back(gpu_id);
        gaze_estimator_.setMethod(GazeEstimator::Method::MPIIGaze, arguments);
    }
    else if (gaze_method == "OpenFace"){
        //gaze_estimator_.setMethod(GazeEstimator::Method::OpenFace, arguments);
        cout << "OpenFace gaze estimation is current not support" << endl;
        exit(EXIT_FAILURE);
    }
    else {
        cout << "The method setting is not right! Options are MPIIGaze or OpenFace!" << endl;
        exit(EXIT_FAILURE);
    }
}

OpenGaze::~OpenGaze() {
    input_handler_.closeInput();
}

// do gaze estimation with camera as input
void OpenGaze::runGazeVisualization() {
    input_handler_.initialize();

    namedWindow("Gaze");
    int key;
    Mat input_image;
    vector<Sample> output;

    cv::VideoWriter m_writer;
    if (is_save_video_){
            boost::filesystem::path save_video_file;
        save_video_file = output_dir_ / (input_dir_.stem().string() + "_gaze_video.avi");
        m_writer.open(save_video_file.string(), CV_FOURCC('M','J','P','G'), 25,
                      Size(input_handler_.getFrameWidth(),input_handler_.getFrameHeight()), true);
        cout << "Saving video to " << save_video_file << endl;
    }

    // construct saving file
    ofstream output_stream;
    boost::filesystem::path output_file_name = output_dir_ / (input_dir_.stem().string() + "_gaze_output.txt");
    output_stream.open(output_file_name.string());
    cout << "Created output file: " << output_file_name.string() << endl;

    // for fps calculation
    double fps_tracker = -1.0;
    double t_start = 0;
    double t_end = 0;

    unsigned int frame_count = 0;

    while(true){// loop all the sample or read frame from Video
        frame_count++;
        t_start = t_end;
        output.clear();

        input_image = input_handler_.getNextSample();// get input image
        if(input_handler_.isReachEnd()){ // check if all sample are processed
            cout<<"Processed all the samples."<<endl;
            break;
        }
        
        Mat undist_img;
        undistort(input_image, undist_img, input_handler_.camera_matrix_, input_handler_.camera_distortion_);
        gaze_estimator_.estimateGaze(undist_img, output); // do gaze estimation
        input_handler_.projectToDisplay(output, gaze_estimator_.input_type_==GazeEstimator::InputType::face);

        // get the fps values
        t_end = cv::getTickCount();
        fps_tracker = 1.0 / (double(t_end - t_start) / cv::getTickFrequency());


        // save output
        for(auto & sample : output) {
            output_stream << frame_count << ",";
            output_stream << sample.face_data.face_id << ",";
            output_stream << sample.face_data.certainty << ",";
            output_stream << sample.face_patch_data.face_center.at<float>(0) << ",";
            output_stream << sample.face_patch_data.face_center.at<float>(1) << ",";
            output_stream << sample.face_patch_data.face_center.at<float>(2) << ",";
            output_stream << sample.gaze_data.gaze2d.x << ",";
            output_stream << sample.gaze_data.gaze2d.y << ",";
            output_stream << sample.eye_data.leye_pos.at<float>(0) << ",";
            output_stream << sample.eye_data.leye_pos.at<float>(1) << ",";
            output_stream << sample.eye_data.leye_pos.at<float>(2) << ",";
            output_stream << sample.eye_data.reye_pos.at<float>(0) << ",";
            output_stream << sample.eye_data.reye_pos.at<float>(1) << ",";
            output_stream << sample.eye_data.reye_pos.at<float>(2) << endl;
        }

        if (is_save_video_ || show_debug_) {
            //////// visualization //////////////////////////////////////////////////
            // draw results
            for(const auto & sample : output){
                //drawLandmarks(sample, undist_img); // draw face landmarks
                drawGazeOnFace(sample, undist_img); // draw gaze ray on face image
                //drawGazeOnSimScreen(sample, undist_img); // draw screen target
            }
            
            if (show_debug_) {
                // show fps
                char fpsC[255];
                std::sprintf(fpsC, "%02f", fps_tracker);
                string fpsSt("FPS: ");
                fpsSt += fpsC;
                cv::putText(undist_img, fpsSt, cv::Point(100, 100), CV_FONT_HERSHEY_SIMPLEX, 1, CV_RGB(255, 0, 0), 2);
                // show the image
                imshow("Gaze", undist_img);
                key = cv::waitKey(1);
                if (key==27) exit(EXIT_SUCCESS); // press ESC to exit
            }

            if (is_save_video_) {
                if (is_save_video_)
                    m_writer << undist_img;
            }
        }

    }
    if (is_save_video_)
        m_writer.release();
}

void OpenGaze::runDataExtraction() {
    assert(input_handler_.getInputType() == InputHandler::InputType::Directory);// Here we just accept the directory folder
    input_handler_.initialize();

    vector<Sample> output;
    Mat input_image;

    while(true){// loop all the sample or read frame from Video
        output.clear();

        input_image = input_handler_.getNextSample();// get input image
        if(input_handler_.isReachEnd()){ // check if all sample are processed
            cout << "Processed all the samples." << endl;
            break;
        }
        
        Mat undist_img;
        undistort(input_image, undist_img, input_handler_.camera_matrix_, input_handler_.camera_distortion_);
        gaze_estimator_.getImagePatch(undist_img, output); // extract the face image

        // save the output
        for (int i=0; i<output.size(); ++i) {
            string save_file_name  = output_dir_.stem().string() + "/img_" + input_handler_.getFileName() + "_" +to_string(i)+".jpg";
            cv::imwrite(save_file_name, output[i].face_patch_data.face_patch);
        }
    }
}

void OpenGaze::runGazeOnScreen() {
    input_handler_.initialize();

    int key;
    Mat input_image, undist_img, show_img;
    vector<Sample> output;

    cv::namedWindow("screen", CV_WINDOW_NORMAL);
    cv::setWindowProperty("screen", CV_WND_PROP_FULLSCREEN, CV_WINDOW_FULLSCREEN);

    show_img = cv::Mat::zeros(input_handler_.getScreenHeight(), input_handler_.getScreenWidth(), CV_8UC3);

    while(true){// loop all the sample or read frame from Video
        output.clear();

        if(input_handler_.isReachEnd()){ // check if all sample are processed
            cout<<"Processed all the samples."<<endl;
            break;
        }
        input_image = input_handler_.getNextSample();// get input image
        undistort(input_image, undist_img, input_handler_.camera_matrix_, input_handler_.camera_distortion_);
        gaze_estimator_.estimateGaze(undist_img, output); // do gaze estimation
        input_handler_.projectToDisplay(output, gaze_estimator_.input_type_==GazeEstimator::InputType::face);

        // save output
        for(auto & sample : output) {
            int loc_x = (int)(sample.gaze_data.gaze2d.x * input_handler_.getScreenWidth());
            int loc_y = (int)(sample.gaze_data.gaze2d.y * input_handler_.getScreenHeight());
            circle(show_img, cv::Point(loc_x, loc_y), 10, CV_RGB(255,255,255), -1);
        }

        imshow("screen", show_img);
        cv::Mat save_img;
        cv::resize(show_img, save_img, cv::Size(1280, 720));
        key = cv::waitKey(1);
        show_img = cv::Mat::zeros(input_handler_.getScreenHeight(), input_handler_.getScreenWidth(), CV_8UC3);
        if (key==27) break; // press ESC to exit
    }
    cv::setWindowProperty("screen", CV_WND_PROP_FULLSCREEN, CV_WINDOW_NORMAL);
    cv::destroyWindow("screen");
}

void OpenGaze::runPersonalCalibration(int num_calibration_point) {
    if (input_handler_.getInputType() != InputHandler::InputType::Camera){ // personal calibration has to be done with camera
        cout << "Error: the input type must be camera for personal calibration!" << endl;
        exit(EXIT_FAILURE);
    }

    Mat input_image, undist_img;
    input_handler_.initialize();

    PersonalCalibrator m_calibrator(input_handler_.getScreenWidth(), input_handler_.getScreenHeight());
    m_calibrator.generatePoints(num_calibration_point);
    m_calibrator.initialWindow(); // show start windows

    vector<cv::Point2f> pred, gt; // prediction and ground-truth
    for (int i=0; i<num_calibration_point; ++i){
        if (m_calibrator.showNextPoint()) {// wait for clicking
            vector<Sample> output;
            input_image = input_handler_.getNextSample(); // get the sample when user clicking
            undistort(input_image, undist_img, input_handler_.camera_matrix_, input_handler_.camera_distortion_);
            gaze_estimator_.estimateGaze(undist_img, output); // do gaze estimation
            input_handler_.projectToDisplay(output, gaze_estimator_.input_type_==GazeEstimator::InputType::face);// convert to 2D projection
            m_calibrator.confirmClicking(); // give feedback to user that they successfully did calibration
            pred.emplace_back(output[0].gaze_data.gaze2d);
            gt.emplace_back(cv::Point2f((m_calibrator.getCurrentPoint().x/(float)input_handler_.getScreenWidth()),
                                      (m_calibrator.getCurrentPoint().y/(float)input_handler_.getScreenHeight())));
        }
        else
            break; // if user press ESC button, we break

    }
    if (pred.size() > 0){
        m_calibrator.generateModel(pred, gt, 1); // get the mapping model
        string per_model_save_path_ = output_dir_.stem().string() + "/personal_gaze_model.yml";
        m_calibrator.saveModel(per_model_save_path_);
    }
}

void OpenGaze::drawGazeOnSimScreen(opengaze::Sample sample, cv::Mat &image) {
    static const int dW = 640;
    static const int dH = 360;
    Mat debug_disp = Mat::zeros(Size(dW, dH), CV_8UC3);

    Point2f g_s;
    g_s.x = dW*sample.gaze_data.gaze2d.x;
    g_s.y = dH*sample.gaze_data.gaze2d.y;

    circle(debug_disp, g_s, 10, CV_RGB(255,0,0), -1);

    debug_disp.copyTo(image(Rect(0, 0, dW, dH)));
}

void OpenGaze::drawGazeOnFace(opengaze::Sample sample, cv::Mat &image) {
    // draw gaze on the face
    if (gaze_estimator_.method_type_ == GazeEstimator::Method::MPIIGaze
        && gaze_estimator_.input_type_ == GazeEstimator::InputType::face) {
        static const float gaze_length = 300.0;
        Mat zero = Mat::zeros(1, 3, CV_32F);
        Mat rvec, tvec;
        sample.face_patch_data.head_r.convertTo(rvec, CV_32F);
        sample.face_patch_data.head_t.convertTo(tvec, CV_32F);

        vector<Point3f> cam_points;
        Vec3f face_center(sample.face_patch_data.face_center.at<float>(0), sample.face_patch_data.face_center.at<float>(1), sample.face_patch_data.face_center.at<float>(2));
        cam_points.emplace_back(face_center);
        cam_points.emplace_back(face_center + gaze_length * sample.gaze_data.gaze3d);

        vector<Point2f> img_points;
        projectPoints(cam_points, zero, zero, input_handler_.camera_matrix_, input_handler_.camera_distortion_, img_points);

        line(image, img_points[0], img_points[1], CV_RGB(255,0,0), 5); // gaze ray
        circle(image, img_points[0], 5, CV_RGB(255,0,0), -1); // staring point
        circle(image, img_points[1], 5, CV_RGB(255,0,0), -1); // end point
    }
    else if ((gaze_estimator_.method_type_ == GazeEstimator::Method::MPIIGaze
              && gaze_estimator_.input_type_ == GazeEstimator::InputType::eye)
             || gaze_estimator_.method_type_ == GazeEstimator::Method::OpenFace) {
        int gaze_length = 300;
        Mat zero = Mat::zeros(1, 3, CV_32F);
        vector<Point3f> cam_points;
        sample.eye_data.leye_pos.convertTo(sample.eye_data.leye_pos, CV_32F);
        Vec3f leye_pose(sample.eye_data.leye_pos.at<float>(0),sample.eye_data.leye_pos.at<float>(1),sample.eye_data.leye_pos.at<float>(2));
        cam_points.emplace_back(leye_pose);
        cam_points.emplace_back(leye_pose + gaze_length*sample.gaze_data.lgaze3d);
        Vec3f reye_pose(sample.eye_data.reye_pos.at<float>(0),sample.eye_data.reye_pos.at<float>(1),sample.eye_data.reye_pos.at<float>(2));
        cam_points.emplace_back(reye_pose);
        cam_points.emplace_back(reye_pose + gaze_length*sample.gaze_data.rgaze3d);

        vector<Point2f> img_points;
        projectPoints(cam_points, zero, zero, input_handler_.camera_matrix_, input_handler_.camera_distortion_, img_points);

        line(image, img_points[0], img_points[1], CV_RGB(255,0,0), 5);
        line(image, img_points[2], img_points[3], CV_RGB(255,0,0), 5);
        circle(image, img_points[1], 3, CV_RGB(255,0,0), -1);
        circle(image, img_points[3], 3, CV_RGB(255,0,0), -1);
    }
}

void OpenGaze::drawLandmarks(opengaze::Sample sample, cv::Mat &image) {
    cv::Rect_<int> face_bb = sample.face_data.face_bb;
    rectangle(image, cv::Point(face_bb.x, face_bb.y),
              cv::Point(face_bb.x+face_bb.width,face_bb.y+face_bb.height), CV_RGB(0,255,0), 5);
    for(int p=0; p<6; ++p)
        circle(image, sample.face_data.landmarks[p], 5, CV_RGB(0,255,0), -1);
}



}