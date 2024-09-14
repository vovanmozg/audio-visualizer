# effects/pulse_effect.py

import numpy as np
from moviepy.editor import VideoClip
from moviepy.editor import ImageClip
from pydub import AudioSegment
from scipy.signal import medfilt

def apply_effect(audio_path, image_path, output_video):
    # Загрузка аудио
    audio_segment = AudioSegment.from_file(audio_path)
    audio_array = np.array(audio_segment.get_array_of_samples()).astype(np.float32)
    if audio_segment.channels == 2:
        audio_array = audio_array.reshape((-1, 2))
        audio_mono = audio_array.mean(axis=1)
    else:
        audio_mono = audio_array

    # Нормализация аудио
    amplitudes = np.abs(audio_mono)
    amplitudes = medfilt(amplitudes, kernel_size=31)
    amplitudes = amplitudes / np.max(amplitudes)

    # Загрузка изображения
    image_clip = ImageClip(image_path)
    duration = audio_segment.duration_seconds
    image_clip = image_clip.set_duration(duration)

    # Функция для пульсации
    def pulse(get_frame, t):
        idx = int(t * audio_segment.frame_rate)
        if idx >= len(amplitudes):
            idx = len(amplitudes) - 1
        scale = 1 + 0.05 * amplitudes[idx]
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

    # Применение эффекта
    pulsating_clip = image_clip.fl(pulse)
    pulsating_clip = pulsating_clip.set_audio(audio_segment)
    pulsating_clip.write_videofile(output_video, fps=30)
