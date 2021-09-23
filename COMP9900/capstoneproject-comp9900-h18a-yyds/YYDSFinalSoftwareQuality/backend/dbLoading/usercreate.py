import csv
from util.database import *
from util.helpers import *
from configs.collection_names import *
import time
from random import randint

db = DB()

file = r'users.txt'
uname = 'user'

index = 10
pword = 'zzbeautiful'
mail = '@gmail.com'

while (index <100) :

    uid = generate_uuid()

    db.insert_one_to_collection(USERS,
        _id=uid,
        username=uname + str(index),
        email=uname + str(index)+mail,
        password=pword,
        recipe_num = 0,
        following_num = 0,
        follower_num = 0,
        liked_num = 0
    )

    db.insert_one_to_collection(FOLLOWINGS,
        user_id=uid,
        followings=[]
    )

    db.insert_one_to_collection(FOLLOWERS,
        user_id=uid,
        followers=[]
    )
    db.insert_one_to_collection(LIKES,
        user_id=uid,
        likes_list=[],
        author_count=[]
    )
    db.insert_one_to_collection(USER_RECIPES,
        user_id=uid,
        recipe_list=[]
    )
    db.insert_one_to_collection(RATES, 
        user_id=uid,
        rates_list=[]
    )

    index += 1

    with open(file, 'a+') as f:
        f.write('{}\n'.format(uid))
    
    print('user {} created\n'.format(uid))
