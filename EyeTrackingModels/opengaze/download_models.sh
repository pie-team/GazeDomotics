OPENGAZE_DIR=~/OpenGaze

mkdir -p $OPENGAZE_DIR/content/caffeModel

cd $OPENGAZE_DIR/content/caffeModel

wget https://datasets.d2.mpi-inf.mpg.de/MPIIGaze/alexnet_face.prototxt

wget https://datasets.d2.mpi-inf.mpg.de/MPIIGaze/alexnet_face.caffemodel