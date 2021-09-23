import os
import sys
import pymongo

# connect to mongodb server
client = pymongo.MongoClient("mongodb+srv://admin:zzYYDS9900@kitchen.5hpbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# database
db = client.kitchen 
# collection == table
user = db.user

out = sys.stdout
sys.stdout = open("help.txt", "w")
 
help(user)
 
sys.stdout.close()
sys.stdout = out