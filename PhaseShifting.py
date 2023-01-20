"""
Capture projection pattern and decode x-coorde.
"""
import cv2 as cv
import numpy as np
import structuredlight as sl
import screeninfo
from matplotlib import pyplot as plt
import basler
import time
firstTimeRun=0
if firstTimeRun:
    basler.Basler.parameterizeCamera()
screen_id=3
def imshowAndCapture(cap,img_pattern,winf,winc,delay=250):
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
    num:int=5
    F:float=35
    F1=F
    F2=float(F)*aspect_ratio

    #generate x pattern
    phaseshiftingX=sl.PhaseShifting(num,F1)
    imlist_patternX=phaseshiftingX.generate((width,height))
    #imlist_nega_x_pat=[cv.rotate(img,cv.ROTATE_180) for img in imlist_posi_x_pat]
    #imlist_posi_x_pat.extend(imlist_nega_x_pat)

    #generate y pattern
    phaseshiftingY=sl.PhaseShifting(num,F2)
    imlist_patternY=sl.transpose(phaseshiftingY.generate((width, height)))
    #imlist_nega_y_pat=[cv.rotate(img,cv.ROTATE_180) for img in imlist_posi_y_pat]
    #imlist_posi_y_pat.extend(imlist_nega_y_pat)

    #pattern projection screen
    fringe_window='projector'
    cv.namedWindow(fringe_window,cv.WND_PROP_FULLSCREEN)
    cv.moveWindow(fringe_window,screen.x-1,screen.y-1)
    cv.setWindowProperty(fringe_window,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

    capture_window='capture'
    cv.namedWindow(capture_window,cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty(capture_window,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    cv.moveWindow(capture_window,0,0)
    
    # Capture
    imlist_capturesX=[imshowAndCapture(cap,img,fringe_window,capture_window) for img in imlist_patternX]
    #cv.imwrite(save_path+'/rawX_'+specified+'.png',imlist_capturesX[np.random.randint(len(imlist_capturesX))])

    # DecodeX
    imgX=sl.PhaseShifting().decodeAmplitude(imlist_capturesX)

    # Capture
    imlist_capturesY=[imshowAndCapture(cap,img,fringe_window,capture_window) for img in imlist_patternY]
    #cv.imwrite(save_path+'/rawY_'+specified+'.png',imlist_capturesY[np.random.randint(len(imlist_capturesY))])

    # DecodeY
    imgY=sl.PhaseShifting().decodeAmplitude(imlist_capturesY)

    # Close camera
    cap.end()

    # Delete unused variables
    del num,F,F1,F2,imlist_patternX,imlist_capturesX,imlist_patternY,imlist_capturesY

    # Visualize decode result
    width,height=1000,100#960,102
    #img_correspondence=cv.addWeighted(imgX,0.5,imgY,0.5,0)
    img_correspondence=cv.merge([0.0*np.zeros_like(imgX),imgX/width,imgY/height])
    #img_correspondence=cv.merge([img_correspondence,imgX/width,imgY/height])
    
    img_correspondence=np.clip(img_correspondence*255.0,0,255).astype(np.uint8)
    img_correspondence=cv.cvtColor(img_correspondence,cv.COLOR_BGR2GRAY)
    
    cv.destroyAllWindows()
    specified=input('enter specific name for the part: ')
    imageX_name='imageX_PhaseShifting_'+specified
    imageY_name='imageY_PhaseShifting_'+specified
    imageXY_name='imageXY_PhaseShifting_'+specified
    save_path='image processing/'+specified
    plt.imsave(imageX_name+'.png',imgX,cmap='gray')
    plt.imsave(imageY_name+'.png',imgY,cmap='gray')
    plt.imsave(imageXY_name+'.png',img_correspondence,cmap='gray')
if __name__=="__main__":
    main()