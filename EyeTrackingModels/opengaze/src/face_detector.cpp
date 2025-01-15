#include <iostream>
#include <tbb/tbb.h>

// if we use OpenFace
#if USE_OPENFACE
#include <LandmarkCoreIncludes.h> // from "OpenFace-master/lib/local/LandmarkDetector/include/"
#endif

#include "face_detector.hpp"

using namespace std;
using namespace cv;

vector<LandmarkDetector::FaceModelParameters> det_parameters_;
vector<LandmarkDetector::CLNF> clnf_models_;

namespace opengaze {

FaceDetector::FaceDetector() {
    method_type_ = Method::OpenFace;
}

FaceDetector::~FaceDetector() {}

void FaceDetector::initialize(int number_users=5) {
    string root_path = OPENFACE_DIR;
    root_path = root_path + "/build/bin";
    //string openface_root = OpenFace_ROOT_DIR;
    // (currently) hard-coded setting
    num_faces_max_ = number_users;
    detection_resize_rate_ = 2.0; // resize the input image to detect face, crucial for speed
    detection_skip_frames_ = 1;
    nonoverlap_threshold_ = 0.5;
    certainty_threshold_ = 0.0; // the smaller the better, 1 is the best, -1 is the worst
    landmark_indices_[0] = 36; landmark_indices_[1] = 39; landmark_indices_[2] = 42;
    landmark_indices_[3] = 45; landmark_indices_[4] = 48; landmark_indices_[5] = 54;
    tracking_loss_limit_ = 10;
    // initialize the tracking models
    LandmarkDetector::FaceModelParameters det_parameter;
    det_parameter.reinit_video_every = -1; // This is so that the model would not try re-initialising itself
    det_parameter.curr_face_detector = LandmarkDetector::FaceModelParameters::MTCNN_DETECTOR;

    det_parameter.model_location = root_path + "/model/main_clm_wild.txt";
    det_parameter.haar_face_detector_location = root_path + "/classifiers/haarcascade_frontalface_alt.xml";// this line will be disable due to "curr_face_detector"
    det_parameter.mtcnn_face_detector_location = root_path + "/model/mtcnn_detector/MTCNN_detector.txt";

    det_parameter.use_face_template = true;
    det_parameter.reinit_video_every = 5;
    // det_parameter.quiet_mode = true; not avaliable fro OpenFace v2.1
    // // For in the wild fitting these parameters are suitable
    det_parameter.window_sizes_init = vector<int>(4);
    det_parameter.window_sizes_init[0] = 15;
    det_parameter.window_sizes_init[1] = 13;
    det_parameter.window_sizes_init[2] = 11;
    det_parameter.window_sizes_init[3] = 9;
    det_parameter.sigma = 1.25;
    det_parameter.reg_factor = 35;
    det_parameter.weight_factor = 2.5;
    det_parameter.num_optimisation_iteration = 10;
    det_parameter.curr_face_detector = LandmarkDetector::FaceModelParameters::HOG_SVM_DETECTOR;
    det_parameters_.push_back(det_parameter);

    LandmarkDetector::CLNF clnf_model_ = LandmarkDetector::CLNF(det_parameter.model_location);
    if (!clnf_model_.loaded_successfully){
        cout << "ERROR: Could not load the landmark detector" << endl;
        exit(-1);
    }
    clnf_model_.face_detector_HAAR.load(det_parameter.haar_face_detector_location);
    clnf_model_.haar_face_detector_location = det_parameter.haar_face_detector_location;
    clnf_model_.face_detector_MTCNN.Read(det_parameter.mtcnn_face_detector_location);
    clnf_model_.mtcnn_face_detector_location = det_parameter.mtcnn_face_detector_location;

    // If can't find MTCNN face detector, default to HOG one
    if (det_parameter.curr_face_detector == LandmarkDetector::FaceModelParameters::MTCNN_DETECTOR && clnf_model_.face_detector_MTCNN.empty()){
        cout << "INFO: defaulting to HOG-SVM face detector" << endl;
        det_parameter.curr_face_detector = LandmarkDetector::FaceModelParameters::HOG_SVM_DETECTOR;
    }

    clnf_models_.reserve(num_faces_max_);
    clnf_models_.push_back(clnf_model_);
    active_models_.push_back(false);

    for(int i=1; i<num_faces_max_; ++i)
    {
        clnf_models_.push_back(clnf_model_);
        active_models_.push_back(false);
        det_parameters_.push_back(det_parameter);
    }

    // variables
    frame_counter_ = 0;
    current_face_id_ = 1;
    for(int i=0; i<num_faces_max_; ++i) face_ids_.push_back(0);

}

void FaceDetector::reset() {
    // reset all status
    frame_counter_ = 0;
    current_face_id_ = 1;

    for(unsigned int model = 0; model < clnf_models_.size(); ++model)
    {
        active_models_[model] = false;
        face_ids_[model] = 0;
        clnf_models_[model].Reset();
    }
}

void NonOverlapingDetections(const vector<LandmarkDetector::CLNF>& clnf_models, vector<cv::Rect_<float> >& face_detections){
    // Go over the model and eliminate detections that are not informative (there already is a tracker there)
    for (size_t model = 0; model < clnf_models.size(); ++model){

        // See if the detections intersect
        cv::Rect_<float> model_rect = clnf_models[model].GetBoundingBox();

        for (int detection=face_detections.size()-1; detection >= 0; --detection)
        {
            double intersection_area = (model_rect & face_detections[detection]).area();
            double union_area = model_rect.area() + face_detections[detection].area() - 2 * intersection_area;

            // If the model is already tracking what we're detecting ignore the detection, this is determined by amount of overlap
            if (intersection_area / union_area > 0.5)
            {
                face_detections.erase(face_detections.begin() + detection);
            }
        }
    }
}

double NonOverlapingDetection(const LandmarkDetector::CLNF &ref_model, const LandmarkDetector::CLNF &tgt_model)
{
    Rect_<double> ref_rect = ref_model.GetBoundingBox();
    Rect_<double> tgt_rect = tgt_model.GetBoundingBox();

    double intersection_area = (ref_rect & tgt_rect).area();
    double union_area = ref_rect.area() + tgt_rect.area() - 2 * intersection_area;

    return intersection_area/union_area;
}

void FaceDetector::track_faces(cv::Mat input_img, std::vector<opengaze::Sample> &output) {
    if(input_img.channels() < 3){
        cout << "The input must be a color image!" <<endl;
        exit(EXIT_FAILURE);
    }
    Mat_<uchar> grayscale_image;
    cvtColor(input_img, grayscale_image, CV_BGR2GRAY);

    bool all_models_active = true;
    for(unsigned int model = 0; model < clnf_models_.size(); ++model)
    {
        if(!active_models_[model])
        {
            all_models_active = false;
            break;
        }
    }

    // Detect faces
    // Get the detections (every Xth frame and when there are free models available for tracking)
    std::vector<Rect_<float> > face_detections;
    cv::Mat small_grayscale_image_;
    if (frame_counter_ % detection_skip_frames_ == 0 && !all_models_active) {
        // resized image for faster face detection
        if (detection_resize_rate_ != 1) resize(grayscale_image, small_grayscale_image_,
               Size(), 1.0/detection_resize_rate_, 1.0/detection_resize_rate_);
        else small_grayscale_image_ = grayscale_image;

        if (det_parameters_[0].curr_face_detector == LandmarkDetector::FaceModelParameters::HOG_SVM_DETECTOR){
            vector<float> confidences;
            LandmarkDetector::DetectFacesHOG(face_detections, small_grayscale_image_, clnf_models_[0].face_detector_HOG, confidences);
        }
        else if (det_parameters_[0].curr_face_detector == LandmarkDetector::FaceModelParameters::HAAR_DETECTOR){
            LandmarkDetector::DetectFaces(face_detections, small_grayscale_image_, clnf_models_[0].face_detector_HAAR);
        }
        else{
            vector<float> confidences;
            LandmarkDetector::DetectFacesMTCNN(face_detections, small_grayscale_image_, clnf_models_[0].face_detector_MTCNN, confidences);
        }

        // resize the face deteciton back
        if (detection_resize_rate_ != 1) {
            for(auto& face_detection : face_detections) {
                face_detection.x *= detection_resize_rate_;
                face_detection.y *= detection_resize_rate_;
                face_detection.width *= detection_resize_rate_;
                face_detection.height *= detection_resize_rate_;
            }
        }

        // Keep only non overlapping detections (also convert to a concurrent vector
        NonOverlapingDetections(clnf_models_, face_detections);
    }

    vector< tbb::atomic<bool> > face_detections_used(face_detections.size());
    // Go through every model and update the tracking
    tbb::parallel_for(0, (int)clnf_models_.size(), [&](int model) {
    //for (unsigned int model = 0; model < clnf_models_.size(); ++model) {
        bool detection_success = false;
        // If the current model has failed more than threshold, remove it
        if (clnf_models_[model].failures_in_a_row > tracking_loss_limit_) {
            active_models_[model] = false;
            clnf_models_[model].Reset();
        }
        // If the model is inactive reactivate it with new detections
        if (!active_models_[model]){
            for (size_t detection_ind = 0; detection_ind < face_detections.size(); ++detection_ind)
            {
                // if it was not taken by another tracker take it (if it is false swap it to true and enter detection, this makes it parallel safe)
                if (!face_detections_used[detection_ind].compare_and_swap(true, false)) {
                    // Reinitialise the model
                    clnf_models_[model].Reset();
                    // This ensures that a wider window is used for the initial landmark localisation
                    clnf_models_[model].detection_success = false;
                    LandmarkDetector::DetectLandmarksInVideo(input_img, face_detections[detection_ind], clnf_models_[model], det_parameters_[model], grayscale_image);
                    // This activates the model
                    active_models_[model] = true;
                    face_ids_[model] = current_face_id_;
                    current_face_id_++;
                    // break out of the loop as the tracker has been reinitialised
                    break;
                }

            }
        }
        else
        {
            // The actual facial landmark detection / tracking
            detection_success = LandmarkDetector::DetectLandmarksInVideo(input_img, clnf_models_[model], det_parameters_[model], grayscale_image);
        }
    //}
    });

    // Go through every model and check the results
    for(size_t model=0; model<clnf_models_.size(); ++model){
        // Check if the alignment result is overlapping previous models
        bool overlapping = false;
        for(size_t model_ref=0; model_ref<model; ++model_ref){
            double overlap_ratio = NonOverlapingDetection(clnf_models_[model_ref], clnf_models_[model]);
            if(overlap_ratio > nonoverlap_threshold_) overlapping = true;
        }
        if(overlapping){
            active_models_[model] = false;
            face_ids_[model] = 0;
            clnf_models_[model].Reset();
            continue;
        }

        if(clnf_models_[model].detection_certainty < certainty_threshold_) continue;

        Sample temp;
        temp.face_data.certainty = clnf_models_[model].detection_certainty;
        temp.face_data.face_id = face_ids_[model];
        temp.face_data.face_bb.x = (int)clnf_models_[model].GetBoundingBox().x;
        temp.face_data.face_bb.y = (int)clnf_models_[model].GetBoundingBox().y;
        temp.face_data.face_bb.height = (int)clnf_models_[model].GetBoundingBox().height;
        temp.face_data.face_bb.width = (int)clnf_models_[model].GetBoundingBox().width;
        for(int p=0; p<6; p++){
            int num_p = landmark_indices_[p];
            temp.face_data.landmarks[p] = Point2d(
                    clnf_models_[model].detected_landmarks.at<float>(num_p,0),
                    clnf_models_[model].detected_landmarks.at<float>(num_p+68,0)
            );
        }
        output.emplace_back(temp);
    }
}



}

