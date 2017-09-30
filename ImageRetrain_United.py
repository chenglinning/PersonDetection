import cv2
import numpy as np
import os
import re
import csv
import sys
import copy

def ImageRetrainUnited(CsvFilepath):
    student_count=0
    
    img=cv2.imread("img_united.png")
    pattern='.csv'
    for filename in os.listdir(CsvFilepath):
        match=re.search(pattern,filename)
        if match is not None:
            x_add=int(filename.split('.')[0].split('_')[0])
            y_add=int(filename.split('.')[0].split('_')[1])
            fp=open(CsvFilepath+filename)
            r=csv.reader(fp)
            for row in r:
                box=[x,y,w,h]=[int(row[1]),int(row[2]),int(row[3]),int(row[4])]  
                if w<30:
                    continue
                x=x+x_add
                y=y+y_add
                student_count+=1
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)
            fp.close()
    print 'the second count is:'+str(student_count)
    with open('studentnumber_save.txt','a') as f:
        f.write(str(student_count)+'\n')
    if os.path.exists("img_united_new.png"):
        os.remove("img_united_new.png")
    cv2.imwrite("img_united_new.png",img)
    #cv2.imshow("img_united_new",img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

CsvFilepath='ImageRetrain_results/'
ImageRetrainUnited(CsvFilepath)
