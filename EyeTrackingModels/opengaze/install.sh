#!/bin/bash

set -e 
set -o pipefail

if [ $# -ne 0 ]
  then
    echo "Usage: install.sh"
    exit 1
fi

# Essential Dependencies
echo "Installing Essential dependencies..."
sudo apt-get -y update
sudo apt-get -y install build-essential
sudo apt-get -y install cmake
sudo apt-get -y install libopenblas-dev liblapack-dev
sudo apt-get -y install git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get -y install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev
echo "Essential dependencies installed."

# OpenCV Dependency
echo "Downloading OpenCV..."
wget https://github.com/opencv/opencv/archive/3.4.0.zip
unzip 3.4.0.zip
cd opencv-3.4.0
mkdir -p build
cd build
echo "Installing OpenCV..."
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=ON -D WITH_CUDA=OFF -D BUILD_SHARED_LIBS=ON ..
make -j4
sudo make install
cd ../..
rm 3.4.0.zip
sudo rm -r opencv-3.4.0
echo "OpenCV installed."

# dlib dependecy
echo "Downloading dlib"
wget http://dlib.net/files/dlib-19.13.tar.bz2;
tar xf dlib-19.13.tar.bz2;
cd dlib-19.13;
mkdir -p build;
cd build;
echo "Installing dlib"
cmake ..;
cmake --build . --config Release;
sudo make install;
sudo ldconfig;
cd ../..;    
rm -r dlib-19.13.tar.bz2
echo "dlib installed"

# Boost C++ Dependency
echo "Installing Boost..."
sudo apt-get install libboost-all-dev
echo "Boost installed."

# Dependency for caffe
sudo apt-get install protobuf glog gflags hdf5