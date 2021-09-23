import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:zzYYDS9900@kitchen.5hpbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# database
db = client.kitchen 

user = db.user
# add
user.insert_one({"name":"shabi", "email":"dashabi@qq.com"})
# delete
user.delete_one({"name":"shabi"})
# change
user.find_and_modify({"name":"shabi"}, {"name":"shabi", "email":"zhenshabi@qq.com"})
# change a field.
user.update_one({'name':'shabi'}, {'$set':{'email':'nishabi'}})
# check
user.find_one({"name":"shh"}) 

user.find_one({ "name": { "$regex": "^s" }})


tmp_doc = user.find_one({'name':'shh'})
tmp_id = tmp_doc['_id'] 
user.find_one('_id', tmp_id) 
# https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html