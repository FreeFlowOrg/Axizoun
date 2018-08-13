# OCR using pytesseract

from PIL import Image
import pytesseract

img = Image.open('sample.jpg')
print(pytesseract.image_to_string(img, lang='eng'))
