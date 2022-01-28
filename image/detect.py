import imutils
import cv2


def detect_edges(image):
    img_blur = convert_to_grey_blur(image)
    edged = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)
    return edged


def convert_to_grey_blur(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    return img_blur


def detect_frame(edges):
    contours = cv2.findContours(edges.copy(), mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            return approx
