"""
Capture projection pattern and decode x-coorde.
"""
import cv2 as cv
import numpy as np
import structuredlight as sl
import screeninfo
from matplotlib import pyplot as plt
import basler
firstTimeRun=0
if firstTimeRun:
    basler.Basler.parameterizeCamera()
screen_id=2
specified='black'
imageX_name='imageX_PhaseShifting_'+specified
imageY_name='imageY_PhaseShifting_'+specified
imageXY_name='imageXY_PhaseShifting_'+specified
save_path='image processing/'+specified
def imshowAndCapture(cap,img_pattern,delay=100):
    window_name='projector'
    cv.imshow(window_name, img_pattern)
    cv.waitKey(delay)
    img_gray=cap.retrieve()
    cv.imshow("img_gray",img_gray)
    #cv.waitKey(delay)
    return img_gray
def main():
    try:
        screen=screeninfo.get_monitors()[screen_id] #get the size of the screen
        width,height=screen.width, screen.height
    except:
        print('Monitor not detected')
        exit()
    try:
        cap=basler.Basler(image_size=(1920,1080),rotate_image=180) #initialize camera
    except:
        cap=cv.VideoCapture(1) #webcam
        cap.open
    num:int=7
    F:int=10 #35
    F1=F
    F2=int(float(F)*9.0/16.0)

    #generate x pattern
    phaseshiftingX=sl.PhaseShifting(num,F1)
    imlist_patternX=phaseshiftingX.generate((width,height))
    #imlist_nega_x_pat=[cv.rotate(img,cv.ROTATE_180) for img in imlist_posi_x_pat]
    #imlist_posi_x_pat.extend(imlist_nega_x_pat)

    #generate y pattern
    phaseshiftingY=sl.PhaseShifting(num,F2)
    imlist=phaseshiftingY.generate((width, height))
    imlist_patternY=sl.transpose(imlist)
    #imlist_nega_y_pat=[cv.rotate(img,cv.ROTATE_180) for img in imlist_posi_y_pat]
    #imlist_posi_y_pat.extend(imlist_nega_y_pat)

    #pattern projection screen
    window_name='projector'
    cv.namedWindow(window_name,cv.WND_PROP_FULLSCREEN)
    cv.moveWindow(window_name,screen.x-1,screen.y-1)
    cv.setWindowProperty(window_name,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

    cv.namedWindow("img_gray",cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty("img_gray",cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)
    cv.moveWindow("img_gray",0,0)
    # Capture
    imlist_capturesX=[imshowAndCapture(cap,img) for img in imlist_patternX]
    cv.imwrite(save_path+'/rawX_'+specified+'.png',imlist_capturesX[np.random.randint(len(imlist_capturesX))])

    # DecodeX
    imgX=sl.PhaseShifting().decodeAmplitude(imlist_capturesX)
    plt.imsave(imageX_name+'.png',imgX,cmap='gray')

    # Capture
    imlist_capturesY=[imshowAndCapture(cap,img) for img in imlist_patternY]
    cv.imwrite(save_path+'/rawY_'+specified+'.png',imlist_capturesY[np.random.randint(len(imlist_capturesY))])

    # DecodeY
    imgY = sl.PhaseShifting().decodeAmplitude(imlist_capturesY)
    plt.imsave(imageY_name+'.png',imgY,cmap='gray')

    # Close camera
    cap.end()

    # Delete unused variables
    del num,F,F1,F2,imlist,imlist_patternX,imlist_capturesX,imlist_patternY,imlist_capturesY

    # Visualize decode result
    img_correspondence=cv.merge([0.0*np.zeros_like(imgX),imgX/width,imgY/height])
    del imgX,imgY
    
    img_correspondence=np.clip(img_correspondence*255.0,0,255).astype(np.uint8)
    img_correspondence=cv.cvtColor(img_correspondence,cv.COLOR_RGB2GRAY)
    plt.imsave(imageXY_name+'.png',img_correspondence,cmap='gray')
    cv.destroyAllWindows()

if __name__=="__main__":
    main()