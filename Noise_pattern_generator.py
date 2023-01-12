import screeninfo
import numpy as np
import cv2
from numba import jit
import time
from PIL import Image
screen_id=0
screen=screeninfo.get_monitors()[screen_id]
@jit()
def generate(w,h):
    start=time.time()
    pattern=[]
    for i in range(h):
        pattern_h=[]
        for j in range(w):
            for k in range(2):
                rand=np.random.randint(0,2)
                pattern_set=np.zeros(3).tolist() if rand==0 else np.ones(3).tolist()
            pattern_set=[pattern_set[k]*255 for k in range(3)]
            pattern_h.append(pattern_set)
        pattern.append(pattern_h)
    pattern=np.array(pattern)
    time_taken=time.time()-start
    #del pattern_set,pattern_h,i,j,k
    print('finished in {:.2f} s'.format(time_taken))
    return pattern
# def resize(pattern,dim):
#     x,y=dim[0],dim[1]
#     x_mult,y_mult=int(x/len(pattern[0])),int(y/len(pattern))
#     new_pattern=np.ones((y,x,3))
#     print(np.shape(new_pattern))
#     l,m=0,0
#     for i in range(len(new_pattern)):
#         for j in range(len(new_pattern[0])):
#             new_pattern[i][j]=pattern[l][m]
#         m+=1
def main():
    #generate(screen.width,screen.height)
    pattern=generate(16,9)
    # pattern=resize(pattern,(1920,1080))
    #image=Image.open(r'C:\Users\Danish\Desktop\pattern.png')
    image=Image.fromarray(np.uint8(pattern))
    image=image.resize((1920,1080),resample=Image.Resampling.BILINEAR)
    image.save(r'C:\Users\Danish\Desktop\pattern.png')
    #image.show()
if __name__=='__main__':
    main()