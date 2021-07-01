import os, re
import numpy as np
import shutil as sh
srcPath1 = "/home/sungyeon/ACL/capstone_morai_dataset2/CAMERA_2"
srcPath = "/home/sungyeon/ACL/capstone_morai_dataset2/CAMERA_1"

dstPath = "/home/sungyeon/ACL/capstone_morai_dataset2/edit"
try:
    os.mkdir(dstPath)
except:
    print('1')


image_width=640
image_height=480

fileList = os.listdir(srcPath1)
print(fileList)
for fileName in fileList:
    if '.txt' in fileName:
        error_flag=0
        srcFilePath = os.path.join(srcPath1, fileName)
        dstFilePath = os.path.join(dstPath, fileName[:-4]+'_'+srcPath[-8:]+'.txt')
        #print(f'From {srcFilePath}', end='')
        
        label_to_list = []
        edited_list = []
        print(srcFilePath)
        with open(srcFilePath, 'r', encoding="utf-8") as fr:
            labelList = fr.read().split('\n')[:-1]
            #print(labelList)
            #print(len(labelList))
            for i in range(len(labelList)) :
                label_to_list.append(labelList[i].split(' '))
            #print(label_to_list)은
            x1list=[];x2list=[];y1list=[];y2list=[]
            
            
            # Label text to id number
            for i in range(len(labelList)) :
                if str(label_to_list[i][0])=='Vehicle':
                    label_to_list[i][0]='0'
                
                # Exceptional
                x1=float(label_to_list[i][4]); x2=float(label_to_list[i][6])
                y1=float(label_to_list[i][5]); y2=float(label_to_list[i][7])
                
                
                dx=x2-x1
                dy=y2-y1
                print(dx); print(dy)
                if dy/(dx+1e-8)<2 and dy/(dx+1e-8)>1/3.5: 
                    x1list.append(x1);
                    y1list.append(y1);
                    x2list.append(x2);
                    y2list.append(y2);


                    edited_list.append(\
                        str(label_to_list[i][0])+str(' ')\
                        +str((x1+x2)/2/image_width)+str(' ')\
                        +str((y1+y2)/2/image_height)+str(' ')\
                        +str((x2-x1)/image_width)+str(' ')\
                        +str((y2-y1)/image_height))
            
        if edited_list==[]:
            continue
        excludeidx=[0]*len(x1list)
        for i in range(len(x1list)):
            for j in range(len(x1list)):
                if x1list[j]<=x1list[i] and x2list[i]<=x2list[j] and y1list[j]<=y1list[i] and y2list[i]<=y2list[j] and i!=j:
                    excludeidx[i]=1
                
                    
        

        # edited_list=list(set(edited_list))
        with open(dstFilePath, 'w') as fw:
            for i in range(len(edited_list)):
                if excludeidx[i]==0:
                    fw.write(edited_list[i]+'\n') 

        imagename=fileName[:-4]+'.png'
        image1name=fileName[:-4]+'.png'
        copyimagename=fileName[:-4]+'_'+srcPath[-8:]+'.png'
        copyimage1name=fileName[:-4]+'_'+srcPath[-8:]+'.png'

        # image for training
        srcImagePath = os.path.join(srcPath, imagename)
        dstImagePath = os.path.join(dstPath, copyimagename)
        sh.copy(srcImagePath, dstImagePath)

        # annotation image
        # srcImage1Path = os.path.join(srcPath1, image1name)
        # dstImage1Path = os.path.join(dstPath, copyimage1name)
        # sh.copy(srcImage1Path, dstImage1Path)
