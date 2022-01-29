import pytesseract
import cv2

img = cv2.imread("../static/scanned_result.jpg")

custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(img, config=custom_config)

with open("../outputs/recognized_from_scan.txt", "w") as file:
    for line in text.split('\n'):
        line = line.strip()
        if len(line) > 0:
            file.write(line)
            file.write("\n")