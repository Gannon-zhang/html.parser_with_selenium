#coding=utf-8
import pyocr


import pytesseract
from PIL import Image

# open image
image = Image.open('..\Training\cd17.png')
code = pytesseract.image_to_string(image, lang='chi_sim')
print code
