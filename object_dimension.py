from scipy.spatial import distance as dist
from imutils import perspective,contours
import imutils
import numpy as np
import cv2
import pypylon.pylon as py
#width=0.925
width=0.891
cam_ratio=2/3
resize_y=768
window_name='object_dim'
k=7
def midpoint(ptA,ptB):
    return ((ptA[0]+ptB[0])*0.5,(ptA[1]+ptB[1])*0.5)
cam=py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
cam.StartGrabbing(py.GrabStrategy_LatestImageOnly)
converter=py.ImageFormatConverter()
converter.OutputPixelFormat=py.PixelType_BGR8packed
converter.OutputBitAlignment=py.OutputBitAlignment_MsbAligned
while cam.IsGrabbing():
    grabResult=cam.RetrieveResult(5000,py.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        image=converter.Convert(grabResult)
        img=image.GetArray()
        img=cv2.resize(img,(int(resize_y/cam_ratio),resize_y))
        orig=img.copy()
        #img=cv2.GaussianBlur(img,(7,7),100)
        #img=cv2.GaussianBlur(img,(k,k),0)
        img=cv2.blur(img,(9,9),0)
        cv2.namedWindow('blur',cv2.WINDOW_NORMAL)
        cv2.imshow('blur',img)
        try:
            edge=cv2.Canny(img,50,100)
            edge=cv2.dilate(edge,None,iterations=1)
            edge=cv2.erode(edge,None,iterations=1)
            cnts=cv2.findContours(edge.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts=imutils.grab_contours(cnts)
            (cnts,_)=contours.sort_contours(cnts)
        except:
            img=cv2.putText(img,'No contours detected',(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,0,255),2)
            cv2.imshow(window_name,img)
        pixelsPerMetric=None
        cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
        #cv2.moveWindow(window_name,0,0)
        for c in cnts:
            if cv2.contourArea(c)<1000:
                # if i==len(cnts)-1:
                #     img=cv2.putText(img,'No contours detected',(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,0,255),2)
                #     cv2.imshow(window_name,img)
                # else:
                #     continue
                continue
            box=cv2.minAreaRect(c)
            box=cv2.boxPoints(box)
            box=np.array(box,dtype='int')
            #box=perspective.order_points(box)
            cv2.drawContours(orig,[box.astype('int')],-1,(0,255,0),2)
            # for (x,y) in box:
            #     cv2.circle(orig,(int(x),int(y)),5,(0,0,255),-1)
            (tl,tr,br,bl)=box
            (tltrX,tltrY)=midpoint(tl,tr)
            (blbrX,blbrY)=midpoint(bl,br)
            (tlblX,tlblY)=midpoint(tl,bl)
            (trbrX,trbrY)=midpoint(tr,br)
            # cv2.circle(orig,(int(tltrX),int(tltrY)),5,(255,0,0),-1)
            # cv2.circle(orig,(int(blbrX),int(blbrY)),5,(255,0,0),-1)
            # cv2.circle(orig,(int(tlblX),int(tlblY)),5,(255,0,0),-1)
            # cv2.circle(orig,(int(trbrX),int(trbrY)),5,(255,0,0),-1)
            #cv2.line(orig,(int(tltrX),int(tltrY)),(int(blbrX),int(blbrY)),(255,0,255),2)
            #cv2.line(orig,(int(tlblX),int(tlblY)),(int(trbrX),int(trbrY)),(255,0,255),2)
            dA=dist.euclidean((tltrX,tltrY),(blbrX,blbrY))
            dB=dist.euclidean((tlblX,tlblY),(trbrX,trbrY))
            if pixelsPerMetric is None:
                pixelsPerMetric=dB/width
            dimA=dA/pixelsPerMetric*25.4
            dimB=dB/pixelsPerMetric*25.4
            cv2.putText(orig, "{:.1f}mm".format(dimB),(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 0), 2)
            cv2.putText(orig, "{:.1f}mm".format(dimA),(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 0), 2)
            cv2.imshow(window_name,orig)
        grabResult.Release()
    if cv2.waitKey(1)==27 or cv2.getWindowProperty(window_name,cv2.WND_PROP_VISIBLE)<1:
        cam.StopGrabbing()
        break
cv2.destroyAllWindows()