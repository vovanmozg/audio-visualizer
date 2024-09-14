import sys
import os
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    VideoFileClip
)
from moviepy.video.fx.all import mask_color
import subprocess

def create_audio_equalizer(audio_path, output_path, duration, size):
    # Создание фильтра filter_complex с использованием showfreqs
    filter_complex = (
        f"[0:a]showfreqs=s={size[0]}x{size[1]}:mode=bar:ascale=log:colors=white[eq];"
        f"color=s={size[0]}x{size[1]}:c=Green[bg];"
        f"[bg][eq]overlay=format=auto"
    )

    cmd = [
        'ffmpeg',
        '-y',  # Перезаписывать выходной файл без запроса
        '-i', audio_path,
        '-filter_complex', filter_complex,
        '-frames:v', str(int(duration * 30)),
        '-pix_fmt', 'rgba',
        output_path
    ]
    subprocess.run(cmd, check=True)

def main():
    if len(sys.argv) != 4:
        print("Использование: python script.py audio.mp3 image.jpg output.mp4")
        sys.exit(1)

    audio_path = sys.argv[1]
    image_path = sys.argv[2]
    output_video = sys.argv[3]

    # Проверка наличия файлов
    if not os.path.isfile(audio_path):
        print(f"Файл {audio_path} не найден.")
        sys.exit(1)
    if not os.path.isfile(image_path):
        print(f"Файл {image_path} не найден.")
        sys.exit(1)

    # Загрузка аудио и получение длительности
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Создание эквалайзера с помощью FFmpeg
    equalizer_video = 'equalizer.mp4'
    equalizer_size = (1280, 200)  # Ширина и высота эквалайзера
    create_audio_equalizer(audio_path, equalizer_video, duration, equalizer_size)

    # Загрузка изображения и настройка его длительности
    image_clip = ImageClip(image_path).set_duration(duration)

    # Загрузка видео с эквалайзером
    equalizer_clip = VideoFileClip(equalizer_video).set_duration(duration)

    # Применение маски для удаления зелёного фона
    equalizer_clip = equalizer_clip.fx(mask_color, color=[0, 255, 0], thr=50, s=5)

    # Размещение эквалайзера поверх изображения
    equalizer_clip = equalizer_clip.set_position(('center', 'bottom'))

    # Объединение клипов
    final_clip = CompositeVideoClip([image_clip, equalizer_clip])
    final_clip = final_clip.set_audio(audio_clip)

    # Экспорт финального видео
    final_clip.write_videofile(output_video, fps=30)

    # Удаление временного файла
    os.remove(equalizer_video)
    print(f"Видео успешно создано: {output_video}")

if __name__ == "__main__":
    main()
