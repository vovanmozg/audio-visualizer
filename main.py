# main.py
# https://chatgpt.com/c/66e5b6a9-e258-8007-af8e-b8b83e5e9dd9

import sys
import os

def main():
    print("Старт программы")
    if len(sys.argv) != 5:
        print("Использование: python main.py audio.mp3 image.jpg output.mp4 effect_name")
        print("Доступные эффекты: pulse, color_shift, visualization, glitch")
        sys.exit(1)

    audio_path = sys.argv[1]
    image_path = sys.argv[2]
    output_video = sys.argv[3]
    effect_name = sys.argv[4]

    # Проверка наличия файлов
    if not os.path.isfile(audio_path):
        print(f"Файл {audio_path} не найден.")
        sys.exit(1)
    if not os.path.isfile(image_path):
        print(f"Файл {image_path} не найден.")
        sys.exit(1)

    # Импорт выбранного эффекта
    if effect_name == 'pulse':
        from effects import pulse_effect as effect
    elif effect_name == 'color_shift':
        from effects import color_shift_effect as effect
    elif effect_name == 'visualization':
        from effects import visualization_effect as effect
    elif effect_name == 'glitch':
        from effects import glitch_effect as effect
    else:
        print(f"Эффект '{effect_name}' не найден.")
        print("Доступные эффекты: pulse, color_shift, visualization, glitch")
        sys.exit(1)

    # Применение эффекта
    print("Применяем эффект")
    effect.apply_effect(audio_path, image_path, output_video)
    print(f"Видео успешно создано: {output_video}")

if __name__ == "__main__":
    main()
