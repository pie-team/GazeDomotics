#include <cmath>
#include <algorithm>
#include <vector>

#include "caffe/layer.hpp"
#include "caffe/layers/dspp_layer.hpp"

#include <boost/spirit/include/phoenix_core.hpp>
#include <boost/spirit/include/phoenix_operator.hpp>


namespace caffe {
    template <typename Dtype>
    void DSPPLayer<Dtype>::LayerSetUp(const vector<Blob<Dtype>*>& bottom,
            const vector<Blob<Dtype>*>& top) {
    }

    template <typename Dtype>
    void DSPPLayer<Dtype>::Reshape(const vector<Blob<Dtype>*>& bottom, const vector<Blob<Dtype>*>& top) {

        num_ = bottom[1]->shape()[0];
        channel_ = bottom[1]->shape()[1]; // the input data size
        height_ = bottom[1]->shape()[2];
        width_ = bottom[1]->shape()[3];

        // init output size
        vector<int> output_shape;
        output_shape.push_back(num_);
        output_shape.push_back(channel_);
        output_shape.push_back(height_);
        output_shape.push_back(width_);
        top[0]->Reshape(output_shape);
    }

    template <typename Dtype>
    void DSPPLayer<Dtype>::Forward_cpu(const vector<Blob<Dtype>*>& bottom,
            const vector<Blob<Dtype>*>& top) {
        Dtype* top_data = top[0]->mutable_cpu_data();

        caffe_set<Dtype>(top[0]->count(), 0, top_data); // initilize to be 0

        for (int n=0; n<num_; ++n) {
            for (int h = 0; h < height_; ++h) { // for the input data size
                for (int w = 0; w < width_; ++w) {
                    for (int c = 0; c < channel_; ++c) {
                        top_data[top[0]->offset(n, c, h, w)] = bottom[1]->data_at(n, c, h, w) * bottom[0]->data_at(n, 0, h, w);
                    }   
                }
            }
        }
        top_data = NULL;
    }

    template <typename Dtype>
    void DSPPLayer<Dtype>::Backward_cpu(const vector<Blob<Dtype>*>& top,
            const vector<bool>& propagate_down,
            const vector<Blob<Dtype>*>& bottom) {
        if (propagate_down[0]) {
            const Dtype* top_diff = top[0]->cpu_diff();
            Dtype* data_diff = bottom[1]->mutable_cpu_diff();
            Dtype* heat_map_diff = bottom[0]->mutable_cpu_diff();

            caffe_set<Dtype>(bottom[1]->count(), 0, data_diff);
            caffe_set<Dtype>(bottom[0]->count(), 0, heat_map_diff);
            // Dtype activation_h, activation_w;

            for (int n = 0; n < num_; ++n) {
                for (int h = 0; h < height_; ++h) {
                    for (int w = 0; w < width_; ++w) {
                        for (int c = 0; c < channel_; ++c) {

                            Dtype buffer = top_diff[top[0]->offset(n, c, h, w)];
                            data_diff[bottom[1]->offset(n, c, h, w)] = buffer * (bottom[0]->data_at(n, 0, h, w));

                            buffer *= bottom[1]->data_at(n,c,h,w) / channel_;
                            
                            heat_map_diff[bottom[0]->offset(n,0,h,w)] += buffer;
                        }
                    }
                }
            }
            top_diff = NULL;
            data_diff = NULL;
            heat_map_diff = NULL;

        }
    }

INSTANTIATE_CLASS(DSPPLayer);
REGISTER_LAYER_CLASS(DSPP);

} // namespace caffe
