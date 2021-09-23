import re

from pymongo import cursor
from util.database import *
from util.helpers import *
from configs.collection_names import *
from random import randint

db = DB()

# uid = generate_uuid()
# db.insert_one_to_collection('tests',
#     _id = uid,
#     content='woshab',
#     end='asidjaosdbai'
# )

#print(db.delete_one_from_collection('tests','content','nishab'))
#res = db.get_one_using_query(USER_RECIPES,{'user_id': '05cc9eded27d11ebb2c955fa17dcadb1', 'recipe_list.recipe_id':'c2cfc218d27d11ebb2c955fa17dcadb1'})
#print(res['user_id'])
# res =db.update_nested_fields_values(USER_RECIPES, 'recipe_list.recipe_id','c2cfc218d27d11ebb2c955fa17dcadb1',{'recipe_list.$.liked_num':1})
# print(res)
#res = db.get_one_projected_using_query(RATES, {'user_id': 'd46d8690d2ff11eb9593fdd54a311815', 'rates_list.recipe_id':'d8cff874d30111eb9593fdd54a311815'}, {'_id':0, 'rates_list': {'$elemMatch': {'recipe_id': "d8cff874d30111eb9593fdd54a311815"}}})
#cursor = db._db.recipes.aggregate([{ "$search": {"text": { "query": "大肠", "path": "ingredients"} } }, {"$project": {"title": 1} } ])
# aggregate里面是个pipline, 放了一串你要干啥。
# cursor = db._db.recipes.aggregate([{'$search': {'index': 'default','text': {'query': '智障','path': {'wildcard': '*'}}}}, {"$project": {"title": 1,'meal_type':1,'ingredients':1 ,'_id':0} }])
# res = {'res':[]}
# res['res'].extend(cursor)
# print(res)
# for x in res:
#     print(x,',', type(x))
# https://stackoverflow.com/questions/65117055/pymongo-atlas-search-not-returning-anything

#db.pop_from_nested_array(USER_RECIPES, 'recipe_list', 'user_id', '72f7d82cd2fd11eb9593fdd54a311815', recipe_id='d04bc476d30111eb9593fdd54a311815')

# print(db.get_one_from_collection('meal_types', 'default', 'all'))



# cursor = db.search_by_range(RECIPES, 1,None, 10, {'_id':1, 'liked_num':1}, {'liked_num':-1})
# res = {'res':[]}
# res['res'].extend(cursor)
# print(res)
# for x in res:
#     print(x,',', type(x))



cursor = db.search_by_range(RECIPES, 1, None, 100, {'_id': 1, 'liked_num': 1})
pool = []
pool.extend(cursor)
n = len(pool)
res = {'res': []}

picks = []
for _ in range(10):
    i = randint(0, n-1)
    while i in picks:
        i = randint(0, n-1)
    picks.append(i)

for i in picks:
    res['res'].append(pool[i])

print(res)