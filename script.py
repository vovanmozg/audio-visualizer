import sys
import os
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    VideoFileClip,
)
import subprocess

def create_audio_spectrum(audio_path, output_path, duration, size):
    # Команда FFmpeg для создания эквалайзера
    cmd = [
        'ffmpeg',
        '-i', audio_path,
        '-filter_complex',
        f"showspectrum=s={size[0]}x{size[1]}:mode=separate:color=intensity:scale=cbrt",
        '-frames:v', str(int(duration * 30)),
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
    spectrum_video = 'spectrum.mp4'
    spectrum_size = (1280, 200)  # Ширина и высота эквалайзера
    create_audio_spectrum(audio_path, spectrum_video, duration, spectrum_size)

    # Загрузка изображения и настройка его длительности
    image_clip = ImageClip(image_path).set_duration(duration)

    # Загрузка видео с эквалайзером
    spectrum_clip = VideoFileClip(spectrum_video).set_duration(duration)

    # Размещение эквалайзера внизу изображения
    spectrum_clip = spectrum_clip.set_position(('center', 'bottom'))

    # Объединение изображений
    final_clip = CompositeVideoClip([image_clip, spectrum_clip])
    final_clip = final_clip.set_audio(audio_clip)

    # Экспорт финального видео
    final_clip.write_videofile(output_video, fps=30)

    # Удаление временного файла
    os.remove(spectrum_video)
    print(f"Видео успешно создано: {output_video}")

if __name__ == "__main__":
    main()
