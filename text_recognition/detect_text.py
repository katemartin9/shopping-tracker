import pytesseract
import cv2
import glob
from text_recognition.img_processing_for_text import process_image_for_ocr
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\marti\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'


def save_to_file(text, filename):
    with open(f"../output/{filename}.txt", "w") as file:
        for line in text.split('\n'):
            line = line.strip()
            if len(line) > 0:
                file.write(line)
                file.write("\n")


def extract_text(path):
    cv2.imread(path)
    custom_config = r'--oem 3 --psm 4'
    image = process_image_for_ocr(path)
    text = pytesseract.image_to_string(image, lang='eng', config=custom_config)
    filename = path.split('\\')[-1].split('.')[0]  # on windows '../static\\IMG_20220609_0002.jpg'
    save_to_file(text, filename)


images = glob.glob('../static/*.jpg')
for img_path in images:
    extract_text(img_path)


