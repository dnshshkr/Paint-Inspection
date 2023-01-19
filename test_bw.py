import cv2 as cv
img=cv.imread(r'image processing\black\5. morphologicalClosing_1.png',cv.IMREAD_GRAYSCALE)
#img=cv.resize(img,(600,480))
for i in range(256):
    imgb=cv.threshold(img,i,255,cv.THRESH_BINARY)[1]
    imgo=cv.threshold(img,i,255,cv.THRESH_TOZERO)[1]
    cv.putText(imgb,str(i),(5,25),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
    cv.imwrite('binaries/b'+str(i)+'.png',imgb)
    # cv.putText(imgo,str(i),(5,25),cv.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
    # cv.imwrite('tozero/b'+str(i)+'.png',imgo)