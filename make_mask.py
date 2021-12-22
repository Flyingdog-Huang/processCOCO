# change img name as ID
from pathlib import Path
import os
import glob
from os import listdir
from os.path import splitext
import json
import cv2
import numpy as np
from numpy.lib.function_base import delete

# get annotations 
label_name='20211216墙.json'
ann_list=[]
idsize_list=[]
with open(label_name,'rb') as label_file : 
    json_data=json.load(label_file)
    ann_list=json_data['annotations']
    img_list=json_data['images']
    for i in range(len(img_list)):
        id_size={}
        img_inf=img_list[i]
        id_size['id']=img_inf['id']
        id_size['height']=img_inf['height']
        id_size['width']=img_inf['width']
        idsize_list.append(id_size)
label_file.close()
# print(ann_list)
# print(len(idsize_list))

# make mask
def changePointStyle(points):
    x_list=[]
    y_list=[]
    new_points=[]
    num_points=len(points)
    for i in range(num_points):
        if i%2==0:
            x_list.append(points[i])
        else:
            y_list.append(points[i])
    num_points=len(x_list)
    for i in range(num_points):
        point=[x_list[i],y_list[i]]
        new_points.append(point)
    new_points=np.array(new_points)
    return new_points

nameId='name_id.json'
wall_color=[0,255,0] # G color
main_wall_color=[0,0,255] # R color
delete_char='[]'
mask_path='./mask/'
check_path='./check/'
img_path='./img/'
with open(nameId,'rb') as nameIdFile:
    nameIdMap=json.load(nameIdFile)
    for filename in nameIdMap:
        # print(nameIdMap[filename])
        id=nameIdMap[filename]
        # get img size
        height=0
        width=0
        for imgsize in idsize_list:
            if id==imgsize['id']:
                height=imgsize['height']
                width=imgsize['width']
                break
        img_name=str(id)+'.png'
        img=cv2.imread(img_path+img_name)
        # check img size
        if height==0 or width==0 or height!=img.shape[0] or width!=img.shape[1]:
            print('wrong img size!')
            print('filename',filename)
            print('id',id)
            print('json: height width - ',height,width)
            print('img: height width - ',img.shape[0],img.shape[1])
            continue
        id_mask=np.zeros((height,width,3),np.uint8)
        for ann in ann_list:
            if ann['image_id']==id:
                # print(type(ann['segmentation']))
                wall_class=ann['category_id']
                segmentation=ann['segmentation']
                for de_char in delete_char:
                    segmentation=segmentation.replace(de_char,'')
                segmentation=segmentation.split(',')
                for position in range(len(segmentation)):
                    segmentation[position]=int(float(segmentation[position]))
                segmentation=changePointStyle(segmentation)
                # print(type(segmentation))
                color=wall_color
                if wall_class=="4DPPJ":
                    color=main_wall_color
                cv2.drawContours(id_mask,[segmentation],0,color,-1)
                # if len(segmentation)%2!=0: print(segmentation)
                # print(type(segmentation[0]))
        mask_name=str(id)+'_mask.png'
        check_name=str(id)+'_check.png'
        check_img=img+id_mask//2
        cv2.imwrite(mask_path+mask_name,id_mask)
        cv2.imwrite(check_path+check_name,check_img)
        print(mask_name+' and '+check_name+' finish ! ')
nameIdFile.close()

'''
with open(json_file,'rb') as label_file : 
    json_data=json.load(file_in)
    images_json=json_data['images']
    num_img_json=len(images_json)
    for file_name in name_list:
        for i in range(num_img_json):
            if file_name==images_json[i]['file_name']:
                id=images_json[i]['id']
                id_map[file_name]=id
                break
file_in.close()


img_path='./source/'
images_dir=Path(img_path)
name_list=[file for file in listdir(images_dir) if file.endswith('.png') or file.endswith('.jpg')]
# print(name_list)
id_map={}


# print('id_map',id_map)  
# print('len_id_map',len(id_map))           
# 保存name-id map到接送文件
name_id_json=json.dumps(id_map)
with open('name_id.json','w') as name_id_oj:
    name_id_oj.write(name_id_json)
name_id_oj.close()



# read imgs one by one and save as id name


from matplotlib import pyplot as plt


# img=cv2.imread(str(img_file_list[0]))
# out_json='wall_label.json'
# test read
# test_img_name=img_path+'01-平面-空中别墅-3.jpg'
# img=cv2.imread(test_img_name)
# print(img)
# img_file_list=list(images_dir.glob(name_list[0]))
# file_out=open(out_json,'w')

from pycocotools.coco import COCO
from skimage import io





# coco=COCO(json_file)
# catIds=coco.getCatIds(catNms=['承重墙'])
# imgIds=coco.getImgIds(catIds=catIds)
# for i in range(len(imgIds)):
#     img=coco.loadImgs(imgIds[i])[0]
#     I=io.imread(img_path+img['file_name'])
#     plt.axis('off')
#     plt.imshow(I) 
#     annIds=coco.getAnnIds(imgIds=img['id'],catIds=catIds,iscrowd=None)
#     anns=coco.loadAnns(annIds)
#     coco.showAnns(anns)
#     plt.show()


# images_dir=Path(img_path)
# name_list=[file for file in listdir(images_dir) if file.endswith('.png') or file.endswith('.jpg')]
# print(name_list[0])
# # num_imgs=len(name_list)
# # num_check=0
# # for i in name_list:
# #     img=cv2.imread(str(images_dir)+i)
# #     if img:num_check+=1
# # print(num_imgs==num_check)
# # print(num_check)
# img=cv2.imread(img_path+name_list[0])
# print(img)
# cv2.imshow(img)

# cv2.waitKey(0)
'''