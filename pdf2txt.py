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

reader = easyocr.Reader(['en'])
#reader = easyocr.Reader(['de','en', 'pt'])
erlaubtezeichen = string.ascii_letters+string.digits
from pdf2jpg import pdf2jpg
wrapper = textwrap.TextWrapper(width=70)

def pdf_auslesen(inputpath, outputpath, pages='ALL'):
    result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, dpi=300, pages=pages)
    return result


# Main
print('PDF to TXT written by Jonathan Germain / github.com/compilebunny')
print('Thanks to\nhttps://github.com/JaidedAI/EasyOCR\nhttps://github.com/pankajr141/pdf2jpg\nJohannes Fischer www.queroestudaralemao.com.br\n\nfor 99% of the work')
#suffix, inputpath = datei_auswaehlen() -- we're not using a gui here. Do it in text instead.

if len(sys.argv) < 2:
    print('syntax: pdf2txt <file.pdf>')
    sys.exit(1)

file_path = sys.argv[1]

#file_path = input("Please enter the file path: ")
# Extract directory name
directory_name = os.path.dirname(file_path)
# Extract base name (file name with extension)
base_name = os.path.basename(file_path)
inputpath = directory_name+'/'+base_name
# Split base name into file name and extension
droppath, suffix = os.path.splitext(file_path)

print(f"Directory Name: {directory_name}")
print(f"Base Name: {base_name}")
print(f"inputpath: {inputpath}")
print(f"Extension: {suffix}")

bigjpg = pdf_auslesen(inputpath, '/tmp/test', pages='ALL')

#print (f"bigjpg: {bigjpg} / type {type(bigjpg)}")

#for jpg_name in bigjpg.output_jpgfiles:
'''
# Non-paragraph approach

for jpg_name in bigjpg[0]['output_jpgfiles']:
    page_result = ''
#    print (f"analyze {jpg_name}")


    result = reader.readtext(jpg_name, x_ths = 1000)
    for (bbox, text, prob) in result:
#        print (f"{text}")
#        junk = input("analyze")
        page_result = page_result + text + " "
#    print (f"page text: {page_result}\n")
    file_result = file_result + page_result + "\n"

print (f"PDF file result: {file_result}\n")
'''

# Paragraph approach
for jpg_name in bigjpg[0]['output_jpgfiles']:
    page_result = ''

    result = reader.readtext(jpg_name, x_ths = 1000, paragraph = True)
#    result = reader.readtext(jpg_name, x_ths = 1000)
#    print (f"Result type: {type(result)}")
#    for (bbox, text, prob) in result:
    for (bboxes, text) in result:
        print (f"{text}")
#        junk = input("analyze")


        page_result = page_result + text + "\n"


#    print (f"page text: {page_result}\n")
#    file_result = file_result + page_result + ' '
    file_result = file_result + page_result + "\n"

#print (f"PDF file result: {file_result}\n")

