import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
img=cv.imread('tozero/b67.png',cv.IMREAD_GRAYSCALE)
# print(len(img))
# with open('test.txt','w') as f:
#     for i in range(len(img)):
#         for j in range(len(img[i])):
#             f.write(str(img[i][j])+' ')
#         print('\n')
highest_diff=0
lowest_diff=255
LOW=0
HIGH=255
img_adjusted=np.zeros((len(img),len(img[0])),np.uint8)
start=time.time()
for i in range(len(img)):
    for j in range(len(img[i])-1):
        diff=abs(img[i][j]-img[i][j+1])
        if diff>highest_diff:
            highest_diff=diff
        if diff<lowest_diff:
            lowest_diff=diff
print(lowest_diff,highest_diff)
LOW=highest_diff
for i in range(len(img)):
    for j in range(len(img[i])-1):
        img_adjusted[i][j]=abs(img[i][j]-img[i][j+1])
cv.imshow('fak',img_adjusted)
cv.waitKey(0)