"""
Capture projection pattern and decode x-coorde.
"""
import cv2
import numpy as np
import structuredlight as sl
import screeninfo
from pypylon import pylon
from matplotlib import pyplot as plt

screen_id = 2
is_color = 1

# get the size of the screen
try:
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height
except:
    print('Monitor not detected')
    exit()

window_name='projector'
def imshowAndCapture(cap, img_pattern, delay=350):
    
    cv2.imshow(window_name, img_pattern)
    cv2.waitKey(delay)
    # ret, img_frame = cap.read()

    img_frame = cap.GrabOne(4000)
    img_gray = img_frame.Array
    
    # resize image
    img_gray = cv2.resize(img_gray, (width,height))#, interpolation = cv2.INTER_AREA)
    #img_gray = img_gray[y1:y2, x1:x2]
    # ret, img_gray = cv2.threshold(img_gray, 30, 255, cv2.THRESH_TOZERO)
    cv2.namedWindow("img_gray", cv2.WND_PROP_FULLSCREEN);cv2.setWindowProperty("img_gray", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);cv2.imshow("img_gray", img_gray);cv2.moveWindow("img_gray",0,0)
    if cv2.waitKey(1)==27:
        exit()
    return img_gray

def main():
    try:
        cap = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        cap.Open()
    except:
        cap = cv2.VideoCapture(1) # External web camera
        cap.open
    pattern = sl.Checker(sqsize=50,step=2)
    
    # Generate and Decode x-coord
    # Generate
    imlist_posi_x_pat = pattern.generate((width, height))
    #imlist_nega_x_pat = [cv2.rotate(img,cv2.ROTATE_180) for img in imlist_posi_x_pat]
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Capture
    imlist_posi_x_cap = [imshowAndCapture(cap, img) for img in imlist_posi_x_pat]
    #imlist_nega_x_cap = [imshowAndCapture(cap, img) for img in imlist_nega_x_pat]
    #imlist_nega_x_cap.extend(imlist_nega_x_cap)
    
    # Decode
    img_index_x,img_glob_x = pattern.decode(imlist_posi_x_cap)
    plt.imshow(img_glob_x,cmap='gray')

    
    # Generate and Decode y-coord
    # Generate
    imlist = pattern.generate((height, width))
    imlist_posi_y_pat = sl.transpose(imlist)
    #imlist_nega_y_pat = [cv2.rotate(img,cv2.ROTATE_180) for img in imlist_posi_y_pat]
    
    # Capture
    imlist_posi_y_cap = [imshowAndCapture(cap, img) for img in imlist_posi_y_pat]
    #imlist_nega_y_cap = [imshowAndCapture(cap, img) for img in imlist_nega_y_pat]
    #imlist_posi_y_cap.extend(imlist_nega_y_cap)
    
    # Decode
    img_index_y,img_glob_y = pattern.decode(imlist_posi_y_cap)
    plt.imshow(img_glob_y,cmap='gray')
   

    # Visualize decode result
    #img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x/width, img_index_y/height])
    img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x/width, img_index_y/height])
    img_correspondence = np.clip(img_correspondence*255.0, 0, 255).astype(np.uint8)
    img_correspondence=cv2.cvtColor(img_correspondence,cv2.COLOR_BGR2GRAY)
    plt.imsave('imageXY.png',img_correspondence,cmap='gray')
    cv2.imshow("x:Green, y:Red", img_correspondence)
    cv2.waitKey(0)
    cv2.imwrite("correspondence.png", img_correspondence)
    cv2.destroyAllWindows()
    cap.release()

if __name__=="__main__":
    main()