#include <iostream>
#include <vector>
#include <string>

#include <opencv2/opencv.hpp>

#include "opengaze/opengaze.hpp"

using namespace std;
using namespace cv;
using namespace opengaze;

vector<string> get_arguments(int argc, char **argv) {
    vector<string> arguments;
    for (int i = 0; i < argc; ++i){
        arguments.emplace_back(string(argv[i]));
    }
    return arguments;
}

int main(int argc, char** argv)
{
    vector<string> arguments = get_arguments(argc, argv);
    OpenGaze open_gaze(argc, argv);
    int num_calibration_point = 20;
    open_gaze.runPersonalCalibration(num_calibration_point);

    return 1;
}