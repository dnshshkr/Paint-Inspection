import numpy as np
import cv2 as cv
img=np.zeros((400,400),np.uint8)
for i in range(256):
    for j in range(400):
        for k in range(400):
            img[j][k]=i
    cv.imwrite('pixel brightness/pix'+str(i)+'.png',img)