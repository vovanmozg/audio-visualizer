#ifndef COLOR_SHIFT_H
#define COLOR_SHIFT_H

#include <opencv2/opencv.hpp>

void applyColorShift(cv::Mat& frame, double audio_level);

#endif // COLOR_SHIFT_H
