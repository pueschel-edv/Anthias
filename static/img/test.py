import cv2
import numpy as np






def converter(uri):
    img = cv2.imread(uri)
    height, width, _ = img.shape
    fps = 1 

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(f'{uri}.mp4', fourcc, fps, (1920, 1080))


    black_img = np.zeros((1080, 1920, 3), dtype=np.uint8)


    x_offset = (1920 - width) // 2
    y_offset = (1080 - height) // 2


    if width > 1920 or height > 1080:
        scale_factor = min(1920 / width, 1080 / height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        img = cv2.resize(img, (new_width, new_height))
        x_offset = (1920 - new_width) // 2
        y_offset = (1080 - new_height) // 2


    black_img[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img


    for i in range(fps * 5):
        out.write(black_img)


    out.release()


while True:
    uri = input("img:  ")
    converter(uri)
