import cv2 as cv
import numpy as np
from PIL import ImageFilter
from PIL import Image
import os
import PhaseShifting
use_camera=0
use_image=1
load_PhaseShifting=1
load_Gray=0
path=r'image processing\\'
for file_name in os.listdir(path):
    if os.path.isfile(path+file_name):
        os.remove(path+file_name)
if use_camera:
    imageX_name=PhaseShifting.imageX_name
    imageY_name=PhaseShifting.imageY_name
    imageXY_name=PhaseShifting.imageXY_name
elif use_image:
    if load_PhaseShifting:
        last_name='PhaseShifting'
    elif load_Gray:
        last_name='Gray'
    imageX_name='imageX_'+last_name
    imageY_name='imageY_'+last_name
    imageXY_name='imageXY_'+last_name
caption_size=1
imgX=cv.imread(imageX_name+'.png',cv.IMREAD_COLOR)
cv.putText(imgX,'imageX',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
imgY=cv.imread(imageY_name+'.png',cv.IMREAD_COLOR)
cv.putText(imgY,'imageY',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
imgXY=cv.imread(imageXY_name+'.png',cv.IMREAD_GRAYSCALE)
saveXY=cv.cvtColor(imgXY,cv.COLOR_GRAY2BGR)
cv.putText(saveXY,'imageXY',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
final_result=cv.cvtColor(imgXY,cv.COLOR_GRAY2BGR)
cv.imwrite('image processing/1. imageX.png',imgX)
cv.imwrite('image processing/2. imageY.png',imgY)
cv.imwrite('image processing/3. imageXY.png',saveXY)
result=imgXY

global result_filter2D
global result_medianBlur
global result_erode
global result_dilate
global result_threshold
global result_Canny

def main():
    global result
    step={1:smoothen_image,
          2:sharpen_image,
          3:erode_image,
          4:dilate_image,
          5:convert_binary,
          6:detect_edge}
    
    result=step[1](result,4,0)
    result=step[3](result,5,0)
    result=step[4](result,6,0)
    result=step[2](result,7,0)
    result=step[5](result,8,1)
    result=step[6](result,9,1)

    #find contours
    contours=cv.findContours(result.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)[0]
    count_all=0
    perimeter_min=15.0
    perimeter_max=200.0
    prevx,prevy=-1,-1
    for i,contour in enumerate(contours):
        r,g,b=np.random.randint(256),np.random.randint(256),np.random.randint(256)
        perimeter=cv.arcLength(contour,True)
        x,y,w,h=cv.boundingRect(contour)
        #print('x: {}, y: {}'.format(x,y))
        #area=cv.contourArea(contour)
        if count_all:
            cv.rectangle(final_result,(x,y),(x+w,y+h),(b,g,r),2)
            cv.putText(final_result,"p{}".format(i),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
        elif (perimeter>=perimeter_min and perimeter<=perimeter_max) and (x!=prevx or y!=prevy):
            cv.rectangle(final_result,(x,y),(x+w,y+h),(b,g,r),2)
            cv.putText(final_result,"p{}".format(i),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
            prevx,prevy=x,y
            #print('prevx: {}, prevy: {}'.format(prevx,prevy))
    cv.putText(final_result,'final result',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite('image processing/10. final result.png',final_result)

    stitch_r0=np.concatenate((imgX,imgY,saveXY),axis=1)
    stitch_r1=np.concatenate((result_medianBlur,result_erode,result_dilate),axis=1)
    stitch_r2=np.concatenate((result_threshold,result_Canny,final_result),axis=1)
    stitch=np.concatenate((stitch_r0,stitch_r1,stitch_r2),axis=0)
    cv.imwrite('image processing/stitch.png',stitch)

def smoothen_image(result,step,enable):#filter noise
    global result_medianBlur
    result=cv.medianBlur(result,3) if enable else result
    result_medianBlur=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_medianBlur,'medianBlur enabled' if enable else 'medianBlur disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite('image processing/'+str(step)+'. medianBlur.png',result_medianBlur)
    return result

def sharpen_image(result,step,enable):#image sharpening
    global result_filter2D
    kernel=np.array([[-1,-1,-1],
                    [-1,9,-1],
                    [-1,-1,-1]])
    result=cv.filter2D(result,-1,kernel) if enable else result

    # cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    # cv.imwrite('temp.png',result)
    # result=Image.open('temp.png')
    # result=Image.filter(ImageFilter.SHARPEN)

    result_filter2D=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_filter2D,'filter2D enabled' if enable else 'filter2D disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite('image processing/'+str(step)+'. filter2D.png',result_filter2D)
    return result

def erode_image(result,step,enable):#erode
    global result_erode
    result=cv.erode(result,np.ones((3,3),np.uint8)) if enable else result
    #result=cv.erode(result,None,iterations=2) if erode else result
    result_erode=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_erode,'erode enabled' if enable else 'erode disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite('image processing/'+str(step)+'. erode.png',result_erode)
    return result

def dilate_image(result,step,enable):#dilate
    global result_dilate
    result=cv.dilate(result,np.ones((3,3),np.uint8)) if enable else result
    #result=cv.dilate(result,None,iterations=1) if dilate else result
    result_dilate=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_dilate,'dilate enabled' if enable else 'dilate disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite('image processing/'+str(step)+'. dilate.png',result_dilate)
    return result

def convert_binary(result,step,enable):#change to black & white
    global result_threshold
    result=cv.threshold(result,127,255,cv.THRESH_BINARY)[1] if enable else result #85 #128
    result_threshold=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_threshold,'threshold enabled' if enable else 'threshold disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite('image processing/'+str(step)+'. threshold.png',result_threshold)
    return result

def detect_edge(result,step,enable):#edge detection
    global result_Canny
    result=cv.Canny(result,100,200,apertureSize=7) if enable else result #3,5,7
    result_Canny=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_Canny,'Canny enabled' if enable else 'Canny disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite('image processing/'+str(step)+'. Canny.png',result_Canny)
    return result

if __name__=='__main__':
    main()