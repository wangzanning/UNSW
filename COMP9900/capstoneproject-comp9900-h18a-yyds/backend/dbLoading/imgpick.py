import base64
import os
from random import randint

dirName = './img'
imgList = os.listdir(dirName)
n = len(imgList)

rand_img = imgList[randint(0,n-1)]

with open(dirName+'/'+rand_img, 'rb') as f:
    image_data = f.read()
    base64_data = base64.b64encode(image_data)  # base64编码
    base64_data = str(base64_data)[2:]

    img_type = rand_img.split('.')[-1]
    prefix = 'data:image/{};base64,'.format(img_type)
    base64_data = prefix + base64_data
    print(base64_data)
    print(type(base64_data))
