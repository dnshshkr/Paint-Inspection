from pypylon import pylon
import os
import cv2
import subprocess
MODE_LIVE:bool=0
MODE_CAPTURE:bool=1
DEFAULT_IMAGE_WIDTH=5472
DEFAULT_IMAGE_HEIGHT=3648
DEAFULT_IMAGE_ORIENTATION=0
_DEFAULT_TIMEOUT=5000
class Basler:
    def __init__(self,mode=MODE_CAPTURE,image_size=(DEFAULT_IMAGE_WIDTH,DEFAULT_IMAGE_HEIGHT),rotate_image=180):
        self.image_size=image_size
        if rotate_image==0:
            pass
        elif rotate_image==90:
            self.image_orientation=cv2.ROTATE_90_CLOCKWISE
        elif rotate_image==180:
            self.image_orientation=cv2.ROTATE_180
        elif rotate_image==-90:
            self.image_orientation=cv2.ROTATE_90_COUNTERCLOCKWISE
        else:
            raise SyntaxError('image orientation is incorrect, available orientation: [-90, 0, 90, 180]')
        try:
            self._camera=pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self._camera.Open()
        except:
            print('no basler camera is found')
        self.mode=mode
        if mode is MODE_LIVE:
            self._camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            self._converter=pylon.ImageFormatConverter()
            self._converter.OutputPixelFormat=pylon.PixelType_BGR8packed
            self._converter.OutputBitAlignment=pylon.OutputBitAlignment_MsbAligned
            self.isLive=self._camera.IsGrabbing()
    def retrieve(self):
        if self.mode==MODE_LIVE:
            self._grabResult=self._camera.RetrieveResult(_DEFAULT_TIMEOUT,pylon.TimeoutHandling_ThrowException)
            self.grabSucceed=self._grabResult.GrabSucceeded()
            self._liveFeed=self._converter.Convert(self._grabResult)
            self._liveFeed=self._liveFeed.GetArray()
            self._liveFeed=cv2.resize(self._liveFeed,self.image_size) if self.image_size!=(DEFAULT_IMAGE_WIDTH,DEFAULT_IMAGE_HEIGHT) else self._liveFeed
            self._liveFeed=cv2.rotate(self._liveFeed,self.image_orientation) if self.image_orientation!=DEAFULT_IMAGE_ORIENTATION else self._liveFeed
            self._grabResult.Release()
            return self._liveFeed
        elif self.mode==MODE_CAPTURE:
            self._instantImage=self._camera.GrabOne(_DEFAULT_TIMEOUT).Array
            self._instantImage=cv2.resize(self._instantImage,self.image_size) if self.image_size!=(DEFAULT_IMAGE_WIDTH,DEFAULT_IMAGE_HEIGHT) else self._instantImage
            self._instantImage=cv2.rotate(self._instantImage,self.image_orientation) if self.image_orientation!=DEAFULT_IMAGE_ORIENTATION else self._instantImage
            return self._instantImage
    def end(self):
        self._camera.StopGrabbing()
        self._camera.Close()
        print('camera stopped')
    @staticmethod
    def parameterizeCamera():
        #os.startfile(r"E:\Delloyd\Paint Inspection\Python codes\ParametrizeCamera_LoadAndSave.exe")
        subprocess.check_call(['cmd','/c','ParametrizeCamera_LoadAndSave.exe'])
        print('camera parameterized')