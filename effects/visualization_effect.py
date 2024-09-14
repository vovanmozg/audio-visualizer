# effects/visualization_effect.py

import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip

def apply_effect(audio_path, image_path, output_video):
    # Создание визуализации с помощью FFmpeg
    visualization_video = 'visualization.mp4'
    visualization_size = (1280, 720)

    filter_complex = (
        f"[0:a]showspectrum=s={visualization_size[0]}x{visualization_size[1]}:"
        f"mode=combined:slide=scroll:color=rainbow:scale=log[spec];"
        f"color=s={visualization_size[0]}x{visualization_size[1]}:c=black[bg];"
        f"[bg][spec]overlay=format=auto"
    )

    cmd = [
        'ffmpeg',
        '-y',
        '-i', audio_path,
        '-filter_complex', filter_complex,
        '-pix_fmt', 'yuv420p',
        visualization_video
    ]
    subprocess.run(cmd, check=True)

    # Загрузка визуализации и аудио
    visualization_clip = VideoFileClip(visualization_video)
    audio_clip = AudioFileClip(audio_path)
    visualization_clip = visualization_clip.set_audio(audio_clip)
    visualization_clip.write_videofile(output_video, fps=30)

    # Удаление временного файла
    import os
    os.remove(visualization_video)
