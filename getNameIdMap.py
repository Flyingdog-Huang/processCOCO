# - get all img name
from pathlib import Path
import os
import glob
from os import listdir
from os.path import splitext

img_path='./source/'
images_dir=Path(img_path)
name_list=[file for file in listdir(images_dir) if file.endswith('.png') or file.endswith('.jpg')]
# print(name_list)

# - get img-id map from json
import json

id_map={}
json_file='20211216墙.json'
with open(json_file,'rb') as file_in : 
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
# print('id_map',id_map)  
# print('len_id_map',len(id_map))           
# 保存name-id map到接送文件
name_id_json=json.dumps(id_map)
with open('name_id.json','w') as name_id_oj:
    name_id_oj.write(name_id_json)
name_id_oj.close()