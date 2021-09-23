from app import db, api, cache
from flask_restx import Resource, abort
from util.request_handling import *
from util.helpers import *
from configs.collection_names import *

search = api.namespace('searches', description='searches service')


@search.route('/', endpoint='searches', strict_slashes=False)
class Search(Resource):
    @search.response(200, 'Success')
    @search.param('ingredients', 'search in specific ingredients')
    @search.param('meal_type', 'search within selected types')
    @search.param('method', 'key words in method')
    @search.param('title', 'key words in recipe title')
    @cache.memoize(timeout=120)
    @search.doc(description="Search in combinations of title, methods, meal types and ingredients")
    def get(self):
        query_title = get_request_arg('title')
        query_methods = get_request_arg('methods')
        query_meal_type = get_request_arg('meal_type')
        query_ingredients = get_request_arg('ingredients')
        queries = {
            'title': query_title if query_title != None else None,
            'methods': query_methods if query_methods != None else None,
            'meal_type': query_meal_type.split(' ') if query_meal_type != None else None,
            'ingredients': query_ingredients.split(' ') if query_ingredients != None else None,
        }
        # if the query is None, search within the entire range,
        # which means the key will not be defined in the value of must
        musts = []
        for field in queries.keys():
            if (queries[field] == None):
                continue

            # replace underline with blank space in the element
            if (type(queries[field]) != str):  # deal with meal_type and ingredients
                queries[field] = [x.replace("_", " ") for x in queries[field]]
            else:  # deal with method and title
                queries[field] = queries[field].replace("_", " ")

            if field == 'title':
                # search within string
                musts.append({
                    'text': {
                        'query': queries[field],
                        'path': field
                    }
                })
            elif field == 'meal_type':
                for tp in queries[field]:
                    musts.append({
                        'text': {
                            'query': tp,
                            'path': 'meal_type'
                        }
                    })
            else:
                # search with in arrays
                musts.append({
                    'text': {
                        'query': queries[field],
                        'path': {"wildcard": "{}.*".format(field)}
                    }
                })
        cursor = db.search_on_multiple_fields(musts, {'_id': 1})
        res = {'res': []}
        res['res'].extend(cursor)
        return res
