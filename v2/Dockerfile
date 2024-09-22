FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    libopencv-dev \
    ffmpeg \
    libavformat-dev \
    libavcodec-dev \
    libavutil-dev \
    libswresample-dev

# Копируем исходный код в контейнер
COPY . /app
WORKDIR /app

# Компилируем проект
RUN g++ -o video_effect main.cpp color_shift.cpp -lavformat -lavcodec -lavutil -lswresample `pkg-config --cflags --libs opencv4`

# Устанавливаем точку входа
ENTRYPOINT ["./video_effect"]
