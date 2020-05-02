import cv2
import numpy as np
img = cv2.imread("out.jpg")
# cv2.imwrite("result1.jpg", img)
# img_h, img_w, c = img.shape
# Convert BGR to HSV
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
img_h, img_w, chanel = img.shape


flt_h = 50
flt_w = 1

for j in range(img_h - flt_h):
    for i in range(img_w - flt_w):
        tmp = mask[j:j+flt_h, i:i+flt_w]
        if np.sum(tmp) != 0:
            top_v = tmp[0, 0]
            bottom_v = tmp[-1, 0]
            if top_v == bottom_v == 0:
                img[j:j+flt_h, i:i+flt_w] = img[j, i]
cv2.imwrite("result1.jpg", img)
# cv2.waitKey(0)
