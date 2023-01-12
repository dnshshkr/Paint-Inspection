import numpy as np
import cv2
import time
x = np.arange(-250, 500, 1)
X, Y = np.meshgrid(x, x)
wavelength=50
patX,patY=np.sin(2*np.pi*X/wavelength),np.sin(2*np.pi*Y/wavelength)
_,grating=cv2.threshold(patX, 0, 0.5, cv2.THRESH_BINARY)
cv2.namedWindow("Fringe", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Fringe",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.moveWindow("Fringe",1920,0)
while True:
    cv2.imshow("Fringe", grating)
    grating=np.roll(grating,shift=30,axis=1)
    time.sleep(0.5)
    if cv2.waitKey(1)==27:
        break