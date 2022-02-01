import cv2


def opencv_resize(image, ratio):
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def approximate_contour(contour):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, 0.02 * peri, True)


def get_receipt_contour(contours):
    largest = sorted(contours, key=lambda x: x.shape[0])[-1]
    approx = approximate_contour(largest)
    return approx


image = cv2.imread('../static/receipt1.jpg', cv2.IMREAD_UNCHANGED)
original = image.copy()
# Resize
resize_ratio = 500 / image.shape[0]
image = opencv_resize(image, 0.5)
cv2.imwrite('resized.jpg', image)
# Grey
src_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('grey.jpg', src_gray)
# Blurred
src_blur = cv2.blur(src_gray, (3, 3))
cv2.imwrite('grey_blur.jpg', src_blur)
# Dilated
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
src_dilated = cv2.dilate(src_blur, rectKernel)
cv2.imwrite('grey_blur_dilated.jpg', src_dilated)

threshold = 250
# Detect edges using Canny
src_edged = cv2.Canny(src_dilated, threshold, threshold * 2, apertureSize=3)
cv2.imwrite('canny.jpg', src_edged)

# Find contours
contours, hierarchy = cv2.findContours(src_edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours
color = (0, 255, 0)
contours = get_receipt_contour(contours)
img_with_contours = cv2.drawContours(image.copy(), [contours], -1, color, thickness=3)
cv2.imwrite('contours2.jpg', img_with_contours)