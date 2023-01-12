import pypylon.pylon as pylon
import cv2
import numpy as np
import pathlib
import basler
#from numba import jit,njit,vectorize
import keyboard
firstTimeRun=1
if firstTimeRun:
    basler.camset()
class usingWebcam:
    def __init__(self):
        self.result=True
    def GrabSucceeded(self):
        return self.result
thres=100
default_filename='capture'
index=0
#@jit()
def variance_of_laplacian(img,attr):
    return cv2.Laplacian(img,attr).var()
def detect_blur_fft(image,size=60,thresh=70):
    (h,w)=(len(image),len(image[0]))
    (cX,cY)=(int(w/2.0),int(h/2.0))
    fft=np.fft.fft2(image)
    fftShift=np.fft.fftshift(fft)
    fftShift[cY-size:cY+size,cX-size:cX+size]=0
    fftShift=np.fft.ifftshift(fftShift)
    recon=np.fft.ifft2(fftShift)
    magnitude=20*np.log(np.abs(recon))
    mean=np.mean(magnitude)
    return (mean,mean>thresh)
try:
    cam=pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    cam.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter=pylon.ImageFormatConverter()
    converter.OutputPixelFormat=pylon.PixelType_BGR8packed
    converter.OutputBitAlignment=pylon.OutputBitAlignment_MsbAligned
    is_basler:bool=True
    is_webcam:bool=False
    print('using basler')
except:
    cam=cv2.VideoCapture(0)
    is_basler:bool=False
    is_webcam:bool=True
    print('using webcam')
while (is_basler and cam.IsGrabbing()) or is_webcam:
    if is_basler:
        grabResult=cam.RetrieveResult(5000,pylon.TimeoutHandling_ThrowException)
    elif is_webcam:
        grabResult=usingWebcam()
    if grabResult.GrabSucceeded():
        if is_basler:
            image=converter.Convert(grabResult)
            img=image.GetArray()
        elif is_webcam:
            _,img=cam.read()
        img=cv2.resize(img,(640,480))
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8S)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8SC1)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8SC2)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8SC3)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8SC4)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8U)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8UC1)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8UC2)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8UC3)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_8UC4)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_16S)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_16SC1)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_16SC2)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_16SC3)))
        # except:fm.append('na')
        # try:fm.append(str(variance_of_laplacian(img,cv2.CV_16SC4)))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_16U))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_16UC1))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_16UC2))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_16UC3))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_16UC4))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32F))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32FC1))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32FC2))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32FC3))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32FC4))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32S))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32SC1))
        # except:fm.append('na')
        # try:fm.a(variance_of_laplacian(img,cv2.CV_32SC2))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32SC3))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_32SC4))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_64F))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_64FC1))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_64FC2))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_64FC3))
        # except:fm.append('na')
        # try:fm.append(variance_of_laplacian(img,cv2.CV_64FC4))
        # except:fm.append('na')
        fm=variance_of_laplacian(img,cv2.CV_8U)
       # fm=variance_of_laplacian(img,cv2.CV_16S)
        text='blur' if fm<thres else 'clear'
        
        #(fm,blurry)=detect_blur_fft(img,size=60,thresh=27)
        #text='blur' if blurry else 'clear'

        #print('{}: {:.2f}'.format(text,fm))
        cv2.namedWindow('blur',cv2.WINDOW_NORMAL)
        #cv2.moveWindow('blur',0,0)
        # padY=10
        # for i in range(len(fm)):
        #     cv2.putText(img,"fm[{}]: {}".format(i,fm[i]),(10,padY),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,255),1)
        #     padY+=10
        if is_basler:
            img=cv2.rotate(img,cv2.ROTATE_180)
        cv2.putText(img,"{}: {:.2f}".format(text,fm),(5,25),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.imshow('blur',img)
        if is_basler:
            grabResult.Release()
    if cv2.waitKey(1)==27 or cv2.getWindowProperty('blur',cv2.WND_PROP_VISIBLE)<1:
            break
    elif keyboard.is_pressed('s') or keyboard.is_pressed('S'):
        path='captures/'+default_filename
        suffix='.png'
        while True:
            if pathlib.Path(path+suffix).is_file:
                index+=1
                filename=path+str(index)+suffix
                cv2.imwrite(filename,img)
                break
            else:
                cv2.imwrite(path+suffix,img)
                break
        #cv2.imwrite('captures/test.png',img)
if is_basler:
    cam.StopGrabbing()
elif is_webcam:
    cam.release()
cv2.destroyAllWindows()