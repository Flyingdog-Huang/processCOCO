import json

json_file='20211216墙.json'
total_area=0.0
wall_area=0.0
main_wall_area=0.0
with open(json_file,'rb') as file_in : 
    json_data=json.load(file_in)
    ann_list=json_data['annotations']
    img_list=json_data['images']
    for ann in ann_list:
        height=0
        width=0
        for img_inf in img_list:
            if img_inf['id']==ann['image_id']:
                height=img_inf['height']
                width=img_inf['width']
                break
        area=height*width
        area_ann=ann['area']
        p_ann=area_ann/area
        total_area+=p_ann
        if ann['category_id']=='4DPPJ':
            main_wall_area+=p_ann
        else:
            wall_area+=p_ann
file_in.close()
print('total_area',total_area)
print('wall_area',wall_area)
print('main_wall_area',main_wall_area)