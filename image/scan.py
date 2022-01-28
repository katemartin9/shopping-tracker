import cv2
from skimage.filters import threshold_local
from image.transform import four_point_transform
from image.detect import detect_edges, detect_frame

image = cv2.imread('../static/receipt2.jpg')
edges = detect_edges(image)

frame = detect_frame(edges)

image_copy = image.copy()
cv2.drawContours(image=image_copy, contours=[frame], contourIdx=-1, color=(0, 255, 0), thickness=2)
cv2.imwrite('contours.jpg', image_copy)

ratio = image.shape[0] / 500.0
orig_image = image.copy()
warped = four_point_transform(orig_image, frame.reshape(4, 2))
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset=10, method="gaussian")
warped = (warped > T).astype("uint8") * 255

cv2.imwrite('../static/scanned_result.jpg', warped)