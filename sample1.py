import numpy as np
import cv2

# load image
ori = cv2.imread("out.jpg")
ori_gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)

img = ori.copy()
img = cv2.blur(img, (5, 5))
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

kernel = np.ones((3, 3), np.uint8)
mask = cv2.dilate(mask, kernel, 1)
inv_mask = cv2.bitwise_not(mask)

# cv2.imshow("mask", cv2.resize(mask, None, fx=0.3, fy=0.3))
print(mask.shape[:2])
# cv2.imshow("inv mask", inv_mask)
# cv2.waitKey()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ch = cv2.bitwise_and(inv_mask, gray)
kernel = np.ones((51, 51), np.uint8)
dilate_ch = cv2.dilate(ch, kernel, 1)
# cv2.imshow("dilate_ch", dilate_ch)
# cv2.waitKey()
erode_ch = cv2.erode(dilate_ch, kernel, 1)
cv2.imshow("erode_ch", erode_ch)
cv2.waitKey()
cv2.imshow("ha", cv2.bitwise_and(ori_gray, inv_mask))
cv2.waitKey()
result_ch = cv2.add(cv2.bitwise_and(ori_gray, inv_mask), cv2.bitwise_and(erode_ch, mask))

# cv2.imshow("ori", cv2.resize(ori, None, fx=0.3, fy=0.3))
# cv2.imshow("mask", cv2.resize(mask, None, fx=0.3, fy=0.3))
# cv2.imshow("erode_ch", cv2.resize(erode_ch, None, fx=0.3, fy=0.3))
# cv2.imshow("result", cv2.resize(result_ch, None, fx=0.3, fy=0.3))

cv2.waitKey(0)
img = cv2.blur(result_ch, (5, 5))
cv2.imwrite("result2.jpg", result_ch)
