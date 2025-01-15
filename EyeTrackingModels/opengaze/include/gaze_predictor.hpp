#ifndef GAZE_PREDICTOR_HPP
#define GAZE_PREDICTOR_HPP

#include <opencv2/opencv.hpp>
#include "data.hpp"
#include "face_detector.hpp"


namespace opengaze{

class GazePredictor {

public:
    GazePredictor();
    ~GazePredictor();

    void initiaMPIIGaze(std::vector<std::string> arguments);
    cv::Point3f predictGazeMPIIGaze(cv::Mat face_patch);

private:
    int model_type_;
    bool is_extract_feature;
};

}



#endif //GAZE_PREDICTOR_HPP
