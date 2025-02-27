# coding: utf-8 -*-
import pathlib
import os
import re
import textwrap
import easyocr
import string
import sys

global file_result
file_result = ''

def pdf_to_jpg(inputpath, outputpath, pages='ALL'):
    result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, dpi=300, pages=pages)
    return result

# Extract the numeric part of the filename and convert it to an integer
def extract_number(filename):
    match = re.search(r'/(\d+)_', filename)
    if match:
        return int(match.group(1))
    return float('inf')  # Return infinity if no number is found

# Main
sys.stderr.write("PDF to TXT written by Jonathan Germain / github.com/compilebunny\n")
sys.stderr.write("Thanks to: https://github.com/JaidedAI/EasyOCR, https://github.com/pankajr141/pdf2jpg, and https://github.com/hansalemaos/PDFImage2TXT for 99% of the work\n\n")

if len(sys.argv) < 2:
    print('syntax: pdf2txt <file.pdf>')
    sys.exit(1)

reader = easyocr.Reader(['en'])
from pdf2jpg import pdf2jpg
#wrapper = textwrap.TextWrapper(width=70)

file_path = sys.argv[1]

# Extract directory name and base name, split into extension
directory_name = os.path.dirname(file_path)
base_name = os.path.basename(file_path)
inputpath = directory_name+'/'+base_name
droppath, suffix = os.path.splitext(file_path)

sys.stderr.write(f"inputpath: {inputpath}\n")

bigjpg = pdf_to_jpg(inputpath, '/tmp/test', pages='ALL')

sorted_imagefile_list = sorted(bigjpg[0]['output_jpgfiles'], key=extract_number)

'''
# Non-paragraph approach

for jpg_name in sorted_imagefile_list:
    page_result = ''
    result = reader.readtext(jpg_name, x_ths = 1000)
    for (bbox, text, prob) in result:
        page_result = page_result + text + " "
    file_result = file_result + page_result + "\n"

print (f"PDF file result: {file_result}\n")
'''

# Paragraph approach
for jpg_name in sorted_imagefile_list:
#    print (f"{jpg_name} / {extract_number(jpg_name)}\n")
    page_result = ''

    result = reader.readtext(jpg_name, x_ths = 1000, paragraph = True)
    for (bboxes, text) in result:
        print (f"{text}")
        page_result = page_result + text + "\n"
    file_result = file_result + page_result + "\n"

#print (f"PDF file result: {file_result}\n")

