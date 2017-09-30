import cv2
import numpy as np
import os
import re
import csv
import sys
import copy

def BoxData_special_process(BoxData_special,rows,cols,heigth_split_num,width_split_num,piex_thresh):
    BoxData_special_return=[]
    for i in range(heigth_split_num-1):
        line_y=rows*(i+1)/heigth_split_num
        BoxList_united=[]
        for key in BoxData_special.keys():
            BoxList_tmp=BoxData_special[key]
            for BoxList in BoxList_tmp:
                if BoxList==[]:
                    continue
                if abs(BoxList[1]-line_y)<piex_thresh or abs(BoxList[1]+BoxList[3]-line_y)<piex_thresh:
                    BoxList_united.append(BoxList)
        [BoxList_del_return,BoxList_united_return]=BoxList_united_process_y(BoxList_united)
        for box in BoxList_del_return:
            flag=0
            for i in range(len(BoxList_united)):
                if BoxList_united[i]==box:
                    BoxList_united[i]=[]
                    break
            for key in BoxData_special.keys():
                BoxList_tmp=BoxData_special[key]
                for i in range(len(BoxList_tmp)):
                    if BoxList_tmp[i]==box:
                        BoxList_tmp[i]=[]
                        break      
                        flag=1
                if flag==1:
                    break    
        BoxList_united.extend(BoxList_united_return)
        BoxData_special[key].extend(BoxList_united_return)
        BoxData_special_return.extend(BoxList_united)

    for j in range(width_split_num-1):
        line_x=cols*(j+1)/width_split_num
        BoxList_united=[]
        for key in BoxData_special.keys():
            BoxList_tmp=BoxData_special[key]
            for BoxList in BoxList_tmp:
                if BoxList==[]:
                    continue
                if abs(BoxList[0]-line_x)<piex_thresh or abs(BoxList[0]+BoxList[2]-line_x)<piex_thresh :
                    BoxList_united.append(BoxList)
        [BoxList_del_return,BoxList_united_return]=BoxList_united_process_x(BoxList_united)
        for box in BoxList_del_return:
            flag=0
            for i in range(len(BoxList_united)):
                if BoxList_united[i]==box:
                    BoxList_united[i]=[]
                    break
            for key in BoxData_special.keys():
                BoxList_tmp=BoxData_special[key]
                for i in range(len(BoxList_tmp)):
                    if BoxList_tmp[i]==box:
                        BoxList_tmp[i]=[]
                        break    
                        flag=1
                if flag==1:
                    break        
        BoxList_united.extend(BoxList_united_return)
        BoxData_special[key].extend(BoxList_united_return)
        BoxData_special_return.extend(BoxList_united)        
    return BoxData_special

def BoxList_united_process_y(BoxList_united):
    index_save=[]
    BoxList_del_return=[]
    BoxList_united_return=[]
    BoxList_united_copy=copy.copy(BoxList_united)
    #BoxList_united_copy=BoxList_united
    for i in range(len(BoxList_united_copy)-1):
        BoxList_i=BoxList_united_copy[i]
        box1=[x1,x2]=[BoxList_i[0],BoxList_i[0]+BoxList_i[2]]
        for j in range(i+1,len(BoxList_united_copy)):
            BoxList_j=BoxList_united_copy[j]
            box2=[x3,x4]=[BoxList_j[0],BoxList_j[0]+BoxList_j[2]]
            box3=np.array(box1)-np.array(box2)
            if abs(box3[0])<5:
                box3[0]=0
            if abs(box3[1])<5:
                box3[1]=0
            if box3[0]*box3[1]<=0:
                if i not in index_save:
                    index_save.append(i)
                if j not in index_save:
                    index_save.append(j)
                box_list=[min(BoxList_i[0],BoxList_j[0]),min(BoxList_i[1],BoxList_j[1]),max(BoxList_i[2],BoxList_j[2]),BoxList_i[3]+BoxList_j[3]]
                BoxList_united_return.append(box_list)
                break
    for index in index_save:
        BoxList_del_return.append(BoxList_united[index])

    return [BoxList_del_return,BoxList_united_return]

def BoxList_united_process_x(BoxList_united):
    index_save=[]
    BoxList_del_return=[]
    BoxList_united_return=[]
    BoxList_united_copy=copy.copy(BoxList_united)
    for i in range(len(BoxList_united_copy)-1):
        BoxList_i=BoxList_united_copy[i]
        box1=[y1,y2]=[BoxList_i[1],BoxList_i[1]+BoxList_i[3]]
        for j in range(i+1,len(BoxList_united_copy)):
            BoxList_j=BoxList_united_copy[j]
            box2=[y3,y4]=[BoxList_j[1],BoxList_j[1]+BoxList_j[3]]
            box3=np.array(box1)-np.array(box2)
            if abs(box3[0])<5:
                box3[0]=0
            if abs(box3[1])<5:
                box3[1]=0
            if box3[0]*box3[1]<=0:
                if i not in index_save:
                    index_save.append(i)
                if j not in index_save:
                    index_save.append(j)
                    box_list=[min(BoxList_i[0],BoxList_j[0]),min(BoxList_i[1],BoxList_j[1]),BoxList_i[2]+BoxList_j[2],max(BoxList_i[3],BoxList_j[3])]
                BoxList_united_return.append(box_list)
                break
    for index in index_save:
        BoxList_del_return.append(BoxList_united[index])

    return [BoxList_del_return,BoxList_united_return]

def Image_Retrain_Imwrite(srcImage,studentImage_retrain):
    dir_path='Image_Retrain/'
    txt_path='Image_Retrain_txt/'
    count=1
    flag=1
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        for name in os.listdir(dir_path):
            os.remove(dir_path+name)
    if not os.path.exists(txt_path):
        os.mkdir(txt_path)
    else:
        for name in os.listdir(txt_path):
            os.remove(txt_path+name)
    img=cv2.imread(srcImage)
    (rows,cols)=img.shape[0:2]
    fp=open(txt_path+str(flag)+'.txt','w')
    for box in studentImage_retrain:
        [x,y,w,h]=box
        filename=str(x)+'_'+str(y)+'.png'
        filepath=dir_path+filename
        if count>3:
        	count=1
        	fp.close()
        	flag+=1
        	fp=open(txt_path+str(flag)+'.txt','w')
        count+=1
        fp.write(filepath+'\n')
        img_tmp=np.zeros((200,200,3),dtype=np.uint8)
        if h>200:
            h=200
        if w>200:
            w=200
        img_tmp[:h,:w]=img[y:y+h,x:x+w]
        cv2.imwrite(filepath,img_tmp)
    fp.close()

def ImageUnited(srcImage,ImagePath,heigth_split_num,width_split_num,piex_thresh):
    student_number=0
    studentImage_retrain=[]
    img=cv2.imread(srcImage)
    img_united=np.zeros(img.shape,dtype=np.uint8)
    (rows,cols)=img.shape[0:2]
    print (rows,cols)
    pattern='.png'
    BoxData_special={}
    for filename in os.listdir('Student_Image_Split/'):
        if filename is not None:
            os.remove('Student_Image_Split/'+filename)
    for filename in os.listdir('ImageRetrain_results/'):
        if filename is not None:
            os.remove('ImageRetrain_results/'+filename)
    for filename in os.listdir(ImagePath):
        #print filename
        match=re.search(pattern,filename)
        if match is not None and len(filename.split('.')[0])==2:
            BoxData={}
            BoxList=[]
            name_split=filename.split('.')[0]
            i=int(name_split)/10-1
            j=int(name_split)%10-1
            Imagefilepath=ImagePath+filename
            Csvfilename=name_split+'.csv'
            CsvfilePath='results/'+Csvfilename
            img_tmp=cv2.imread(Imagefilepath)
            img_tmp_copy=img_tmp.copy()
            fp=open(CsvfilePath)
            r=csv.reader(fp)
            for row in r:
                box=(int(row[1]),int(row[2]),int(row[3]),int(row[4]))
                BoxData[str(row[0])]=box
            for key in BoxData:
                (x,y,w,h)=BoxData[key]     
                if w*h>15000:
                    continue                
                [left,right,top,bot]=[x,x+w,y,y+h]
                if left<piex_thresh or abs(right-cols/width_split_num)<piex_thresh or top<piex_thresh or abs(bot-rows/heigth_split_num)<piex_thresh:
                    BoxList.append([x+j*cols/width_split_num,y+i*rows/heigth_split_num,w,h])
                    continue
                if w*h>5000 and i<(heigth_split_num/2):
                    print [x+j*cols/width_split_num,y+i*rows/heigth_split_num,w,h]
                    studentImage_retrain.append([x+j*cols/width_split_num,y+i*rows/heigth_split_num,w,h])
                    continue
                student_number+=1
                student_file_save_path='Student_Image_Split/'+str(student_number)+'.png'
                cv2.imwrite(student_file_save_path,img_tmp_copy[y:y+h,x:x+w])
                cv2.rectangle(img_tmp,(x,y),(x+w,y+h),(0,0,255),1)
            BoxData_special[name_split]=BoxList
            cv2.imwrite(ImagePath+'rectangle'+filename,img_tmp)
            # cv2.imshow(Imagefilepath,img_tmp)
            img_united[i*(rows/heigth_split_num):(i+1)*(rows/heigth_split_num),j*(cols/width_split_num):(j+1)*(cols/width_split_num)]=img_tmp
    for ii in range(width_split_num-1):
        cv2.line(img_united,(cols*(ii+1)/width_split_num,0),(cols*(ii+1)/width_split_num,rows),(0,255,0),1)
    for jj in range(heigth_split_num-1):
        cv2.line(img_united,(0,rows*(jj+1)/heigth_split_num),(cols,rows*(jj+1)/heigth_split_num),(0,255,0),1) 

    BoxData_special_return=BoxData_special_process(BoxData_special,rows,cols,heigth_split_num,width_split_num,piex_thresh)
    for key in BoxData_special_return:
        BoxData_array_tmp=BoxData_special_return[key]
        for box_list in BoxData_array_tmp:
            if box_list==[]:
                continue
            [x,y,w,h]=box_list
            if x>cols:
                x=cols
            if y>rows:
                y=rows
            if x+w>cols:
                w=cols-x
            if y+h>rows:
                h=rows-y
            if w*h>7000 and (y+h/2)>rows/2:
                print box_list
                studentImage_retrain.append(box_list)
                continue
            if w*h>4000 and (y+h/2)<rows/2:
                print box_list
                studentImage_retrain.append(box_list)
                continue
            student_number+=1
            cv2.rectangle(img_united,(x,y),(x+w,y+h),(0,0,255),1)
    Image_Retrain_Imwrite(srcImage,studentImage_retrain)
    # cv2.imshow('img_united.png',img_united)
    print 'The first count is:%d'%(student_number)
    if os.path.exists("studentnumber_save.txt"):
        os.remove("studentnumber_save.txt")
    with open('studentnumber_save.txt','w') as f:
        f.write(str(student_number)+'\n')
    if os.path.exists("img_united.png"):
        os.remove("img_united.png")
    cv2.imwrite('img_united.png',img_united)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return BoxData_special


#this is main
srcImage=str(sys.argv[1])
heigth_split_num=int(sys.argv[2])
width_split_num=int(sys.argv[3])   

ImageUnited(srcImage,'Image_Split/',heigth_split_num,width_split_num,4)

                    

    
