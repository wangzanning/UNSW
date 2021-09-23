from pymongo import MongoClient
import certifi
class DB():
    def __init__(self):
        self._client = MongoClient(
            "mongodb+srv://admin:zzYYDS9900@kitchen.5hpbe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())
        self._db = self._client.kitchen

    def select_table(self, collection):
        self._collection = collection
        return self

    def query(self, **kargs):
        self._query = kargs
        return self

    def get_one_from_collection(self, collection: str, query_key: str, query_value):
        return self._db[collection].find_one({query_key: query_value})

    def get_one_in_nested_array(self, collection: str, query_key: str, **kwargs):
        # querying something in a nested array
        # db.inventory.find( { "instock": { $elemMatch: { qty: 5, warehouse: "A" } } } )
        return self._db[collection].find_one({query_key: {'$elemMatch': kwargs}})

    def get_one_and_project(self, collection: str, filter: dict, projection: dict):
        return self._db[collection].find(filter, projection)

    def get_one_using_query(self, collection: str, query: dict):
        return self._db[collection].find_one(query)

    def get_one_projected_using_query(self, collection: str, query: dict, project: dict):
        # db.inventory.find( { status: "A" }, { status: 1, instock: 1, _id: 0} )
        return self._db[collection].find_one(query, project)

    def delete_one_from_collection(self, collection: str, query_key: str, query_value):
        # 测试通过
        return self._db[collection].delete_one({query_key: query_value})

    def update_one_from_collection(self, collection: str, query_key: str, query_value, **kwargs):
        return self._db[collection].update_one({query_key: query_value}, {'$set': kwargs})
        # return self._db[collection].find_one({query_key: query_value})

    def update_one_using_dict(self, collection: str, query_key: str, query_value, newDict: dict):
        return self._db[collection].update_one({query_key: query_value}, {'$set': newDict})
        # self._db[collection].find_one({query_key: query_value})

    def update_nested_array(self, collection, query: dict, update: dict):
        return self._db[collection].update_one(query, {'$set': update}, True)

    def update_fields_values(self, collection: str, query_key: str, query_value, **kwargs):
        return self._db[collection].update_one({query_key: query_value}, {'$inc': kwargs})

    def update_nested_fields_values(self, collection: str, query: dict, items: dict):
        # item example: {'recipe_list.$.liked_num':-1}
        # db.update_nested_fields_values(USER_RECIPES, 'recipe_list.recipe_id', target, {'recipe_list.$.liked_num':-1})
        return self._db[collection].update_one(query, {'$inc': items}, upsert=True)

    def update_fields_in_array(self, collection: str, query: dict, update: dict):
        return self._db[collection].update_one(query, {'$set': update})

    def push_many_into_array(self, collection: str, array_name: str, query_key: str, query_value, items: list):
        n = len(items)
        if not n:
            return
        if n == 1:
            return self._db[collection].update_one({query_key: query_value}, {'$push': {array_name: items[0]}})
        return self._db[collection].update_one({query_key: query_value}, {'$addToSet': {array_name: {'$each': items}}}, upsert=True)
        # return self._db[collection].find_one({query_key: query_value})

    def pop_many_from_array(self, collection: str, array_name: str, query_key: str, query_value, items: list):
        return self._db[collection].update_one({query_key: query_value}, {'$pullAll': {array_name: items}})
        # return self._db[collection].find_one({query_key: query_value})

    def pop_from_nested_array(self, collection: str, array_name: str, query_key: str, query_value, **kwargs):
        return self._db[collection].update_one({query_key: query_value}, {'$pull': {array_name: kwargs}})

    def insert_one_to_collection(self, collection, **kwargs):
        return self._db[collection].insert_one(kwargs)

    def insert_one_using_dict(self, collection, payload: dict):
        return self._db[collection].insert_one(payload)

    def search_by_ingredients(self, query, limit):
        # {"$project": {"title": 1,'meal_type':1,'ingredients':1 ,'_id':0}}
        return self._db.recipes.aggregate([
            {
                '$search': {
                    'index': 'default',
                    'text': {
                        'query': query,
                        'path': {"wildcard": "{}.*".format('ingredients')}
                    }
                }
            },
            {
                '$limit': limit
            },
            {
                "$project": {
                    '_id': 1,
                }
            }
        ])

    def search_on_multiple_fields(self, musts: list, project: dict, sort=None):
        # compound, muitple
        # Document of how to apply compound is in tht following link
        # https://docs.atlas.mongodb.com/reference/atlas-search/compound/#std-label-compound-ref
        pipline = [{
            '$search': {
                'index': 'default',
                "compound": {
                    "must": musts
                }
            }
        },
            {
            "$project": project
        }]
        if sort:
            # https://docs.mongodb.com/manual/reference/operator/aggregation/sort/)
            pipline.append({'$sort': sort})

        return self._db.recipes.aggregate(pipline)

    def search_by_range(self, collection: str, greater: int, less: int, limit: int, project: dict, sort=None):
        range = {'path': 'liked_num'}
        if greater:
            range['gte'] = greater
        if less:
            range['lte'] = less

        pipline = [
            {
                '$search': {
                    "index": "likes",
                    "range": range
                }
            },
            {
                '$limit': limit
            },
            {
                '$project': project
            }
        ]
        if sort:
            pipline.append({'$sort': sort})
        return self._db[collection].aggregate(pipline)
