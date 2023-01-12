import screeninfo
import numpy as np
import cv2
import pypylon.pylon as py
import matplotlib.pyplot as plt
class Basler():
    def __init__(self,model):
        super().__init__()
        self.model=model
        if self.model=='ac5472':
            self.resolutionX=5472
            self.resolutionY=3648
        #self.cap=py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
        self.cap=py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
def capture(cap,window_name,resX,resY,img,delay=250):
    #params
    scale_percent=100
    cv2.imshow(window_name,img)
    img_gray=cap.GrabOne(4000)
    img_gray=img_gray.Array
    width=int(resX*scale_percent/100)
    height=int(resY*scale_percent/100)
    dim=(width,height)
    img_gray=cv2.resize(img_gray,dim,interpolation=cv2.INTER_AREA)
    cv2.namedWindow("img_gray",cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("img_gray",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("img_gray",img_gray)
    cv2.moveWindow("img_gray",0,0)
    cv2.waitKey(delay)
    return img_gray
def calc_param(imlist):
    num=len(imlist)
    n=np.arange(0,num)
    R=np.dstack(imlist)
    M=np.array([np.ones_like(n),np.cos(2*np.pi*n/num),-np.sin(2*np.pi*n/num)]).T #(num, 3)
    M_pinv=np.linalg.inv(M.T@M)@M.T #(3, num)
    U=np.tensordot(M_pinv,R,axes=(1,2)).transpose(1,2,0) #(height, width, 3)
    return U
def decodeAmplitude(imlist):
    U=calc_param(imlist)
    _,U2,U3=list(U.transpose(2,0,1))
    img_amplitude=np.sqrt(U2**2+U3**2)
    return img_amplitude
def main():
    screen_id=2
    screen=screeninfo.get_monitors()[screen_id]
    camera=Basler('ac5472')
    h=1080
    w=1920
    window_name='static'
    try:
        #cap = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
        cap=camera.cap
        cap.Open()
    except:
        print('error accessing the camera')
    pattern=[]
    # for i in range(h):
    #     pattern_h=[]
    #     for j in range(w):
    #         for k in range(2):
    #             rand=np.random.randint(0,2)
    #             if rand==0:
    #                 pattern_set=np.zeros(3).tolist()
    #             else:
    #                 pattern_set=np.ones(3).tolist()
    #         pattern_set=[pattern_set[k]*255 for k in range(3)]
    #         pattern_h.append(pattern_set)
    #     pattern.append(pattern_h)
    # pattern=np.array(pattern)
    #cv2.imwrite(r'C:\Users\Danish\Desktop\static2.png',pattern)

    #pattern.append(cv2.imread(r'E:\Delloyd\Paint Inspection\static.png'))#[0]
    pattern.append(cv2.imread(r'E:\Delloyd\Paint Inspection\Pictures\pattern1.png'))#[0]
    pattern.append(np.bitwise_not(pattern[0]))#[1]
    pattern.append(np.rot90(np.rot90(pattern[0])))#[2]
    pattern.append(np.bitwise_not(pattern[2]))#[3]

    # pattern.append(cv2.imread(r'E:\Delloyd\Paint Inspection\Pictures\pattern2.png'))#[4]
    # pattern.append(np.bitwise_not(pattern[4]))#[5]
    # pattern.append(np.rot90(np.rot90(pattern[4])))#[6]
    # pattern.append(np.bitwise_not(pattern[6]))#[7]
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name,screen.x-1,screen.y-1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    imlistX=[capture(cap,window_name,camera.resolutionX,camera.resolutionY,img) for img in pattern[0:int(len(pattern)/2)]]
    img_indexX=decodeAmplitude(imlistX)
    imlistY=[capture(cap,window_name,camera.resolutionX,camera.resolutionY,img) for img in pattern[int(len(pattern)/2):int(len(pattern))]]
    img_indexY=decodeAmplitude(imlistY)
    img_merge=cv2.merge([0.0*(np.zeros_like(img_indexX)),img_indexX/screen.width,img_indexY/screen.height])
    img_merge=np.clip(img_merge*255.0,0,255).astype(np.uint8)
    img_correspondence=cv2.cvtColor(img_merge,cv2.COLOR_BGR2GRAY)
    print(len(imlistX),len(imlistY))
    del img_merge
    cv2.destroyAllWindows()
    plt.subplot(131)
    plt.imshow(img_correspondence,cmap='gray')
    plt.title('Merged XY')
    plt.subplot(132)
    plt.imshow(img_indexX,cmap='gray')
    plt.title('indexX')
    plt.subplot(133)
    plt.imshow(img_indexY,cmap='gray')
    plt.title('indexY')
    plt.show()
    # for i in range(len(pattern)):
    #     cv2.imshow(window_name,pattern[i])
    #     cv2.waitKey(1000)
    # cv2.waitKey()

    
if __name__=='__main__':
    main()
