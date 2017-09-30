import os
import numpy as np 
student_num=0
with open('studentnumber_save.txt','rb') as fp:
    for line in fp.readlines():
        student_num+=int(line)
print 'the number of student is:'+str(student_num)