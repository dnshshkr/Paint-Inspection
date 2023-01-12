import cv2 as cv
import numpy as np
import os
use_camera=1
use_image=0
path=r'image processing\white\\'
for file_name in os.listdir(path):
    if os.path.isfile(path+file_name):
        os.remove(path+file_name)
last_name='PhaseShifting_white'
imageX_name='imageX_'+last_name
imageY_name='imageY_'+last_name
imageXY_name='imageXY_'+last_name
caption_size=1
imgX=cv.imread(imageX_name+'.png',cv.IMREAD_COLOR)
imgY=cv.imread(imageY_name+'.png',cv.IMREAD_COLOR)
imgXY=cv.imread(imageXY_name+'.png',cv.IMREAD_COLOR)

final_result=imgXY.copy()
result=cv.cvtColor(final_result,cv.COLOR_BGR2GRAY)

cv.putText(imgX,'imageX',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
cv.putText(imgY,'imageY',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
cv.putText(imgXY,'imageXY',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
cv.imwrite(path+'1. imageX.png',imgX)
cv.imwrite(path+'2. imageY.png',imgY)
cv.imwrite(path+'3. imageXY.png',imgXY)

def process():
    main()
def main():
    global result
    process={1:smoothen_image,
             2:sharpen_image,
             3:erode_image,
             4:dilate_image,
             5:convert_binary,
             6:detect_edge}
    
    stitch_image_array=[]
    result,stitch=process[1](result,4,1)
    stitch_image_array.append(stitch)
    result,stitch=process[3](result,5,1)
    stitch_image_array.append(stitch)
    result,stitch=process[4](result,6,1)
    stitch_image_array.append(stitch)
    result,stitch=process[2](result,7,0)
    stitch_image_array.append(stitch)
    result,stitch=process[5](result,8,1)
    stitch_image_array.append(stitch)
    result,stitch=process[6](result,9,0)
    stitch_image_array.append(stitch)

    #find contours
    contours=cv.findContours(result.copy(),cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]
    contourImage=np.zeros((len(final_result),len(final_result[0]),3),np.uint8)
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
            cv.putText(final_result,"p{:.1f}".format(perimeter),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
            cv.drawContours(contourImage,[contour],0,(b,g,r),1)
            cv.putText(contourImage,"p{}".format(i),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
        elif (perimeter>=perimeter_min and perimeter<=perimeter_max) and (x!=prevx or y!=prevy):
            cv.rectangle(final_result,(x,y),(x+w,y+h),(b,g,r),2)
            cv.putText(final_result,"p{:.1f}".format(perimeter),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
            prevx,prevy=x,y
            cv.drawContours(contourImage,[contour],0,(b,g,r),1)
            cv.putText(contourImage,"p{}".format(i),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
    cv.putText(contourImage,'contours',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(path+'10. contours.png',contourImage)
    cv.putText(final_result,'final result',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(path+'11. final result.png',final_result)

    stitch_r0=np.concatenate((imgX,imgY,imgXY),axis=1)
    stitch_r1=np.concatenate((stitch_image_array[0],stitch_image_array[1],stitch_image_array[2]),axis=1)
    stitch_r2=np.concatenate((stitch_image_array[3],stitch_image_array[4],stitch_image_array[5]),axis=1)
    stitch_r3=np.concatenate((contourImage,final_result,np.zeros((1080,1920,3),np.uint8)),axis=1)
    stitch=np.concatenate((stitch_r0,stitch_r1,stitch_r2,stitch_r3),axis=0)
    cv.imwrite(path+'stitch.png',stitch)

def smoothen_image(result,step,enable):#filter noise
    result=cv.medianBlur(result,3) if enable else result
    result_medianBlur=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_medianBlur,'medianBlur enabled' if enable else 'medianBlur disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(path+str(step)+'. medianBlur.png',result_medianBlur)
    return result,result_medianBlur

def sharpen_image(result,step,enable):#image sharpening
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
    cv.imwrite(path+str(step)+'. filter2D.png',result_filter2D)
    return result,result_filter2D

def erode_image(result,step,enable):#erode
    result=cv.erode(result,np.ones((6,6),np.uint8)) if enable else result
    #result=cv.erode(result,None,iterations=2) if erode else result
    result_erode=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_erode,'erode enabled' if enable else 'erode disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(path+str(step)+'. erode.png',result_erode)
    return result,result_erode

def dilate_image(result,step,enable):#dilate
    result=cv.dilate(result,np.ones((5,5),np.uint8)) if enable else result
    #result=cv.dilate(result,None,iterations=1) if dilate else result
    result_dilate=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_dilate,'dilate enabled' if enable else 'dilate disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(path+str(step)+'. dilate.png',result_dilate)
    return result,result_dilate

def convert_binary(result,step,enable):#change to black & white
    result=cv.threshold(result,170,255,cv.THRESH_BINARY)[1] if enable else result #85 #128 #170
    result_threshold=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_threshold,'threshold enabled' if enable else 'threshold disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(path+str(step)+'. threshold.png',result_threshold)
    return result,result_threshold

def detect_edge(result,step,enable):#edge detection
    result=cv.Canny(result,100,200,apertureSize=7) if enable else result #3,5,7
    result_Canny=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_Canny,'Canny enabled' if enable else 'Canny disabled',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(path+str(step)+'. Canny.png',result_Canny)
    return result,result_Canny

if __name__=='__main__':
    main()