from pypylon import pylon
import os
import cv2
import subprocess
MODE_LIVE:bool=0
MODE_CAPTURE:bool=1
DEFAULT_IMAGE_WIDTH=5472
DEFAULT_IMAGE_HEIGHT=1080
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
            del self
        finally:
            print('camera started')
        self.mode=mode
        if mode is MODE_LIVE:
            self._camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            self._converter=pylon.ImageFormatConverter()
            self._converter.OutputPixelFormat=pylon.PixelType_BGR8packed
            self._converter.OutputBitAlignment=pylon.OutputBitAlignment_MsbAligned
            self.isLive=self._camera.IsGrabbing()
    def live(self):
        if self.mode==MODE_LIVE:
            self._grabResult=self._camera.RetrieveResult(5000,pylon.TimeoutHandling_ThrowException)
            self.liveFeed=self._converter.Convert(self._grabResult)
            self.liveFeed=self.liveFeed.GetArray()
            self.liveFeed=cv2.resize(self.liveFeed,self.image_size) if self.image_size!=(DEFAULT_IMAGE_WIDTH,DEFAULT_IMAGE_HEIGHT) else self.liveFeed
            self.liveFeed=cv2.rotate(self.liveFeed,self.image_orientation) if self.image_orientation!=DEAFULT_IMAGE_ORIENTATION else self.liveFeed
            return self.liveFeed
        elif self.mode==Basler.MODE_CAPTURE:
            raise SyntaxError('camera is not in live mode, consider changing mode to MODE_LIVE')
    def capture(self):
        self.instantImage=self._camera.GrabOne(_DEFAULT_TIMEOUT).Array
        self.instantImage=cv2.resize(self.instantImage,self.image_size) if self.image_size!=(DEFAULT_IMAGE_WIDTH,DEFAULT_IMAGE_HEIGHT) else self.instantImage
        self.instantImage=cv2.rotate(self.instantImage,self.image_orientation) if self.image_orientation!=DEAFULT_IMAGE_ORIENTATION else self.instantImage
        return self.instantImage
    def end(self):
        self._camera.StopGrabbing()
        self._camera.Close()
        print('camera stopped')
    @staticmethod
    def parameterizeCamera():
        #os.startfile(r"E:\Delloyd\Paint Inspection\Python codes\ParametrizeCamera_LoadAndSave.exe")
        subprocess.check_call(['cmd','/c','ParametrizeCamera_LoadAndSave.exe'])
        print('camera parameterized')