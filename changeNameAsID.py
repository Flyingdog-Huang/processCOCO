# change img name as ID and copy file to img
import os
import json
import shutil

source_path='./source/'
filenames = os.listdir(source_path)
img_path='./img/'
nameId='name_id.json'
# print(filenames)
# test_num=0
with open(nameId,'rb') as nameIdFile:
    nameIdMap=json.load(nameIdFile)
    # print(type(nameIdMap))
    for filename in filenames:
        # print(filename)
        if filename in nameIdMap:
            # test_num+=1
            id_str=str(nameIdMap[filename])
            # print(type(id_str))
            shutil.copy(os.path.join(source_path,filename),os.path.join(img_path,id_str+'.png'))
            print('copy source {} to img {}.png. '.format(filename,id_str))
nameIdFile.close()
# print(test_num)