import cv2
import test as np

#read image
src = cv2.imread('out.jpg', cv2.IMREAD_UNCHANGED)
print(src.shape)

# assign red channel to zeros
src[:,:,2] = np.zeros([src.shape[0], src.shape[1]])

#save image
cv2.imwrite('result.jpg', src)
