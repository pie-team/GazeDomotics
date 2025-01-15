#include "gaze_predictor.hpp"

#include <string>

// caffe
#define USE_OPENCV 1;
#include <caffe/caffe.hpp>
#include <caffe/util/io.hpp>
#include <caffe/blob.hpp>
#include <caffe/layers/pose_data_layer.hpp>
#include <caffe/layers/memory_data_layer.hpp>


using namespace cv;
using namespace std;
using namespace caffe;

namespace opengaze {
caffe::Net<float> *p_net_;

GazePredictor::GazePredictor() {

}
GazePredictor::~GazePredictor() {
    delete p_net_;
}

void GazePredictor::initiaMPIIGaze(const std::vector<std::string> arguments={}) {
    p_net_ = nullptr;
    string param_path = arguments[0];
    string model_path = arguments[1];
    int gpu_id = stoi(arguments[3]);

    // Set GPU (or CPU)
    /*caffe::Caffe::set_mode(caffe::Caffe::CPU);
    cout << "Using CPU model" << endl;*/
    caffe::Caffe::set_mode(caffe::Caffe::GPU);
    cout << "Using GPU with id " << gpu_id << endl;
    Caffe::SetDevice(gpu_id);

    cout << "load caffe model parameters from " << param_path << endl;
    // create CNN
    p_net_ = new Net<float>(param_path, caffe::TEST);

    cout << "load caffe model from " << model_path << endl;
    // load pre-trained weights (binary proto)
    p_net_->CopyTrainedLayersFrom(model_path);

    // judge model type base on the paramater file name
    size_t i = param_path.rfind("/", param_path.length());
    string filename;
    if (i != string::npos)
        filename = param_path.substr(i+1, param_path.length() - i);
    if (!filename.compare(string("lenet_test.prototxt")))
        model_type_ = 1;
    else if (!filename.compare(string("googlenet.prototxt")))
        model_type_ = 2;
    else if (!filename.compare(string("alexnet_eye.prototxt")))
        model_type_ = 3;
    else if (!filename.compare(string("alexnet_face.prototxt")))
        model_type_ = 4; // the single face model
    else if (!filename.compare(string("alexnet_face_448.prototxt")))
        model_type_ = 4; // the single face model
    else{
        model_type_ = 0;
        cout<<"Cannot define the type of model!"<<endl;
        exit(EXIT_FAILURE);
    }
}

// gaze estimation with single face input image and with MPIIGaze method
Point3f GazePredictor::predictGazeMPIIGaze(cv::Mat input_image) {
    vector<Mat> img_vec;

    img_vec.push_back(input_image);
    Vec2f gaze_norm_2d;
    Point3f gaze_norm_3d;

    std::vector<int> labelVector;
    labelVector.clear();
    labelVector.push_back(1);
    labelVector.push_back(1);
    float loss = 0.0;
    caffe::shared_ptr<caffe::MemoryDataLayer<float> > data_layer_;
    data_layer_ = boost::static_pointer_cast<MemoryDataLayer<float> >(p_net_->layer_by_name("data"));
    data_layer_->AddMatVector(img_vec, labelVector);

    // run network
    p_net_->ForwardPrefilled(&loss);

    if (model_type_==1)
    {
        // get output layer "ip2"
        float *temp = (float*)p_net_->blob_by_name("ip2")->cpu_data();
        // copy estimated gaze vector
        gaze_norm_2d.val[0] = temp[0];
        gaze_norm_2d.val[1] = temp[1];
        temp = nullptr;
    }
    else if (model_type_==2)// if it is googlenet
    {
        float *temp1 = (float*)p_net_->blob_by_name("loss1/classifier")->cpu_data();
        float *temp2 = (float*)p_net_->blob_by_name("loss2/classifier")->cpu_data();
        float *temp3 = (float*)p_net_->blob_by_name("loss3/classifier")->cpu_data();
        // average the output of three output values
        gaze_norm_2d.val[0] = (temp1[0]+temp2[0]+temp3[0]) / 3.0f;
        gaze_norm_2d.val[1] = (temp1[1]+temp2[1]+temp3[1]) / 3.0f;
        temp1 = nullptr;
        temp2 = nullptr;
        temp3 = nullptr;
    }
    else if (model_type_==3)// if it is alexnet
    {
        float *temp;
        temp = (float*)p_net_->blob_by_name("fc8")->cpu_data();// blob name can be fc8
        if (temp == NULL)
            temp = (float*)p_net_->blob_by_name("gaze_output")->cpu_data(); //blob name can be gaze_output
        if (temp == NULL) {
            cout << "ERROR: cannot find the blob name in the model. The final blob name muse be fc8 or gaze_output" << endl;
            exit(EXIT_FAILURE);
        }
        // copy estimated gaze vector
        gaze_norm_2d.val[0] = temp[0];
        gaze_norm_2d.val[1] = temp[1];
        temp = NULL;
    }
    else if (model_type_==4)// if it is alexnet
    {
        float *temp;
        temp = (float*)p_net_->blob_by_name("fc8")->cpu_data();// blob name can be fc8
        if (temp == NULL)
            temp = (float*)p_net_->blob_by_name("gaze_output")->cpu_data(); //blob name can be gaze_output
        if (temp == NULL) {
            cout << "ERROR: cannot find the blob name in the model. The final blob name muse be fc8 or gaze_output" << endl;
            exit(EXIT_FAILURE);
        }

        // copy estimated gaze vector
        gaze_norm_2d.val[0] = temp[0];
        gaze_norm_2d.val[1] = temp[1];

        //// get the feature out
        //temp = (float*)p_net_->blob_by_name("fc6_gaze")->cpu_data();
        //for (int num_f=0; num_f<4096; ++num_f)
        //{
        //    feature[num_f] = temp[num_f];
        //}
        temp = NULL;
    }

    float theta = gaze_norm_2d.val[0];
    float phi = gaze_norm_2d.val[1];
    gaze_norm_3d.x = (-1.0f)*cos(theta)*sin(phi);
    gaze_norm_3d.y = (-1.0f)*sin(theta);
    gaze_norm_3d.z = (-1.0f)*cos(theta)*cos(phi);

    return gaze_norm_3d;
}

}