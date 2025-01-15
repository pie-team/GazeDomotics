#ifndef FACE_DETECTOR_HPP
#define FACE_DETECTOR_HPP

#include <iostream>
#include <vector>
#include <string>
#include <opencv2/opencv.hpp>

#if USE_DLIB
// if we use dlib
#include <dlib/opencv.h>
#include <dlib/image_processing/frontal_face_detector.h>
#include <dlib/image_processing/render_face_detections.h>
#include <dlib/image_processing.h>
#include <dlib/gui_widgets.h>
#include <dlib/image_io.h>
#endif


#include "data.hpp"

namespace opengaze{

class FaceDetector {
public:
    FaceDetector();
    ~FaceDetector();

    /**
     * face and facial landmark detection selection
     * The current implementation is only OpenFace. OpenFace use dlib for face detection
     */
    enum Method{OpenFace, OpenCV, Dlib};

    /**
     * main function to detect and track face and facial landmarks
     * @param input_img input image
     * @param output output data structure
     */
    void track_faces(cv::Mat input_img, std::vector<opengaze::Sample> &output);

    void reset();
    void setMethodType(Method method_type) {method_type_ = method_type;}
    Method getMethodType() {return method_type_;}
    void initialize(int number_users);

private:
    Method method_type_;

    #if USE_DLIB
    dlib::frontal_face_detector dlib_detector_;
    dlib::shape_predictor dlib_sp_;
    #endif

    // parameters for OpenFace
    std::vector<bool> active_models_;
    unsigned long num_faces_max_;
    int detection_skip_frames_, tracking_loss_limit_;
    float detection_resize_rate_;
    float nonoverlap_threshold_;
    double certainty_threshold_;
    int landmark_indices_[6];
    int frame_counter_;
    unsigned long current_face_id_;
    std::vector<unsigned long> face_ids_;
};
}




#endif //FACE_DETECTOR_HPP
