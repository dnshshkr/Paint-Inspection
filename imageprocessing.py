import cv2 as cv
import numpy as np
import os
use_camera=1
use_image=0
folder_name='red'
part_name='_'+folder_name
save_path='image processing/'+folder_name+'/'

imageX_name='image processing/red/1. imageX'
imageY_name='image processing/red/2. imageY'
imageXY_name='image processing/red/3. imageXY'
caption_size=1

#load image
try:
    imgX=cv.imread(imageX_name+'.png',cv.IMREAD_COLOR)
    imgY=cv.imread(imageY_name+'.png',cv.IMREAD_COLOR)
except:
    pass
imgXY=cv.imread(imageXY_name+'.png',cv.IMREAD_COLOR)

final_result=imgXY.copy()
result=cv.cvtColor(final_result,cv.COLOR_BGR2GRAY)

for file_name in os.listdir(save_path):
    if os.path.isfile(save_path+file_name):
        os.remove(save_path+file_name)

#save path
try:
    cv.putText(imgX,'imageX',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.putText(imgY,'imageY',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
except:
    pass
cv.putText(imgXY,'imageXY',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
try:
    cv.imwrite(save_path+'1. imageX.png',imgX)
    cv.imwrite(save_path+'2. imageY.png',imgY)
except:
    pass
cv.imwrite(save_path+'3. imageXY.png',imgXY)

def process():
    main()
def main():
    global result
    process={1:smoothen_image,
             2:sharpen_image,
             3:equalize_background,
             4:morphology,
             5:erode_image,
             6:dilate_image,
             7:laplacian,
             8:convert_binary,
             9:detect_edge}
    
    stitch_image_array=[]
    result,stitch=process[1](result,4,0)
    stitch_image_array.append(stitch)
    result,stitch=process[3](result,5,0)
    stitch_image_array.append(stitch)
    result,stitch=process[4](result,6,1)
    stitch_image_array.append(stitch)
    result,stitch=process[2](result,7,0)
    stitch_image_array.append(stitch)
    result,stitch=process[5](result,8,0)
    stitch_image_array.append(stitch)
    result,stitch=process[6](result,9,0)
    stitch_image_array.append(stitch)
    result,stitch=process[7](result,10,0)
    stitch_image_array.append(stitch)
    result,stitch=process[8](result,11,1)
    stitch_image_array.append(stitch)
    result,stitch=process[9](result,11,0)
    stitch_image_array.append(stitch)

    index=13
    #find contours
    contours=cv.findContours(result.copy(),cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]
    contourImage=np.zeros((len(final_result),len(final_result[0]),3),np.uint8)
    count_all=1
    contour_label=0
    contour_box=0
    overlay_contours=1
    perimeter_min=8.0
    perimeter_max=200.0
    prevx,prevy=-1,-1
    for i,contour in enumerate(contours):
        r,g,b=np.random.randint(256),np.random.randint(256),np.random.randint(256)
        perimeter=cv.arcLength(contour,True)
        x,y,w,h=cv.boundingRect(contour)
        #print('x: {}, y: {}'.format(x,y))
        #area=cv.contourArea(contour)
        if count_all:
            if contour_box:
                cv.rectangle(final_result,(x,y),(x+w,y+h),(b,g,r),2)
            if contour_label:
                cv.putText(final_result,"p{:.1f}".format(perimeter),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
            cv.drawContours(contourImage,[contour],0,(b,g,r),1)
            if overlay_contours:
                cv.drawContours(final_result,[contour],0,(b,g,r),1)
            if contour_label:
                cv.putText(contourImage,"p{}".format(i),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
        elif not count_all and (perimeter>=perimeter_min and perimeter<=perimeter_max) and (x!=prevx or y!=prevy):
            if contour_box:
                cv.rectangle(final_result,(x,y),(x+w,y+h),(b,g,r),2)
            if contour_label:
                cv.putText(final_result,"p{:.1f}".format(perimeter),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
            cv.drawContours(contourImage,[contour],0,(b,g,r),1)
            if overlay_contours:
                cv.drawContours(final_result,[contour],0,(b,g,r),1)
            if contour_label:
                cv.putText(contourImage,"p{}".format(i),(x,y-7),cv.FONT_HERSHEY_SIMPLEX,0.6,(b,g,r),2)
            prevx,prevy=x,y
    cv.putText(contourImage,'contours',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(index)+'. contours.png',contourImage)
    index+=1
    cv.putText(final_result,'final result',(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(index)+'. final result.png',final_result)

    stitch_r0=np.concatenate((imgX,imgY,imgXY),axis=1)
    stitch_r1=np.concatenate((stitch_image_array[0],stitch_image_array[1],stitch_image_array[2]),axis=1)
    stitch_r2=np.concatenate((stitch_image_array[3],stitch_image_array[4],stitch_image_array[5]),axis=1)
    stitch_r3=np.concatenate((stitch_image_array[6],contourImage,final_result),axis=1)
    stitch=np.concatenate((stitch_r0,stitch_r1,stitch_r2,stitch_r3),axis=0)
    cv.imwrite(save_path+'stitch.png',stitch)

def smoothen_image(result,step,enable):#filter noise
    result=cv.medianBlur(result,3) if enable else result
    #result=cv.blur(result,(9,9),0) if enable else result
    result_medianBlur=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_medianBlur,'medianBlur '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. medianBlur_'+str(enable)+'.png',result_medianBlur)
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
    cv.putText(result_filter2D,'filter2D '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. filter2D_'+str(enable)+'.png',result_filter2D)
    return result,result_filter2D

def equalize_background(result,step,enable):
    if enable:
        ycrcb=cv.cvtColor(cv.cvtColor(result,cv.COLOR_GRAY2BGR),cv.COLOR_BGR2YCrCb)
        y,cr,cb=cv.split(ycrcb)
        y_eq=cv.equalizeHist(y)
        ycrcb_eq=cv.merge((y_eq,cr,cb))
        result=cv.cvtColor(cv.cvtColor(ycrcb_eq,cv.COLOR_YCrCb2BGR),cv.COLOR_BGR2GRAY)
    result_equalizeBackground=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_equalizeBackground,'equalize background '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. equalizeBackground_'+str(enable)+'.png',result_equalizeBackground)
    return result,result_equalizeBackground

def morphology(result,step,enable):
    kernel=np.ones((5,5),np.uint8)
    if enable:
        closing=cv.morphologyEx(result,cv.MORPH_CLOSE,kernel)
    result=cv.absdiff(result,closing) if enable else result
    result_morphologicalClosing=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_morphologicalClosing,'morphological closing '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. morphologicalClosing_'+str(enable)+'.png',result_morphologicalClosing)
    return result,result_morphologicalClosing

def erode_image(result,step,enable):#erode
    #result=cv.erode(result,np.ones((6,6),np.uint8)) if enable else result
    result=cv.erode(result,None,iterations=2) if enable else result
    result_erode=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_erode,'erode '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. erode_'+str(enable)+'.png',result_erode)
    return result,result_erode

def dilate_image(result,step,enable):#dilate
    #result=cv.dilate(result,np.ones((5,5),np.uint8)) if enable else result
    result=cv.dilate(result,None,iterations=1) if enable else result
    result_dilate=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_dilate,'dilate '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. dilate_'+str(enable)+'.png',result_dilate)
    return result,result_dilate

def laplacian(result,step,enable):#laplacian
    result=cv.Laplacian(result,cv.CV_8U) if enable else result
    result_laplacian=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_laplacian,'Laplacian '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. Laplacian_'+str(enable)+'.png',result_laplacian)
    return result,result_laplacian

def convert_binary(result,step,enable):#change to black & white
    result=cv.threshold(result,20,255,cv.THRESH_BINARY)[1] if enable else result #85 #128 #170
    result_threshold=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_threshold,'threshold '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. threshold_'+str(enable)+'.png',result_threshold)
    return result,result_threshold

def detect_edge(result,step,enable):#edge detection
    result=cv.Canny(result,100,200,apertureSize=7) if enable else result #3,5,7
    result_Canny=cv.cvtColor(result,cv.COLOR_GRAY2BGR)
    cv.putText(result_Canny,'Canny '+('enabled' if enable else 'disabled'),(5,30),cv.FONT_HERSHEY_SIMPLEX,caption_size,(0,0,255),2)
    cv.imwrite(save_path+str(step)+'. Canny_'+str(enable)+'.png',result_Canny)
    return result,result_Canny

if __name__=='__main__':
    main()