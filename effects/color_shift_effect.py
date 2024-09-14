# effects/color_shift_effect.py

import numpy as np
from moviepy.editor import ImageClip, AudioFileClip
from scipy.signal import medfilt
import matplotlib.colors

def apply_effect(audio_path, image_path, output_video):
    # Load audio using MoviePy
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Get audio data for processing
    audio_array = audio_clip.to_soundarray(fps=22050)
    audio_mono = audio_array.mean(axis=1)  # Convert to mono

    # Normalize audio
    amplitudes = np.abs(audio_mono)
    amplitudes = medfilt(amplitudes, kernel_size=31)
    amplitudes = amplitudes / np.max(amplitudes)

    # Load image
    image_clip = ImageClip(image_path).set_duration(duration)

    # Function to shift colors
    def color_shift(get_frame, t):
        idx = int(t * 22050)
        if idx >= len(amplitudes):
            idx = len(amplitudes) - 1
        shift = 50 * amplitudes[idx]  # Adjust the shift factor as needed
        frame = get_frame(t)
        frame_hsv = matplotlib.colors.rgb_to_hsv(frame / 255.0)
        frame_hsv[:, :, 0] = (frame_hsv[:, :, 0] + shift / 360.0) % 1.0
        frame_rgb = matplotlib.colors.hsv_to_rgb(frame_hsv) * 255.0
        return frame_rgb.astype('uint8')

    # Apply the effect
    color_clip = image_clip.fl(color_shift, apply_to=['mask', 'video'])

    # Set audio and write the video
    color_clip = color_clip.set_audio(audio_clip)
    color_clip.write_videofile(output_video, fps=30)
