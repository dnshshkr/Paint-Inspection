from pypylon import pylon
import screeninfo
import cv2
import structuredlight as sl
import numpy as np
screen_id=2
converter=''
kernel=np.array([[-1,-1,-1],
                 [-1,8,-1],
                 [-1,-1,-1]])
try:
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height
except:
    print('Monitor not detected')
    exit()
def main():
    global converter
    try:
        cap=pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        cap.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        converter=pylon.ImageFormatConverter()
        converter.OutputPixelFormat=pylon.PixelType_BGR8packed
        converter.OutputBitAlignment=pylon.OutputBitAlignment_MsbAligned
    except:
        cap = cv2.VideoCapture(1) # External web camera
        cap.open
    
    #smooth edge
    # num1=num2=7
    # F1=10
    # F2=int(float(F1)*9.0/16.0)
    # phaseShiftingX=sl.PhaseShifting(num1,F1)
    # imlistX=phaseShiftingX.generate((width,height))
    # phaseShiftingY=sl.PhaseShifting(num2,F2)
    # imlistY=sl.transpose(phaseShiftingY.generate((width,height)))

    #solid edge
    x = np.arange(-250, 500, 1)
    X, Y = np.meshgrid(x, x)
    wavelength=50
    patX,patY=np.sin(2*np.pi*X/wavelength),np.sin(2*np.pi*Y/wavelength)
    _,imlistX=cv2.threshold(patX, 0, 0.5, cv2.THRESH_BINARY)
    _,imlistY=cv2.threshold(patY, 0, 0.5, cv2.THRESH_BINARY)

    print(len(imlistX))

    shifting(cap,imlistX,'shiftingX')
    shifting(cap,imlistY,'shiftingY')
    cv2.destroyAllWindows()
def shifting(cap,imlist,wnamePat,delay=350):
    global converter
    global kernel
    wnameDisp='display'
    cv2.namedWindow(wnamePat,cv2.WND_PROP_FULLSCREEN)
    #print(screen.x,screen.y)
    cv2.moveWindow(wnamePat,screen.x-1,screen.y-1)
    cv2.setWindowProperty(wnamePat,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.namedWindow(wnameDisp,cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(wnameDisp,0,0)
    cv2.setWindowProperty(wnameDisp,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    index=0
    while cap.IsGrabbing():
        cv2.imshow(wnamePat,imlist[index])
        grabResult=cap.RetrieveResult(5000,pylon.TimeoutHandling_ThrowException)
        image=converter.Convert(grabResult).GetArray()
        image=cv2.resize(image,(1920,1080))
        image=cv2.filter2D(image,ddepth=-1,kernel=kernel)
        cv2.imshow(wnameDisp,image)
        index+=1
        if index==len(imlist):
            index=0
        if cv2.waitKey(1)==27 or cv2.waitKey(1)==10 or cv2.getWindowProperty(wnameDisp,cv2.WND_PROP_VISIBLE)<1:
            break
if __name__=='__main__':
    main()