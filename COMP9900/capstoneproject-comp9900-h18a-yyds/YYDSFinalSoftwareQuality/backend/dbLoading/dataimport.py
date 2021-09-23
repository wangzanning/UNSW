import csv
from util.database import *
from util.helpers import *
from configs.collection_names import *
import time
from random import randint
import base64
import os


db = DB()

superVs = [
'3fbd727dedfc11eba3592f2591537b69',
'3fbd727eedfc11eba3592f2591537b69',
'3fbd727fedfc11eba3592f2591537b69',
'3fbd7280edfc11eba3592f2591537b69',
'3fbd7281edfc11eba3592f2591537b69',
'40f0867aedfc11eba3592f2591537b69',
'40f0867bedfc11eba3592f2591537b69',
'40f0867cedfc11eba3592f2591537b69',
'40f0867dedfc11eba3592f2591537b69',
'8c2508c8edfc11eba3592f2591537b69',
'8c2508c9edfc11eba3592f2591537b69',
'8d2b62e4edfc11eba3592f2591537b69',
'8d2b62e5edfc11eba3592f2591537b69',
'8d2b62e6edfc11eba3592f2591537b69',
'8d2b62e7edfc11eba3592f2591537b69',
'8d2b62e8edfc11eba3592f2591537b69',
'8d2b62e9edfc11eba3592f2591537b69',
'8d2b62eaedfc11eba3592f2591537b69',
'8e55c650edfc11eba3592f2591537b69',
'8e55c651edfc11eba3592f2591537b69',
'8e55c652edfc11eba3592f2591537b69',
'8e55c653edfc11eba3592f2591537b69',
'8e55c654edfc11eba3592f2591537b69',
'8e55c655edfc11eba3592f2591537b69',
'8e55c656edfc11eba3592f2591537b69',
'8e55c657edfc11eba3592f2591537b69',
'8fa891aeedfc11eba3592f2591537b69',
'8fa891afedfc11eba3592f2591537b69',
'8fa891b0edfc11eba3592f2591537b69',
'8fa891b1edfc11eba3592f2591537b69',
'8fa891b2edfc11eba3592f2591537b69',
'8fa891b3edfc11eba3592f2591537b69',
'8fa891b4edfc11eba3592f2591537b69',
'90bac12aedfc11eba3592f2591537b69',
'90bac12bedfc11eba3592f2591537b69',
'90bac12cedfc11eba3592f2591537b69',
'90bac12dedfc11eba3592f2591537b69',
'90bac12eedfc11eba3592f2591537b69',
'90bac12fedfc11eba3592f2591537b69',
'90bac130edfc11eba3592f2591537b69',
'92073d2eedfc11eba3592f2591537b69',
'92073d2fedfc11eba3592f2591537b69',
'92073d30edfc11eba3592f2591537b69',
'92073d31edfc11eba3592f2591537b69',
'92073d32edfc11eba3592f2591537b69',
'92073d33edfc11eba3592f2591537b69',
'92073d34edfc11eba3592f2591537b69',
'92073d35edfc11eba3592f2591537b69',
'9335f848edfc11eba3592f2591537b69',
'9335f849edfc11eba3592f2591537b69',
'9335f84aedfc11eba3592f2591537b69',
'9335f84bedfc11eba3592f2591537b69',
'9335f84cedfc11eba3592f2591537b69',
'9335f84dedfc11eba3592f2591537b69',
'9335f84eedfc11eba3592f2591537b69',
'94504760edfc11eba3592f2591537b69',
'94504761edfc11eba3592f2591537b69',
'94504762edfc11eba3592f2591537b69',
'94504763edfc11eba3592f2591537b69',
'94504764edfc11eba3592f2591537b69',
'94504765edfc11eba3592f2591537b69',
'94504766edfc11eba3592f2591537b69',
'94504767edfc11eba3592f2591537b69',
'957e13e2edfc11eba3592f2591537b69',
'957e13e3edfc11eba3592f2591537b69',
'957e13e4edfc11eba3592f2591537b69',
'957e13e5edfc11eba3592f2591537b69',
'957e13e6edfc11eba3592f2591537b69',
'957e13e7edfc11eba3592f2591537b69',
'957e13e8edfc11eba3592f2591537b69',
'957e13e9edfc11eba3592f2591537b69',
'96cbb72cedfc11eba3592f2591537b69',
'96cbb72dedfc11eba3592f2591537b69',
'96cbb72eedfc11eba3592f2591537b69',
'96cbb72fedfc11eba3592f2591537b69',
'96cbb730edfc11eba3592f2591537b69',
'96cbb731edfc11eba3592f2591537b69',
'96cbb732edfc11eba3592f2591537b69',
'97e2bcf0edfc11eba3592f2591537b69',
'97e2bcf1edfc11eba3592f2591537b69',
'97e2bcf2edfc11eba3592f2591537b69',
'97e2bcf3edfc11eba3592f2591537b69',
'97e2bcf4edfc11eba3592f2591537b69',
'97e2bcf5edfc11eba3592f2591537b69',
'97e2bcf6edfc11eba3592f2591537b69',
'97e2bcf7edfc11eba3592f2591537b69',
'992c88e8edfc11eba3592f2591537b69',
'992c88e9edfc11eba3592f2591537b69',
'992c88eaedfc11eba3592f2591537b69',
'992c88ebedfc11eba3592f2591537b69',
'992c88ecedfc11eba3592f2591537b69',
'992c88ededfc11eba3592f2591537b69',
'992c88eeedfc11eba3592f2591537b69',
'9a5bd868edfc11eba3592f2591537b69',
'9a5bd869edfc11eba3592f2591537b69',
'9a5bd86aedfc11eba3592f2591537b69',
'9a5bd86bedfc11eba3592f2591537b69',
'9a5bd86cedfc11eba3592f2591537b69',
'9a5bd86dedfc11eba3592f2591537b69',
]

lineCount = 0

meal_types = [
    "Chinese cuisine","French cuisine","Italian cuisine","Indian cuisine",
    "Japanese cuisine","Greece cuisine","Spanish cuisine",
    "Thai cuisine","Turkish cuisine","Indonesian cuisine",
    "Korean cuisine","Mongolian cuisine","Filipino cuisine",
    "Malaysian cuisine","Singaporean cuisine","Vietnamese cuisine",
    "Canadian cuisine","American cuisine","Mexican cuisine", "Mediterranean cuisine",
    "Cuisines of the Balkans","Portuguese cuisine","Dutch cuisine","Cuisines of the Islands of the North Atlantic",
    "German cuisine","Central European cuisine","Russian cuisine","Ukrainian cuisine","Caucasian cuisine",
    "Eastern European cuisine","Nordic cuisines","Baltic cuisines",
    "Iranian cuisine","South Caucasus cuisine","Arab cuisine","Pakistani cuisine",
    "Nepalese cuisine","Bangladeshi cuisine","Central Asian cuisine",
    "Central American cuisine","Argentinian cuisine","Colombian cuisine",
    "Brazilian cuisine","Venezuelan cuisine","Caribbean cuisine","Latin American cuisine",
    "Central African cuisine","East African cuisine","North African cuisine","Southern African cuisine",
    "West African cuisine",
]

def getParsedList(array):
    # ['ground beef', 'yellow onions', 'diced tomatoes', 'tomato paste', 'tomato soup', 'rotel tomatoes', 'kidney beans', 'water', 'chili powder', 'ground cumin', 'salt', 'lettuce', 'cheddar cheese']
    
    # ['mix all ingredients& boil for 2 1 / 2 hours , or until thick', 
    # 'pour into jars', 
    # "i use'old' glass ketchup bottles", 
    # "it is not necessary for these to'seal", 
    # "'my amish mother-in-law has been making this her entire life , and has never used a'sealed' jar for this recipe , and it's always been great !"
    # ]
    print(array)
    if array[0] != '[':
        return [array]

    res = []
    l, r, n = 0, 0, len(array)
    while (r<n):
        if array[l] == '[':
            l+=1
            r+=1
        elif array[l] == '\'' :
            l+=1
            r+=1
            while array[r] != '\'':
                if array[r] == '\\' and array[r+1] == '\'':
                    r += 2
                    continue
                r+=1
            res.append(array[l:r])
            l = r+1
            r+=1
        elif array[l] == '\"':
            l+=1
            r+=1
            while array[r] != '\"':
                if array[r] == '\\' and array[r+1] == '\"':
                    r += 2
                    continue
                r+=1
            res.append(array[l:r])
            l = r+1
            r+=1
        else:
            l+=1
            r+=1
    return res


dirName = './img'
imgList = os.listdir(dirName)
n = len(imgList)

with open('dataset/yuki1000.csv','r') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=':')
    for row in csvReader:
        if lineCount<=50:
            lineCount+=1
            continue
        else:
            # row[0] # title
            # row[1] # n steps
            # row[2] # steps, list
            # row[3] # abstract
            # row[4] # ingredient

            rid = generate_uuid()
            uid = superVs[randint(0, len(superVs)-1)]
            now = time.time() * 1000
            
            # randomly pick img
            rand_img = imgList[randint(0,n-1)]
            img = 0
            with open(dirName+'/'+rand_img, 'rb') as f:
                image_data = f.read()
                img = base64.b64encode(image_data)  # base64编码
                img = str(img)[2:-2]

                img_type = rand_img.split('.')[-1]
                prefix = 'data:image/{};base64,'.format(img_type)
                img = prefix + img

            payload = {
                '_id' :rid,
                'author_id':uid,
                'title': row[0],
                'last_modified': now,
                'abstract':row[3],
                'image': img,
                'liked_num':0,
                'rate_sum':0,
                'rate_by':0,
                'meal_type':meal_types[randint(0,len(meal_types)-1)],
                'methods': [ 
                    {
                        'thumbnail':'',
                        'method': item
                    }
                    for item in getParsedList(row[2])
                ],
                'ingredients': [
                    {
                        'ingredient':item,
                        'volume':1,
                        'unit':'serve'
                    }
                    for item in getParsedList(row[4])
                ],
                'comments_pages': []
            }
            for k in payload.keys():
                print(k, ': ', payload[k], '\n')
            print('\n*****************************\n')
    
            db.insert_one_using_dict(RECIPES, payload)
            
            db.push_many_into_array(USER_RECIPES, 'recipe_list','user_id', uid, [{'recipe_id': rid, 'liked_num': 0, 'last_modified': now}])
            
            db.update_fields_values(USERS, '_id', uid, recipe_num=1)
            lineCount += 1
            if lineCount % 100 == 0:
                print('now user ', uid, ', now recipe_n: ', lineCount)
                print('\n', payload, '\n***************\n')
            # if lineCount == 50:
            #     break