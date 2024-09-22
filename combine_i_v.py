import cv2
import numpy as np

# Функция для создания альфа-канала на основе черного фона
def apply_mask(foreground, background):
    gray_foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_foreground, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    particles = cv2.bitwise_and(foreground, foreground, mask=mask)
    background_part = cv2.bitwise_and(background, background, mask=mask_inv)
    result = cv2.add(background_part, particles)
    return result

# Открываем видео с частицами и изображение
video = cv2.VideoCapture('particles_video.mp4')
background_image = cv2.imread('background_image.jpg')

fps = video.get(cv2.CAP_PROP_FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)

# Открываем видеопоток для записи результата
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

background_image = cv2.resize(background_image, frame_size)

while True:
    ret, frame = video.read()
    if not ret:
        break

    output_frame = apply_mask(frame, background_image)
    out.write(output_frame)

video.release()
out.release()
cv2.destroyAllWindows()
