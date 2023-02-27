"""
Capture projection pattern and decode x-coorde.
"""
import cv2 as cv
import numpy as np
import structuredlight as sl
import screeninfo
from matplotlib import pyplot as plt
import basler
import os.path
import time
firstTimeRun=0
if firstTimeRun:
    basler.Basler.parameterizeCamera()
screen_id=1
def imshowAndCapture(cap,img_pattern,winf,winc,delay=100):
    cv.imshow(winf,img_pattern)
    cv.waitKey(delay)
    img_gray=cap.retrieve()
    cv.imshow(winc,img_gray)
    if cv.waitKey(1)==27 or cv.getWindowProperty(winf,cv.WND_PROP_VISIBLE)<1:
        cap.end()
        cv.destroyAllWindows()
        exit()
    return img_gray
def main():
    try:
        screen=screeninfo.get_monitors()[screen_id-1] #get the size of the screen
        width,height=screen.width,screen.height
        aspect_ratio:float=height/width
    except:
        print('Monitor not detected')
        exit()
    try:
        cap=basler.Basler(mode=basler.MODE_CAPTURE,image_size=(1920,1080),rotate_image=180) #initialize camera
    except:
        cap=cv.VideoCapture(1) #webcam
        cap.open
    num:int=4
    F:float=40 #70 for silver 23 for white 35 others
    F1=F
    F2=float(F)*aspect_ratio
    is_white=0
    is_silver=0
    # if is_silver:
    #     F1=23
    #     F2=0.5
    # if is_white:
    #     F1=35
    #     F2=0.5
    #generate x pattern
    phaseshiftingX=sl.PhaseShifting(num,F1)
    imlist_patternX=phaseshiftingX.generate((width,height))

    #generate y pattern
    phaseshiftingY=sl.PhaseShifting(num,F2)
    imlist_patternY=sl.transpose(phaseshiftingY.generate((width, height)))

    #pattern projection screen
    fringe_window='projector'
    cv.namedWindow(fringe_window,cv.WND_PROP_FULLSCREEN)
    cv.moveWindow(fringe_window,screen.x-1,screen.y-1)
    cv.setWindowProperty(fringe_window,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

    capture_window='capture'
    cv.namedWindow(capture_window,cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty(capture_window,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    cv.moveWindow(capture_window,0,0)
    
    # CaptureX
    timeX_start=timeXY_start=time.time()
    imlist_capturesX=[imshowAndCapture(cap,img,fringe_window,capture_window) for img in imlist_patternX]

    # DecodeX
    imgX=phaseshiftingX.decodeAmplitude(imlist_capturesX)
    if is_silver:
        imgX=cv.convertScaleAbs(imgX,alpha=1.5,beta=10)
        imgX=cv.addWeighted(imgX,5,imgX,0,2)
        # imgX=cv.convertScaleAbs(imgX,alpha=127.0/np.max(imgX))
        # imgX=cv.addWeighted(imgX,0.5,imgX,0.5,0)
    timeX_end=time.time()-timeX_start
    print(f'timeX: {timeX_end*1000} ms')

    # CaptureY
    timeY_start=time.time()
    imlist_capturesY=[imshowAndCapture(cap,img,fringe_window,capture_window) for img in imlist_patternY]

    # DecodeY
    imgY=phaseshiftingY.decodeAmplitude(imlist_capturesY)
    if is_silver:
        imgY=cv.convertScaleAbs(imgY,alpha=1.5,beta=10)
        imgY=cv.addWeighted(imgY,5,imgY,0,2)
        # imgY=cv.convertScaleAbs(imgY,alpha=127.0/np.max(imgY))
        # imgY=cv.addWeighted(imgY,0.5,imgY,0.5,0)
    timeY_end=time.time()-timeY_start
    print(f'timeY: {timeY_end*1000} ms')

    # Close camera
    cap.end()

    # Delete unused variables
    del imlist_patternX,imlist_capturesX,imlist_patternY,imlist_capturesY

    # Visualize decode result
    width,height=1000,100#960,102
    #img_correspondence=cv.addWeighted(imgX,0.5,imgY,0.5,0)
    img_correspondence=cv.merge([0.0*np.zeros_like(imgX),imgX/width,imgY/height])
    #img_correspondence=cv.merge([img_correspondence,imgX/width,imgY/height])
    
    img_correspondence=np.clip(img_correspondence*255.0,0,255).astype(np.uint8)
    img_correspondence=cv.cvtColor(img_correspondence,cv.COLOR_BGR2GRAY)
    timeXY_end=time.time()-timeXY_start
    print(f'timeXY: {timeXY_end*1000} ms')
    
    cv.destroyAllWindows()
    algorithm='PhaseShifting'
    folder=f'captures/{algorithm}/'
    algorithm+='_'
    specified=input('enter specific name for the part: ')
    #specified='demo_red'
    imageX_name='imageX_PhaseShifting_'
    imageY_name='imageY_PhaseShifting_'
    imageXY_name='imageXY_PhaseShifting_'
    save_pathX=folder+imageX_name+specified+'_F1-'+str(F1)+'_N'+str(num)
    save_pathY=folder+imageY_name+specified+'_F2-'+str(F2)+'_N'+str(num)
    save_pathXY=folder+imageXY_name+specified+'_F1-'+str(F1)+'_F2-'+str(F2)+'_N'+str(num)
    while os.path.exists(save_pathX+'.png') or os.path.exists(save_pathY+'.png') or os.path.exists(save_pathXY+'.png'):
        decision=input('the file already exists, do you want to overwrite it? (y/n): ')
        if decision=='y':
            break
        else:
            specified=input('please enter another name: ')
    plt.imsave(save_pathX+'.png',imgX,cmap='gray')
    plt.imsave(save_pathY+'.png',imgY,cmap='gray')
    plt.imsave(save_pathXY+'.png',img_correspondence,cmap='gray')
    img_correspondence=cv.imread(save_pathXY+'.png',cv.IMREAD_GRAYSCALE)
    # if is_silver:
    #     img_correspondence=cv.GaussianBlur(img_correspondence,(5,5),0)
    #     thresh = cv.adaptiveThreshold(img_correspondence, 65, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)

    #     # Find contours in the thresholded image
    #     contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #     img_correspondence=cv.cvtColor(img_correspondence,cv.COLOR_GRAY2BGR)
    #     # Draw contours around the bright areas
    #     cv.drawContours(img_correspondence, contours, -1, (0, 255, 0), 3)
    cv.imshow('demo',img_correspondence)
    cv.setWindowProperty('demo',cv.WND_PROP_AUTOSIZE,cv.WINDOW_NORMAL)
    cv.waitKey(0)
if __name__=="__main__":
    main()