#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include <vector>
#include <cmath>
#include "color_shift.h"

extern "C" {
    #include <libavformat/avformat.h>
    #include <libavcodec/avcodec.h>
    #include <libswresample/swresample.h>
    #include <libavutil/opt.h>
    #include <libavutil/samplefmt.h>
    #include <libavutil/channel_layout.h>
}

// Функция для отображения прогресса
void displayProgress(int current, int total);

std::vector<double> getAudioLevels(const std::string& filename, int total_frames, double fps);

int main(int argc, char* argv[]) {
    if(argc != 4) {
        std::cout << "Usage: ./video_effect <input_video> <output_video> <effect_name>" << std::endl;
        return -1;
    }

    std::string inputVideo = argv[1];
    std::string outputVideo = argv[2];
    std::string effectName = argv[3];

    // Инициализируем FFmpeg
    av_register_all();

    cv::VideoCapture cap(inputVideo);
    if(!cap.isOpened()) {
        std::cout << "Error opening input video." << std::endl;
        return -1;
    }

    int frame_width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    int frame_height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    double fps = cap.get(cv::CAP_PROP_FPS);
    int total_frames = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_COUNT));

    cv::VideoWriter writer(outputVideo, cv::VideoWriter::fourcc('M','J','P','G'), fps, cv::Size(frame_width, frame_height));

    std::cout << "Processing audio levels..." << std::endl;

    // Получаем уровни звука для каждого кадра
    std::vector<double> audio_levels = getAudioLevels(inputVideo, total_frames, fps);
    if(audio_levels.empty()) {
        std::cout << "Error processing audio levels." << std::endl;
        return -1;
    }

    std::cout << "Audio levels processed." << std::endl;

    cv::Mat frame;
    int frame_index = 0;
    std::cout << "Processing video frames..." << std::endl;
    while(cap.read(frame)) {
        if(frame_index >= audio_levels.size()) {
            std::cout << "Frame index out of range." << std::endl;
            break;
        }

        double audio_level = audio_levels[frame_index];

        if(effectName == "color_shift") {
            applyColorShift(frame, audio_level);
        } else {
            std::cout << "Unknown effect: " << effectName << std::endl;
            return -1;
        }

        writer.write(frame);

        // Обновляем прогресс каждые 10 кадров
        if (frame_index % 10 == 0 || frame_index == total_frames - 1) {
            displayProgress(frame_index + 1, total_frames);
        }

        frame_index++;
    }

    cap.release();
    writer.release();

    std::cout << "\nProcessing completed." << std::endl;
    return 0;
}

// Функция для отображения прогресса
void displayProgress(int current, int total) {
    int barWidth = 50;
    double progress = (double)current / total;

    std::cout << "\r[";
    int pos = barWidth * progress;
    for (int i = 0; i < barWidth; ++i) {
        if (i < pos) std::cout << "=";
        else if (i == pos) std::cout << ">";
        else std::cout << " ";
    }
    std::cout << "] " << int(progress * 100.0) << "% (" << current << "/" << total << ")    ";
    std::cout.flush();
}

std::vector<double> getAudioLevels(const std::string& filename, int total_frames, double fps) {
    std::vector<double> audio_levels(total_frames, 0.0);

    AVFormatContext* formatContext = nullptr;
    if (avformat_open_input(&formatContext, filename.c_str(), NULL, NULL) != 0) {
        std::cerr << "Could not open input file." << std::endl;
        return {};
    }

    if (avformat_find_stream_info(formatContext, NULL) < 0) {
        std::cerr << "Could not find stream information." << std::endl;
        avformat_close_input(&formatContext);
        return {};
    }

    AVCodec* codec = nullptr;
    int audioStreamIndex = av_find_best_stream(formatContext, AVMEDIA_TYPE_AUDIO, -1, -1, &codec, 0);
    if (audioStreamIndex < 0) {
        std::cerr << "Could not find audio stream in the input." << std::endl;
        avformat_close_input(&formatContext);
        return {};
    }

    AVCodecContext* codecContext = avcodec_alloc_context3(codec);
    if (!codecContext) {
        std::cerr << "Could not allocate codec context." << std::endl;
        avformat_close_input(&formatContext);
        return {};
    }

    avcodec_parameters_to_context(codecContext, formatContext->streams[audioStreamIndex]->codecpar);

    if (avcodec_open2(codecContext, codec, NULL) < 0) {
        std::cerr << "Could not open codec." << std::endl;
        avcodec_free_context(&codecContext);
        avformat_close_input(&formatContext);
        return {};
    }

    SwrContext* swr_ctx = swr_alloc();
    if (!swr_ctx) {
        std::cerr << "Could not allocate SwrContext." << std::endl;
        avcodec_free_context(&codecContext);
        avformat_close_input(&formatContext);
        return {};
    }

    av_opt_set_int(swr_ctx, "in_channel_layout", codecContext->channel_layout, 0);
    av_opt_set_int(swr_ctx, "in_sample_rate", codecContext->sample_rate, 0);
    av_opt_set_sample_fmt(swr_ctx, "in_sample_fmt", codecContext->sample_fmt, 0);

    av_opt_set_int(swr_ctx, "out_channel_layout", codecContext->channel_layout, 0);
    av_opt_set_int(swr_ctx, "out_sample_rate", codecContext->sample_rate, 0);
    av_opt_set_sample_fmt(swr_ctx, "out_sample_fmt", AV_SAMPLE_FMT_FLT, 0);

    if (swr_init(swr_ctx) < 0) {
        std::cerr << "Failed to initialize the resampling context." << std::endl;
        swr_free(&swr_ctx);
        avcodec_free_context(&codecContext);
        avformat_close_input(&formatContext);
        return {};
    }

    AVPacket* packet = av_packet_alloc();
    AVFrame* frame = av_frame_alloc();

    int64_t last_frame_index = -1;

    while (av_read_frame(formatContext, packet) >= 0) {
        if (packet->stream_index == audioStreamIndex) {
            if (avcodec_send_packet(codecContext, packet) < 0) {
                std::cerr << "Error sending packet for decoding." << std::endl;
                break;
            }
            while (avcodec_receive_frame(codecContext, frame) >= 0) {
                // Конвертируем аудио данные в формат float
                uint8_t** converted_data = nullptr;
                int dst_nb_samples = av_rescale_rnd(swr_get_delay(swr_ctx, codecContext->sample_rate) + frame->nb_samples,
                                                    codecContext->sample_rate, codecContext->sample_rate, AV_ROUND_UP);
                int ret = av_samples_alloc_array_and_samples(&converted_data, nullptr, codecContext->channels,
                                                             dst_nb_samples, AV_SAMPLE_FMT_FLT, 0);
                if (ret < 0) {
                    std::cerr << "Could not allocate converted samples." << std::endl;
                    break;
                }

                int converted_samples = swr_convert(swr_ctx, converted_data, dst_nb_samples,
                                                    (const uint8_t**)frame->data, frame->nb_samples);
                if (converted_samples < 0) {
                    std::cerr << "Error while converting." << std::endl;
                    av_freep(&converted_data[0]);
                    av_freep(&converted_data);
                    break;
                }

                // Вычисляем уровень звука (RMS)
                double sum = 0.0;
                int num_samples = converted_samples * codecContext->channels;
                float* samples = (float*)converted_data[0];
                for (int i = 0; i < num_samples; i++) {
                    float sample = samples[i];
                    sum += sample * sample;
                }
                double rms = sqrt(sum / num_samples);

                // Маппинг аудио времени на индекс кадра видео
                double audio_time = frame->best_effort_timestamp * av_q2d(formatContext->streams[audioStreamIndex]->time_base);
                int64_t frame_index = static_cast<int64_t>(audio_time * fps);
                if (frame_index >= 0 && frame_index < total_frames) {
                    // Учитываем максимальное значение уровня звука для кадра
                    if (frame_index != last_frame_index) {
                        audio_levels[frame_index] = rms;
                        last_frame_index = frame_index;
                    } else {
                        if (rms > audio_levels[frame_index]) {
                            audio_levels[frame_index] = rms;
                        }
                    }
                }

                av_freep(&converted_data[0]);
                av_freep(&converted_data);
            }
        }
        av_packet_unref(packet);
    }

    av_frame_free(&frame);
    av_packet_free(&packet);
    swr_free(&swr_ctx);
    avcodec_free_context(&codecContext);
    avformat_close_input(&formatContext);

    return audio_levels;
}
