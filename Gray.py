"""
Capture projection pattern and decode x-coorde.
"""
import cv2
import numpy as np
import structuredlight as sl
import screeninfo
from pypylon import pylon
from matplotlib import pyplot as plt
import basler

screen_id=2
part_name='dust_silver'
imageX_name='imageX_Gray'+'_'+part_name
imageY_name='imageY_Gray'+'_'+part_name
imageXY_name='imageXY_Gray'+'_'+part_name

# get the size of the screen
try:
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height
except:
    print('Monitor not detected')
    exit()

window_name='projector'
def imshowAndCapture(cap, img_pattern, delay=100):
    
    cv2.imshow(window_name, img_pattern)
    cv2.waitKey(delay)
    # ret, img_frame = cap.read()

    # img_frame = cap.GrabOne(5000)
    # img_gray = img_frame.Array

    img_gray=cap.retrieve()
    #img_gray = img_gray[y1:y2, x1:x2]
    # ret, img_gray = cv2.threshold(img_gray, 30, 255, cv2.THRESH_TOZERO)
    cv2.namedWindow("img_gray", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("img_gray", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("img_gray", img_gray)
    cv2.moveWindow("img_gray",0,0)
    if cv2.waitKey(1)==27:
        exit()
    return img_gray

def main():
    try:
        cap=basler.Basler(basler.MODE_CAPTURE,(1920,1080),180)
    except:
        cap = cv2.VideoCapture(1) # External web camera
        cap.open
    pattern = sl.Gray()
    
    # Generate and Decode x-coord
    # Generate
    imlist_posi_x_pat = pattern.generate((width, height))
    imlist_nega_x_pat = sl.invert(imlist_posi_x_pat)

    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Capture
    imlist_posi_x_cap = [imshowAndCapture(cap, img) for img in imlist_posi_x_pat]
    imlist_nega_x_cap = [imshowAndCapture(cap, img) for img in imlist_nega_x_pat]
    
    # Decode
    img_index_x = pattern.decode(imlist_posi_x_cap, imlist_nega_x_cap)
    #img_index_x=sl.PhaseShifting().decodeAmplitude(imlist_posi_x_cap)

    
    # Generate and Decode y-coord
    # Generate
    imlist = pattern.generate((height, width))
    imlist_posi_y_pat = sl.transpose(imlist)
    imlist_nega_y_pat = sl.invert(imlist_posi_y_pat)
    
    # Capture
    imlist_posi_y_cap = [imshowAndCapture(cap, img) for img in imlist_posi_y_pat]
    imlist_nega_y_cap = [imshowAndCapture(cap, img) for img in imlist_nega_y_pat]
    
    # Decode
    img_index_y = pattern.decode(imlist_posi_y_cap, imlist_nega_y_cap)
    #img_index_y=sl.PhaseShifting().decodeAmplitude(imlist_posi_y_cap)
   

    # Visualize decode result
    img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x/width, img_index_y/height])
    #img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x, img_index_y])
    img_correspondence = np.clip(img_correspondence*255.0, 0, 255).astype(np.uint8)
    img_correspondence=cv2.cvtColor(img_correspondence,cv2.COLOR_BGR2GRAY)
    plt.imsave(imageX_name+'.png',img_index_x,cmap='gray')
    plt.imsave(imageY_name+'.png',img_index_y,cmap='gray')
    plt.imsave(imageXY_name+'.png',img_correspondence,cmap='gray')

    
    cv2.destroyAllWindows()
    cap.end()

if __name__=="__main__":
    main()