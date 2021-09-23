from configs.collection_names import RECIPES, USER_RECIPES
from util.database import *
from random import randint
db = DB()

superVs = [ 'eb35b81adafd11eb892559354efcec79',
            '31f9a248dafe11eb892559354efcec79', 
            '4f31261adafe11eb892559354efcec79',
            '81a431bedafe11eb892559354efcec79',
            '9f0cf330dafe11eb892559354efcec79',
            'e1c10018dafe11eb892559354efcec79',
            'f014d838dafe11eb892559354efcec79',
            '0010aba4daff11eb892559354efcec79',
            '17f78c60daff11eb892559354efcec79',
            '609a46ecdaff11eb892559354efcec79']

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

total = 0
for uid in superVs:
    rids = db.get_one_from_collection(USER_RECIPES, 'user_id', uid)['recipe_list']
    print('now user ', uid, '\n')
    for r in rids:
        rid = r['recipe_id']
        total += 1
        db.update_one_from_collection(RECIPES, '_id', rid, meal_type=[meal_types[randint(0,len(meal_types)-1)]])
        if total % 100 == 0:
            print('now {} recipe edited'.format(total))

print('totally {} recipe edited'.format(total))