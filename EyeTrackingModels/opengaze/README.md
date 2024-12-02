# OpenGaze: Open Source Toolkit for Camera-Based Gaze Estimation and Interaction

Appearance-based gaze estimation methods that only require an off-the-shelf camera have significantly improved and promise a wide range of new applications in gaze-based interaction and attentive user interfaces. However, these methods are not yet widely used in the human-computer interaction (HCI) community.

To democratize their use in HCI, we present OpenGaze, the first software toolkit that is specifically developed for gaze interface designers. OpenGaze is open source and aims to implement state-of-the-art methods for camera-based gaze estimation and interaction.

## Functionality

The toolkit is capable of performing the following gaze-related tasks:

* **Gaze Estimation**
Estimate and show a user's gaze on a screen in real time.

[![Demo](https://img.youtube.com/vi/aenp4ZWjBZo/0.jpg)](https://youtu.be/aenp4ZWjBZo "Gaze Estimation")
<p>&nbsp;</p>

* **Gaze Visualization**
Plot gaze direction in images.

[![Demo](https://img.youtube.com/vi/9Lujg3beiYI/0.jpg)](https://youtu.be/9Lujg3beiYI "Gaze Visualization")
<p>&nbsp;</p>

* **Personal Calibration**
Perform personal calibration and remap the gaze target on a screen.

[![Demo](https://img.youtube.com/vi/BjhZcRw4N-w/0.jpg)](https://youtu.be/BjhZcRw4N-w "Personal Calibration")
<p>&nbsp;</p>

## Installation
[Unix Installation](https://git.hcics.simtech.uni-stuttgart.de/public-projects/opengaze/wikis/Unix-installation)

## Use
[Command line arguments](https://git.hcics.simtech.uni-stuttgart.de/public-projects/opengaze/wikis/Command-line-arguments)

## Citation
**If you use any of the resources provided on this page in any of your publications, please cite the following paper:**

```
Evaluation of Appearance-Based Methods and Implications for Gaze-Based Applications
Xucong Zhang, Yusuke Sugano, Andreas Bulling
Proc. ACM SIGCHI Conference on Human Factors in Computing Systems (CHI), 2019
```
[Project page](https://www.perceptualui.org/publications/zhang19_chi/)

@inproceedings{zhang19_chi,<br/>
title = {Evaluation of Appearance-Based Methods for Gaze-Based Applications},<br/>
author = {Xucong Zhang and Yusuke Sugano and Andreas Bulling},<br/>
doi = {10.1145/3290605.3300646},<br/>
year = {2019},<br/>
booktitle = {Proc. ACM SIGCHI Conference on Human Factors in Computing Systems (CHI)},<br/>
abstract = {Appearance-based gaze estimation methods that only require an off-the-shelf camera have significantly improved but they are still not yet widely used in the human-computer interaction (HCI) community. This is partly because it remains unclear how they perform compared to model-based approaches as well as dominant, special-purpose eye tracking equipment. To address this limitation, we evaluate the performance of state-of-the-art appearance-based gaze estimation for interaction scenarios with and without personal calibration, indoors and outdoors, for different sensing distances, as well as for users with and without glasses. We discuss the obtained findings and their implications for the most important gaze-based applications, namely explicit eye input, attentive user interfaces, gaze-based user modelling, and passive eye monitoring. To democratise the use of appearance-based gaze estimation and interaction in HCI, we finally present OpenGaze (www.opengaze.org), the first software toolkit for appearance-based gaze estimation and interaction.}<br/>
}

## License

The license agreement can be found in [LICENSE](https://git.hcics.simtech.uni-stuttgart.de/public-projects/opengaze/blob/master/LICENSE).

You have to respect boost, OpenFace and OpenCV licenses.

Furthermore, you have to respect the licenses of the datasets used for [model training](https://git.hcics.simtech.uni-stuttgart.de/public-projects/opengaze/wikis/Model-training).

## Code layout
* caffe-layers: Our customized layers for the Caffe library.
* content: Directory for storing calibration configurations, Caffe model and face model
* exe: Example code to call the opengaze library
* include:
    * opengaze: Directory of head files
* pre-compiled:
    * opengaze_1.0.deb: The pre-compiled installation file
* src: Directory of source files
* CMakeLists.txt: CMake file to compile OpenGaze
* default.cfg: The configuration file for setting input parameters
* download_models.sh: Script to download the pre-trained Caffe model
* install.sh: Script to install dependencies except for Caffe and OpenFace.
* README.md
* RELEASE.md: Release notes

## Contact
email: opengaze.toolkit@gmail.com
