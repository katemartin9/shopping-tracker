import cv2
import numpy as np
import time
IMAGE_SIZE = 1800
BINARY_THREHOLD = 180


def process_image_for_ocr(file_path):
    im_new = remove_noise_and_smooth(file_path)
    return im_new


def image_smoothing(img_grey):
    ret1, th1 = cv2.threshold(img_grey, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothing(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image