import PyPDF2
import img2pdf
import os
import sys
import pdf2image
import numpy as np
import cv2
from PIL import Image
from argparse import ArgumentParser

output_image_file = 'output.jpg'
red_removed_file = 'changed.jpeg'
temp_pdf_file = 'temp.pdf'
result_pdf_file = 'output.pdf'


def remove_red_color(file_path):
    ori = cv2.imread(file_path)

    img = ori.copy()
    img = cv2.blur(img, (5, 5))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Range for lower red
    lower_red = np.array([0, 70, 70])
    upper_red = np.array([30, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    # Range for upper range
    lower_red = np.array([160, 70, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    # Generating the final mask to detect red color
    mask = mask1 + mask2
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, 1)
    inv_mask = cv2.bitwise_not(mask)
    print(mask.shape[:2])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ch = cv2.bitwise_and(inv_mask, gray)
    kernel = np.ones((51, 51), np.uint8)
    dilate_ch = cv2.dilate(ch, kernel, 1)
    erode_ch = cv2.erode(dilate_ch, kernel, 1)
    b, g, r = cv2.split(ori)
    result_b = cv2.add(cv2.bitwise_and(b, inv_mask), cv2.bitwise_and(erode_ch, mask))
    result_g = cv2.add(cv2.bitwise_and(g, inv_mask), cv2.bitwise_and(erode_ch, mask))
    result_r = cv2.add(cv2.bitwise_and(r, inv_mask), cv2.bitwise_and(erode_ch, mask))
    result = cv2.merge([result_b, result_g, result_r])
    cv2.imwrite(red_removed_file, result)


def change_image_to_pdf(file_path):
    image1 = Image.open(file_path)
    im1 = image1.convert('RGB')
    im1.save(temp_pdf_file)


def pdf_read(file_path):
    pdf = PyPDF2.PdfFileReader(open(file_path, "rb"))
    return pdf


def delete_temp_files():
    os.remove(output_image_file)
    os.remove(red_removed_file)
    os.remove(temp_pdf_file)


def main(pdf_path):
    images = pdf2image.convert_from_path(pdf_path)
    # num_pages = existing_pdf.numPages
    output = PyPDF2.PdfFileWriter()
    # x = existing_pdf.getNumPages()
    # add all pages from original pdf into output pdf
    i = 0
    for image in images:
        i = i + 1
        print('{} page is processing'.format(str(i)))
        image.save(output_image_file, 'JPEG')
        remove_red_color(output_image_file)
        change_image_to_pdf(red_removed_file)
        temp = pdf_read(temp_pdf_file)
        output.addPage(temp.getPage(0))
        delete_temp_files()
    # finally, write "output" to a real file
    outputStream = open(result_pdf_file, "wb")
    output.write(outputStream)
    outputStream.close()

def build_parser():
    parser = ArgumentParser()

    parser.add_argument('--pdf_path', type=str,
                        dest='pdf_path', help='Original pdf position',
                        metavar='PDF Path', required=True)

    return parser


if __name__ == '__main__':
    parser = build_parser()
    parameter = parser.parse_args()
    main(parameter.pdf_path)
