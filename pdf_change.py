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
    # load image
    frame = cv2.imread(file_path)
    # frame = cv2.resize(frame, (800, 600))
    frame_blur = cv2.blur(frame, (5, 5))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
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
    # cv2.imshow("mask image", cv2.resize(mask, (800, 600)))
    # cv2.waitKey()
    gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
    ch = cv2.bitwise_and(inv_mask, gray)
    # cv2.imshow("mask image", cv2.resize(ch, (800, 600)))
    # cv2.waitKey()
    kernel = np.ones((51, 51), np.uint8)
    dilate_ch = cv2.dilate(ch, kernel, 1)
    erode_ch = cv2.erode(dilate_ch, kernel, 1)
    # cv2.imshow("erode image", erode_ch)
    # cv2.waitKey()

    ch_bgr = cv2.cvtColor(erode_ch, cv2.COLOR_GRAY2BGR)
    # cv2.imshow("ch bgr", ch_bgr)
    # cv2.waitKey()

    # mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # cv2.imshow("mask bgr", mask_bgr)
    # cv2.waitKey()
    red_contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_outside_colors = []
    cnt_frame = frame.copy()
    for cnt in red_contours:
        cnt_box = cv2.boundingRect(cnt)
        x, y, w, h = cnt_box
        roi_ch = ch_bgr[y:y + h, x:x + w]
        roi_b, roi_g, roi_r = cv2.split(roi_ch)
        outside_b = np.mean(roi_b)
        outside_g = np.mean(roi_g)
        outside_r = np.mean(roi_r)
        cv2.drawContours(cnt_frame, [cnt], 0, (outside_b, outside_g, outside_r), -1)
        red_outside_colors.append([int(outside_b), int(outside_g), int(outside_r)])
    cv2.imwrite(red_removed_file, cnt_frame)


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
