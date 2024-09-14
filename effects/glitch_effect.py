# effects/glitch_effect.py

import numpy as np
from moviepy.editor import ImageClip, AudioFileClip
from scipy.signal import medfilt

def apply_effect(audio_path, image_path, output_video):
    # Загрузка аудио
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Получение аудиоданных для обработки
    audio_array = audio_clip.to_soundarray(fps=44100)
    audio_mono = audio_array.mean(axis=1)  # Преобразуем в моно

    # Нормализация амплитуды аудио
    amplitudes = np.abs(audio_mono)
    amplitudes = medfilt(amplitudes, kernel_size=31)
    amplitudes = amplitudes / np.max(amplitudes)

    # Загрузка изображения и установка длительности
    image_clip = ImageClip(image_path).set_duration(duration)

    # Получение размеров изображения
    width, height = image_clip.size

    # Функция для применения глитч-эффекта
    def glitch_effect(get_frame, t):
        frame = get_frame(t)

        idx = int(t * 44100)
        if idx >= len(amplitudes):
            idx = len(amplitudes) - 1

        # Определяем интенсивность глитча на основе амплитуды аудио
        glitch_intensity = amplitudes[idx]

        # Применяем глитч с вероятностью, пропорциональной интенсивности
        if np.random.rand() < glitch_intensity * 0.5:
            # Случайные параметры глитча
            max_offset = int(10 + 20 * glitch_intensity)  # Смещение пикселей
            offset_x = np.random.randint(-max_offset, max_offset)
            offset_y = np.random.randint(-max_offset, max_offset)
            glitch_frame = np.roll(frame, shift=(offset_y, offset_x), axis=(0, 1))

            # Случайное изменение цветовых каналов
            if np.random.rand() < 0.5:
                glitch_frame[:, :, 0] = np.roll(glitch_frame[:, :, 0], shift=np.random.randint(-5, 5), axis=0)
            if np.random.rand() < 0.5:
                glitch_frame[:, :, 1] = np.roll(glitch_frame[:, :, 1], shift=np.random.randint(-5, 5), axis=1)
            if np.random.rand() < 0.5:
                glitch_frame[:, :, 2] = np.roll(glitch_frame[:, :, 2], shift=np.random.randint(-5, 5), axis=0)

            # Добавляем шум
            noise_amplitude = glitch_intensity * 50
            noise = np.random.randint(-noise_amplitude, noise_amplitude, frame.shape, dtype='int16')
            glitch_frame = np.clip(glitch_frame.astype('int16') + noise, 0, 255).astype('uint8')

            return glitch_frame

        else:
            return frame

    # Применение глитч-эффекта
    glitch_clip = image_clip.fl(glitch_effect, apply_to=['mask', 'video'])

    # Установка аудио и сохранение видео
    final_clip = glitch_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_video, fps=30)

