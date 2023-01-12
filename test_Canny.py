import cv2 as cv
img=cv.imread('quick test/7. threshold.png',cv.IMREAD_GRAYSCALE)
for i in range(255):
    img_Canny=cv.Canny(img,i,200,apertureSize=7)
    img_Canny_color=cv.cvtColor(img_Canny,cv.COLOR_GRAY2BGR)
    cv.putText(img_Canny_color,str(i),(5,60),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
    cv.imwrite('Canny/C'+str(i)+'.png',img_Canny_color)