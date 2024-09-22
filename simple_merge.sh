#!/bin/bash

# Проверка наличия всех аргументов
if [ "$#" -ne 3 ]; then
    echo "Использование: $0 путь_к_картинке путь_к_музыке путь_к_видео"
    exit 1
fi

# Аргументы
IMAGE=$1
MUSIC=$2
OUTPUT_VIDEO=$3

# Проверка наличия изображений и музыки
if [ ! -f "$IMAGE" ]; then
    echo "Ошибка: файл изображения не найден: $IMAGE"
    exit 1
fi

if [ ! -f "$MUSIC" ]; then
    echo "Ошибка: музыкальный файл не найден: $MUSIC"
    exit 1
fi

# Выполнение команды ffmpeg для создания видео
# ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v libx264 -c:a aac -b:a 192k -shortest -vf "scale=1280:720" -pix_fmt yuv420p "$OUTPUT_VIDEO"
# без масштабирования
#ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v libx264 -c:a aac -b:a 192k -shortest -pix_fmt yuv420p "$OUTPUT_VIDEO"
# 1 кадр на все видео
# ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v libx264 -preset fast -r 1 -c:a aac -b:a 192k -shortest -pix_fmt yuv420p "$OUTPUT_VIDEO"
# понизим качество звука
#ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v libx264 -preset ultrafast -r 1 -c:a libmp3lame -b:a 128k -shortest -pix_fmt yuv420p "$OUTPUT_VIDEO"
# отключим перекодирование звука
#ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v libx264 -preset ultrafast -r 1 -c:a copy -shortest "$OUTPUT_VIDEO"
# использовать другой кодек
#ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v mpeg4 -preset ultrafast -r 1 -c:a copy -shortest "$OUTPUT_VIDEO"
# использовать многопоточность
# ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v mpeg4 -preset ultrafast -r 1 -q:v 31 -c:a copy -shortest -threads 16 "$OUTPUT_VIDEO"
# вернуть качество видео
ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v libx264 -c:a copy -shortest -pix_fmt yuv420p "$OUTPUT_VIDEO"


#
#ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v libx264 -preset ultrafast -r 1 -q:v 31 -c:a copy -shortest "$OUTPUT_VIDEO"
#
#ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v mpeg4 -preset ultrafast -r 1 -q:v 31 -c:a copy -shortest "$OUTPUT_VIDEO"
#ffmpeg -loop 1 -i "$IMAGE" -i "$MUSIC" -c:v mpeg4 -preset ultrafast -r 1 -q:v 31 -c:a copy -shortest -threads 8 "$OUTPUT_VIDEO"






# Проверка успешности выполнения
if [ $? -eq 0 ]; then
    echo "Видео успешно создано: $OUTPUT_VIDEO"
else
    echo "Произошла ошибка при создании видео."
    exit 1
fi
