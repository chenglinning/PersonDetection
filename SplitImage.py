import cv2
import numpy as np
import os
import sys
def Image_Split(srcpicture_path,dstpicture_path,heigth_split_num,width_split_num):
    image=cv2.imread(srcpicture_path)
    #image=cv2.GaussianBlur(image,(3,3),0)
    (h,w)=image.shape[0:2]
    for filename in os.listdir(dstpicture_path):
		if filename is not None:
			os.remove(dstpicture_path+filename)
    for filename in os.listdir('results/'):
		if filename is not None:
			os.remove('results/'+filename)
    Writefile_path=dstpicture_path+'Image_Split_names1.txt'
    fp=open(Writefile_path,'wb')
    count=0
    flag=1
    for i in range(heigth_split_num):
        for j in range(width_split_num):
            if count==3:
                fp.close()
                Writefile_path=dstpicture_path+'Image_Split_names'+str(flag+1)+'.txt'
                fp=open(Writefile_path,'wb')
                flag+=1
                count=0
            filename=str(i+1)+str(j+1)+'.png'          
            filepath=dstpicture_path+filename
            fp.write(filepath)
            fp.write('\n')
            count+=1
            
            cv2.imwrite(filepath,image[i*(h/heigth_split_num):(i+1)*(h/heigth_split_num),j*(w/width_split_num):(j+1)*(w/width_split_num)])
    fp.close()
    
srcpicture_path=str(sys.argv[1])
dstpicture_path='Image_Split/'
heigth_split_num=int(sys.argv[2])
width_split_num=int(sys.argv[3])
Image_Split(srcpicture_path,dstpicture_path,heigth_split_num,width_split_num)
