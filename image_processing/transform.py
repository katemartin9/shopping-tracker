import numpy as np
import cv2


def order_points(pts):
	"""
	This function initializes a list of coordinates that will be ordered
	such that:
	- the first entry in the list is the top-left,
	- the second entry is the top-right,
	- the third is the bottom-right
	- the fourth is the bottom-left
	Computes the sum:
	The top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum
	Computes the difference:
	The top-right point will have the smallest difference whereas the bottom-left will have the largest difference

	:param pts: x,y coordinates of an image
	:return:
	"""
	rect = np.zeros((4, 2), dtype="float32")
	s = pts.sum(axis=1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	diff = np.diff(pts, axis=1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	return rect


def four_point_transform(image, pts):
	"""
	This function calls order points to obtain a consistent order of the points and unpack them.
	It then computes the width of the new image which will be the maximum distance bottom-right
	and bottom-left x-coordinates or the top-right and top-left x-coordinates.
	It also computes the height of the new image, which will be the maximum distance
	between the top-right and bottom-right y-coordinates or the top-left and bottom-left y-coordinates.
	Once the new dimensions are obtained it will construct the set of destination points to obtain
	a "birds eye view" of the image, again specifying points in the top-left, top-right, bottom-right, and bottom-left.

	:param image: scanned image
	:param pts: x,y coordinates of an image
	:return:
	"""
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	max_width = max(int(width_a), int(width_b))

	height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	max_height = max(int(height_a), int(height_b))

	dst = np.array([
		[0, 0],
		[max_width - 1, 0],
		[max_width - 1, max_height - 1],
		[0, max_height - 1]], dtype = "float32")

	mtrx = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, mtrx, (max_width, max_height))
	return warped