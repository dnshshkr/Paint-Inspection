import basler,cv2,keyboard,pathlib
DEFAULT_FILENAME='raw_capture'
WINDOW_NAME='live cam'
index=0
firstTimeRun=1
if firstTimeRun:
    basler.Basler.parameterizeCamera()
cam=basler.Basler(mode=basler.MODE_LIVE,image_size=(1920,1080),rotate_image=180)
cv2.namedWindow(WINDOW_NAME,cv2.WINDOW_GUI_NORMAL)
cv2.moveWindow(WINDOW_NAME,0,0)
while cam.isLive:
    img=cam.retrieve()
    cv2.imshow(WINDOW_NAME,img)
    if cv2.waitKey(1)==27 or cv2.getWindowProperty(WINDOW_NAME,cv2.WND_PROP_VISIBLE)<1:
        cam.end()
        cv2.destroyAllWindows()
        break
    elif keyboard.is_pressed('s') or keyboard.is_pressed('S'):
        path='image processing/gray/'+DEFAULT_FILENAME
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