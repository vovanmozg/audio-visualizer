#!/bin/bash

# Проверка наличия аргумента эффекта
if [ "$#" -lt 1 ]; then
    echo "Использование: ./gen.sh [effect_name] [audio_file] [image_file] [output_file]"
    echo "Доступные эффекты: pulse, color_shift, visualization"
    exit 1
fi

# Присваиваем переменным значения по умолчанию
EFFECT="$1"
AUDIO_FILE="${2:-audio.mp3}"
IMAGE_FILE="${3:-image.jpg}"
OUTPUT_FILE="${4:-output.mp4}"

# Запуск Docker-контейнера с передачей параметров
docker run --rm -v "$(pwd)":/app audio_visualizer "$AUDIO_FILE" "$IMAGE_FILE" "$OUTPUT_FILE" "$EFFECT"
