import basler,cv2,keyboard,pathlib
DEFAULT_FILENAME='raw_capture'
WINDOW_NAME='live cam'
index=0
show_fringe=1
firstTimeRun=1
if firstTimeRun:
    basler.Basler.parameterizeCamera()
if show_fringe:
    import structuredlight as sl
    import screeninfo
    img=sl.PhaseShifting()
    imgX=img.generate((1920,1080))
    screen=screeninfo.get_monitors()[1]
cam=basler.Basler(mode=basler.MODE_LIVE,image_size=(1920,1080),rotate_image=180)
cv2.namedWindow(WINDOW_NAME,cv2.WINDOW_GUI_NORMAL)
cv2.moveWindow(WINDOW_NAME,0,0)
i=0
if show_fringe:
    cv2.namedWindow('stripe',cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty('stripe',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow('stripe',screen.x-1,screen.y-1)
while cam.isLive:
    img=cam.retrieve()
    cv2.imshow(WINDOW_NAME,img)
    if show_fringe:
        cv2.imshow('stripe',imgX[i])
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