import cv2
import numpy as np


def morphological(im, operator=min):
    height, width, _ = im.shape
    # create empty image
    out_im = np.zeros((height, width, 3), np.uint8)
    out_im.fill(255)  # fill with white
    for y in range(height):
        for x in range(width):
            try:
                if im[y, x][0] < 10 and im[y, x][1] < 255 and im[y, x][1] > 70 and im[y, x][2] < 255 and im[y, x][2] > 70:
                    # nlst = neighbours(im, y, x)
                    #
                    # out_im[y, x] = operator(nlst, key=lambda x: np.mean(x))
                    out_im[y, x] = 0
                else:
                    out_im[y, x] = im[y, x]
            except Exception as e:
                print(e)
    return out_im


def neighbours(pix, y, x):
    nlst = []
    # search pixels around im[y,x] add them to nlst
    for yy in range(y - 1, y + 1):
        for xx in range(x - 1, x + 1):
            try:
                nlst.append(pix[yy, xx])
            except:
                pass
    return np.array(nlst)

img = cv2.imread("out.jpg")
img1 = morphological(img, max)
img2 = morphological(img, min)
cv2.imwrite("test2.jpg", img2)
