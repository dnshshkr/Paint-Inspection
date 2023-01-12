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
except:
    print('Monitor not detected')
    exit()
finally:
    width, height = screen.width, screen.height

window_name='projector'
def imshowAndCapture(cap, img_pattern, delay=350):
    cv2.imshow(window_name, img_pattern)
    cv2.waitKey(delay)

    img_frame = cap.GrabOne(5000)
    img_gray = img_frame.Array
    
    # resize image
    img_gray = cv2.rotate(cv2.resize(img_gray, (width,height)),cv2.ROTATE_180)#, interpolation = cv2.INTER_AREA)
    #img_gray = img_gray[y1:y2, x1:x2]
    # ret, img_gray = cv2.threshold(img_gray, 30, 255, cv2.THRESH_TOZERO)
    cv2.namedWindow("img_gray", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("img_gray", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("img_gray", img_gray)
    cv2.moveWindow("img_gray",0,0)
    # cv2.waitKey(0)
    # print(img_gray.shape)
    # img_gray = cv2.cvtColor(img_frame, cv2.COLOR_BGR2GRAY)
    #cv2.waitKey(1)
    return img_gray

def filterImage(img_correspondence,iteration_filter2D:bytes=1,kernelType_filter2D:str='sharpen',kernel_ED:np.matrix=np.ones((5,5),np.uint8),iteration_ED:bytes=1):
    #for i in range(iteration_ED):
    img_correspondence=cv2.erode(img_correspondence,kernel_ED,iterations=1)
    #img_correspondence=cv2.dilate(img_correspondence,kernel_ED,iterations=1)
    for i in range(iteration_filter2D):
        if kernelType_filter2D=='sharpen':
            kernel=np.array([[0,-1,0],
                            [-1,5,-1],
                            [0,-1,0]])
        elif iteration_filter2D=='edgeDetection3':
            kernel=np.array([[-1,-1,-1],
                            [-1,8,-1],
                            [-1,-1,-1]])
        img_correspondence=cv2.filter2D(img_correspondence,ddepth=-1,kernel=kernel)
    return img_correspondence

def main():
    try:
        cap = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        cap.Open()
    except:
        cap = cv2.VideoCapture(1) # External web camera
        cap.open
    num:int=5
    F:int=35
    num1=num
    F1=F
    phaseshifting = sl.PhaseShifting(num1,F1)
    #phaseshifting = sl.Gray()
   
    imlist_posi_x_pat = phaseshifting.generate((width, height))
    imlist_neg_x_pat = [cv2.rotate(img,cv2.ROTATE_180) for img in imlist_posi_x_pat]

    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Capture
    imlist_posi_x_cap = [imshowAndCapture(cap, img) for img in imlist_posi_x_pat]
    imlist_neg_x_cap = [imshowAndCapture(cap, img) for img in imlist_neg_x_pat]
    imlist_posi_x_cap.extend(imlist_neg_x_cap)

    # Decode
    #img_index_x=sl.Gray().decode(imlist_posi_x_cap,imlist_neg_x_cap)
    img_index_x = sl.PhaseShifting().decodeAmplitude(imlist_posi_x_cap)
    #img_index_x=cv2.fastNlMeansDenoising(img_index_x,None,20,7,21)

    
    num2=num
    #F2=int(20*9/16)
    F2=int(float(F)*9.0/16.0)
    phaseshifting = sl.PhaseShifting(num2,F2)
    #phaseshifting = sl.Gray()

    # Generate and Decode y-coord
    imlist = phaseshifting.generate((width, height))
    
    imlist_posi_y_pat = sl.transpose(imlist)
    imlist_neg_y_pat = [cv2.rotate(img,cv2.ROTATE_180) for img in imlist_posi_y_pat]

    # Capture
    imlist_posi_y_cap = [imshowAndCapture(cap, img) for img in imlist_posi_y_pat]
    imlist_neg_y_cap = [imshowAndCapture(cap, img) for img in imlist_neg_y_pat]
    imlist_posi_y_cap.extend(imlist_neg_y_cap)
    
    # Decode
    #img_index_y=sl.Gray().decode(imlist_posi_y_cap,imlist_neg_y_cap)
    img_index_y = sl.PhaseShifting().decodeAmplitude(imlist_posi_y_cap)
    #img_index_y=cv2.fastNlMeansDenoising(img_index_y,None,20,7,21)
   

    # Visualize decode result
    img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x/width, img_index_y/height])
    #img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x/height, img_index_y/width])
    #img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x, img_index_y])
    img_correspondence = np.clip(img_correspondence*255.0, 0, 255).astype(np.uint8)
    img_correspondence = cv2.cvtColor(img_correspondence, cv2.COLOR_BGR2GRAY)

    plt.imsave('imageXY_PhaseShifting.png',img_correspondence,cmap='gray')
    # kernel_ED=np.ones((5,5),np.uint8)
    # img_correspondence=filterImage(img_correspondence,iteration_filter2D=1,kernelType_filter2D='sharpen',kernel_ED=kernel_ED,iteration_ED=1)
    # img_correspondence=cv2.addWeighted(img_correspondence,10,img_correspondence,5,5)
    
    # x1=2000
    # x2=4500
    # y1=400
    # y2=2000

    # x1=1500
    # x2=3250
    # y1=300
    # y2=1500

    cv2.destroyWindow('img_gray')
    #cv2.imwrite('out.png',img_correspondence)
    #cv2.imshow('img_cv',img_cv)
    #plt.subplot(1, 3, 1)
    #plt.imshow(img_correspondence, cmap='gray')
    #plt.title('Combine Index XY')
    # plt.xlim([x1,x2])
    # plt.ylim([y1,y2])

    # plt.subplot(1, 2, 1)
    # plt.imshow(img_index_x, cmap='gray')
    # plt.title('img_index_x Num: '+ str(num1) + " and F: " + str(F1))

    #plt.subplot(1, 3, 2)
    #plt.imshow(img_index_x, cmap='gray')
    # plt.xlim([x1,x2])
    # plt.ylim([y1,y2])
    #plt.title('img_index_x Num: '+ str(num1) + " and F: " + str(F1))

    #plt.subplot(1, 3, 3)
    #plt.imshow(img_index_y, cmap='gray')
    #plt.title('img_index_y Num: '+ str(num2) + " and F: " + str(F2))
    # plt.xlim([x1,x2])
    # plt.ylim([y1,y2])
    plt.imsave('imageX_PhaseShifting.png',img_index_x,cmap='gray')
    plt.imsave('imageY_PhaseShifting.png',img_index_y,cmap='gray')
    # plt.imsave('imageXY.png',img_correspondence,cmap='gray')
    plt.show()
    cv2.destroyAllWindows()
    # cap.release()

if __name__=="__main__":
    main()