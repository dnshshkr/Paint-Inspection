import basler,cv2,keyboard,pathlib
DEFAULT_FILENAME='raw_capture'
WINDOW_NAME='live cam'
index=0
show_fringe=0
show_white=0
firstTimeRun=0
if firstTimeRun:
    import screeninfo
    basler.Basler.parameterizeCamera()
if show_fringe or show_white:
    import screeninfo
    screen=screeninfo.get_monitors()[0]
if show_fringe:
    import structuredlight as sl
    img=sl.PhaseShifting()
    imgX=img.generate((1920,1080))
cam=basler.Basler(mode=basler.MODE_LIVE,image_size=(1920,1080),rotate_image=180)
cv2.namedWindow(WINDOW_NAME,cv2.WINDOW_GUI_NORMAL)
cv2.moveWindow(WINDOW_NAME,0,0)
i=0
if show_fringe:
    cv2.namedWindow('fringe',cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty('fringe',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow('fringe',screen.x,screen.y)
elif show_white:
    import numpy as np
    cv2.namedWindow('white',cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty('white',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow('white',screen.x,screen.y)
    cv2.imshow('white',255*np.ones((1080,1920),dtype=np.uint8))
while cam.isLive:
    img=cam.retrieve()
    cv2.imshow(WINDOW_NAME,img)
    if show_fringe:
        cv2.imshow('fringe',imgX[i])
        i+=1
        if i>=len(imgX):
            i=0
    if cv2.waitKey(1)==27 or cv2.getWindowProperty(WINDOW_NAME,cv2.WND_PROP_VISIBLE)<1:
        cam.end()
        cv2.destroyAllWindows()
        break
    elif keyboard.is_pressed('s') or keyboard.is_pressed('S'):
        path=r'E:\Delloyd\Paint Inspection\Pictures\Raw captures'+DEFAULT_FILENAME
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