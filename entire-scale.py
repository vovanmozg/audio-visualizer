import sys
import os
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
)
import numpy as np
from pydub import AudioSegment

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
    print(f"Audio duration: {duration} seconds")

    # Загрузка изображения и настройка его длительности
    image_clip = ImageClip(image_path).set_duration(duration)

    # Загрузка аудио с помощью pydub
    audio_segment = AudioSegment.from_file(audio_path)
    audio_array = np.array(audio_segment.get_array_of_samples())
    audio_array = audio_array.astype(np.float32)

    # Нормализация аудиоданных
    if audio_segment.channels == 2:
        audio_array = audio_array.reshape((-1, 2))
        audio_mono = audio_array.mean(axis=1)
    else:
        audio_mono = audio_array

    amplitudes = np.abs(audio_mono)
    # Сглаживание сигнала
    from scipy.signal import medfilt
    amplitudes = medfilt(amplitudes, kernel_size=31)

    # Нормализация амплитуды
    amplitudes = amplitudes / np.max(amplitudes)

    # Создание функции для изменения масштаба изображения
    def pulse(get_frame, t):
        idx = int(t * audio_segment.frame_rate)
        if idx >= len(amplitudes):
            idx = len(amplitudes) - 1
        scale = 1 + 0.05 * amplitudes[idx]  # Изменение масштаба на ±5%
        frame = get_frame(t)
        height, width = frame.shape[:2]
        new_size = (int(width * scale), int(height * scale))
        frame_resized = ImageClip(frame).resize(new_size).get_frame(0)
        frame_resized = np.array(frame_resized)
        # Центрируем изображение
        y_offset = (frame_resized.shape[0] - height) // 2
        x_offset = (frame_resized.shape[1] - width) // 2
        frame_cropped = frame_resized[y_offset:y_offset+height, x_offset:x_offset+width]
        return frame_cropped

    # Применение эффекта пульсации
    pulsating_clip = image_clip.fl(pulse)

    # Добавляем аудио к клипу
    final_clip = pulsating_clip.set_audio(audio_clip)

    # Экспорт финального видео
    final_clip.write_videofile(output_video, fps=30)

    print(f"Видео успешно создано: {output_video}")

if __name__ == "__main__":
    main()
