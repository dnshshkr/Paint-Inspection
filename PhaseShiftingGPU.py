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
import imageprocessing as ip
firstTimeRun=0
if firstTimeRun:
    basler.Basler.parameterizeCamera()

screen_id=2

# get the size of the screen
try:
    screen = screeninfo.get_monitors()[screen_id]
except:
    print('Monitor not detected')
    exit()
finally:
    width, height = screen.width, screen.height

# x1=2900
# x2=3400
# y1=600
# y2=1400

def imshowAndCapture(cap, img_pattern, delay=350):
    window_name='projector'
    cv2.imshow(window_name, img_pattern)
    cv2.waitKey(delay)
    # ret, img_frame = cap.read()

    img_gray=cap.capture()
    
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

def main():
    try:
        cap=basler.Basler(image_size=(1920,1080),rotate_image=180)
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
    #imlist_neg_x_pat = [cv2.rotate(img,cv2.ROTATE_180) for img in imlist_posi_x_pat]
    #print(imlist_posi_x_pat)
    window_name='projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Capture
    imlist_posi_x_cap = [imshowAndCapture(cap, img) for img in imlist_posi_x_pat]
    #imlist_neg_x_cap = [imshowAndCapture(cap, img) for img in imlist_neg_x_pat]
    #imlist_posi_x_cap.extend(imlist_neg_x_cap)

    # Decode
    img_index_x = sl.PhaseShifting().decodeAmplitude(imlist_posi_x_cap)
    plt.imsave('imageX_PhaseShifting.png',img_index_x,cmap='gray')
    
    num2=num
    #F2=int(20*9/16)
    F2=int(float(F)*9.0/16.0)
    phaseshifting = sl.PhaseShifting(num2,F2)

    # Generate and Decode y-coord
    imlist = phaseshifting.generate((width, height))
    imlist_posi_y_pat = sl.transpose(imlist)

    # Capture
    imlist_posi_y_cap = [imshowAndCapture(cap, img) for img in imlist_posi_y_pat]

    #close camera
    cap.end()
    
    # Decode
    img_index_y = sl.PhaseShifting().decodeAmplitude(imlist_posi_y_cap)
    plt.imsave('imageY_PhaseShifting.png',img_index_y,cmap='gray')

    #delete unused variables
    del num,num1,num2,F,F1,F2,imlist,imlist_posi_x_pat,imlist_posi_x_cap,imlist_posi_y_pat,imlist_posi_y_cap

    # Visualize decode result
    img_correspondence = cv2.merge([0.0*np.zeros_like(img_index_x), img_index_x/width, img_index_y/height])
    del img_index_x,img_index_y
    
    img_correspondence = np.clip(img_correspondence*255.0, 0, 255).astype(np.uint8)
    gpu_frame=cv2.cuda_GpuMat()
    gpu_frame.upload(img_correspondence)
    img_correspondence_gpu=cv2.cuda.cvtColor(gpu_frame, cv2.COLOR_BGR2GRAY)
    plt.imsave('imageXY_PhaseShifting.png',img_correspondence_gpu.download(),cmap='gray')

    #filter noise
    img_correspondence=cv2.cuda.medianBlur(img_correspondence_gpu,3)
    
    kernel_erode=np.ones((6,6),np.uint8)
    kernel_dilate=np.ones((5,5),np.uint8)
    #erode
    img_correspondence_gpu=cv2.cuda.erode(img_correspondence_gpu,kernel_erode)
    plt.imsave('imageXY_PhaseShiftingErode.png',img_correspondence_gpu.download(),cmap='gray')

    #dilate
    plt.imsave('imageXY_PhaseShiftingDilate.png',ip.dilate(img_correspondence,'low'),cmap='gray')

    #binary
    plt.imsave('imageXY_PhaseShiftingBW.png',ip.blackAndWhite(cv2.imread('imageXY_PhaseShifting.png'),150),cmap='gray')

    processed_image=cv2.cvtColor(cv2.imread('processed image.png',plt.imsave('processed image.png',ip.dilate(ip.erode(img_correspondence,'medium'),'low'),cmap='gray')),cv2.COLOR_BGR2GRAY)
    binary_image=ip.blackAndWhite(processed_image,100)

    #close all windows
    cv2.destroyAllWindows()

    _images=[[cv2.imread('imageX_PhaseShifting.png'),cv2.imread('imageY_PhaseShifting.png'),cv2.imread('imageXY_PhaseShifting.png')],
            [cv2.imread('imageXY_PhaseShiftingErode.png'),cv2.imread('imageXY_PhaseShiftingDilate.png'),cv2.imread('imageXY_PhaseShiftingBW.png')]]
    _texts=[['imageX_PhaseShifting','imageY_PhaseShifting','imageXY_PhaseShifting'],
           ['imageXY_PhaseShiftingErode','imageXY_PhaseShiftingDilate','imageXY_PhaseShiftingBW']]
    images=[]
    for i in range(len(_images)):
        __images=[]
        for j in range(len(_images[0])):
            __images.append(ip.putText(_images[i][j],_texts[i][j]))
        images.append(__images)
    _images.clear()
    del _texts
    window_name='output'
    _images=[np.concatenate((images[0][0],images[0][1],images[0][2]),axis=1),np.concatenate((images[1][0],images[1][1],images[1][2]),axis=1)]
    image=np.concatenate((_images[0],_images[1]),axis=0)
    image=cv2.resize(image,(1920,1080))
    cv2.imwrite('stiched image.png',image)
    
    contours,_=cv2.findContours(binary_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        if cv2.contourArea(contour)>100:
            x,y,w,h=cv2.boundingRect(contour)
            cv2.rectangle(img_correspondence,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.namedWindow(window_name,cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow(window_name,0,0)
    cv2.imshow(window_name,image)
    cv2.imshow('processed image',processed_image)
    cv2.imshow('binary image',binary_image)
    cv2.imshow('suspected defects',img_correspondence)
    cv2.waitKey(0)

if __name__=="__main__":
    main()