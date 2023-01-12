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
specified='_white'
imageX_name='imageX_PhaseShifting'+specified
imageY_name='imageY_PhaseShifting'+specified
imageXY_name='imageXY_PhaseShifting'+specified

def imshowAndCapture(cap, img_pattern, delay=400):
    window_name='projector'
    cv.imshow(window_name, img_pattern)
    cv.waitKey(delay)
    img_gray=cap.capture()
    cv.namedWindow("img_gray", cv.WND_PROP_FULLSCREEN)
    cv.setWindowProperty("img_gray", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.imshow("img_gray", img_gray)
    cv.moveWindow("img_gray",0,0)
    return img_gray

def main():
    # get the size of the screen
    try:
        screen=screeninfo.get_monitors()[screen_id]
        width,height=screen.width, screen.height
    except:
        print('Monitor not detected')
        exit()
    try:
        cap=basler.Basler(image_size=(1920,1080),rotate_image=180)
    except:
        cap=cv.VideoCapture(1) # External web camera
        cap.open
    num:int=5
    F:int=5 #35num
    F1=F
    F2=int(float(F)*9.0/16.0)

    #generate x pattern
    phaseshiftingX=sl.PhaseShifting(num,F1)
    imlist_posi_x_pat=phaseshiftingX.generate((width,height))
    #imlist_nega_x_pat=[cv.rotate(img,cv.ROTATE_180) for img in imlist_posi_x_pat]
    #imlist_posi_x_pat.extend(imlist_nega_x_pat)

    #generate y pattern
    phaseshiftingY=sl.PhaseShifting(num,F2)
    imlist=phaseshiftingY.generate((width, height))
    imlist_posi_y_pat=sl.transpose(imlist)
    #imlist_nega_y_pat=[cv.rotate(img,cv.ROTATE_180) for img in imlist_posi_y_pat]
    #imlist_posi_y_pat.extend(imlist_nega_y_pat)

    #pattern projection screen
    window_name='projector'
    cv.namedWindow(window_name,cv.WND_PROP_FULLSCREEN)
    cv.moveWindow(window_name,screen.x-1,screen.y-1)
    cv.setWindowProperty(window_name,cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

    # Capture
    imlist_posi_x_cap=[imshowAndCapture(cap, img) for img in imlist_posi_x_pat]

    # DecodeX
    img_index_x=sl.PhaseShifting().decodeAmplitude(imlist_posi_x_cap)
    plt.imsave(imageX_name+'.png',img_index_x,cmap='gray')

    # Capture
    imlist_posi_y_cap=[imshowAndCapture(cap, img) for img in imlist_posi_y_pat]

    # DecodeY
    img_index_y = sl.PhaseShifting().decodeAmplitude(imlist_posi_y_cap)
    plt.imsave(imageY_name+'.png',img_index_y,cmap='gray')

    # Close camera
    cap.end()

    # Delete unused variables
    del num,F,F1,F2,imlist,imlist_posi_x_pat,imlist_posi_x_cap,imlist_posi_y_pat,imlist_posi_y_cap

    # Visualize decode result
    img_correspondence = cv.merge([0.0*np.zeros_like(img_index_x), img_index_x/width, img_index_y/height])
    del img_index_x,img_index_y
    
    img_correspondence=np.clip(img_correspondence*255.0, 0, 255).astype(np.uint8)
    img_correspondence=cv.cvtColor(img_correspondence, cv.COLOR_BGR2GRAY)
    plt.imsave(imageXY_name+'.png',img_correspondence,cmap='gray')
    #cv.imwrite(imageXY_name+'.png',img_correspondence)
    cv.destroyAllWindows()

if __name__=="__main__":
    main()