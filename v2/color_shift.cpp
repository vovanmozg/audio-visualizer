#include "color_shift.h"

void applyColorShift(cv::Mat& frame, double audio_level) {
    // Применяем смещение цвета на основе уровня аудио
    cv::Mat hsv;
    cv::cvtColor(frame, hsv, cv::COLOR_BGR2HSV);

    for(int y = 0; y < hsv.rows; y++) {
        for(int x = 0; x < hsv.cols; x++) {
            // Смещаем оттенок (H) на основе audio_level
            hsv.at<cv::Vec3b>(y,x)[0] = (hsv.at<cv::Vec3b>(y,x)[0] + static_cast<int>(audio_level * 180)) % 180;
        }
    }

    cv::cvtColor(hsv, frame, cv::COLOR_HSV2BGR);
}
