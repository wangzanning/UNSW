from app import api, db, cache
from util.helpers import *
from util.models import *
from util.request_handling import *
from flask_restx import Resource, abort, reqparse, fields
from flask import request
from configs.collection_names import *
import time
from configs.default import COMMENT_PAGE_CAPACITY
recipe = api.namespace('recipes', description='CRUD of recipes and comments')


@recipe.route('/', strict_slashes=False)
class Recipe(Resource):
    @recipe.response(200, 'Success', recipes_collection)
    @recipe.response(403, 'Invalid Auth Token')
    @recipe.response(400, 'Malformed Request')
    @recipe.response(404, 'User Not Found')
    @recipe.param('id', 'Id of the recipe')
    @cache.memoize(timeout=10)
    @recipe.doc(description='''
        return the content of a recipe. can be fetched without logging in. 
    ''')
    def get(self):
        rid = get_request_arg('id')
        if not rid:
            abort(400, "require Recipe id")
        res = db.get_one_from_collection(RECIPES, '_id', rid)
        if not res:
            abort(404, "Recipe not found")
        return res

    @recipe.response(200, 'Success', recipes_collection)
    @recipe.response(403, 'Invalid Auth Token')
    @recipe.response(400, 'Malformed Request')
    @recipe.response(404, 'User Not Found')
    @recipe.expect(auth_details, recipes_uploading_details, validate=False)
    @recipe.doc(description='''
        To create a new recipe. 
    ''')
    def post(self):
        j = get_request_json()
        (title, abstract, image, meal_type, methods, ingredients) = unpack(j,
                                                                           'title', 'abstract', 'image', 'meal_type', 'methods', 'ingredients')
        rid = generate_uuid()
        uid = authorize(request)
    
        now = time.time() * 1000
        if not title:
            title = 'Null'
        if not abstract:
            abstract = 'Null'
        if not image:
            image = '0'
        if not meal_type:
            meal_type = 'default'
        if not methods:
            methods = {}
        if not ingredients:
            ingredients = {}
        # time_info = {'date':now.date(), 'time':now.time()}
        db.insert_one_to_collection(RECIPES,
                                    _id=rid,
                                    author_id=uid,
                                    title=title,
                                    last_modified=now,
                                    abstract=abstract,
                                    image=image,
                                    liked_num=0,
                                    rate_sum=0,
                                    rate_by=0,
                                    meal_type=meal_type,
                                    methods=methods,
                                    ingredients=ingredients,
                                    comments_pages=[]
                                    )
        # update post list of a user
        db.push_many_into_array(USER_RECIPES, 'recipe_list', 'user_id', uid, [
                                {'recipe_id': rid, 'liked_num': 0, 'last_modified': now}])
        # update posting number of a user
        db.update_fields_values(USERS, '_id', uid, recipe_num=1)

        return db.get_one_from_collection(RECIPES, '_id', rid)

    @recipe.response(200, 'Success', recipes_collection)
    @recipe.response(403, 'Invalid Auth Token')
    @recipe.response(400, 'Malformed Request')
    @recipe.response(404, 'User Not Found')
    @recipe.param('id', 'Id of recipes to do modification')
    @recipe.expect(auth_details, recipes_collection)
    @recipe.doc(description='''
        To edit a recipe.
    ''')
    def put(self):
        uid = authorize(request)
        request_json = get_request_json()
        rid = get_request_arg('id')
        res = db.get_one_from_collection(RECIPES, '_id', rid)
        if not res:
            abort(404, "Recipe not found")
        now = time.time() * 1000
        request_json['last_modified'] = time.time()*1000
        db.update_one_using_dict(RECIPES, '_id', rid, request_json)
        db.update_nested_array(USER_RECIPES, {'user_id': uid, 'recipe_list.recipe_id': rid}, {
                               'recipe_list.$.last_modified': now})
        return db.get_one_from_collection(RECIPES, '_id', rid)

    @recipe.response(200, 'Success')
    @recipe.response(403, 'Invalid Auth Token')
    @recipe.response(400, 'Malformed Request')
    @recipe.response(404, 'User Not Found')
    @recipe.param('id', 'Id of reciepes to delete')
    @recipe.expect(auth_details)
    @recipe.doc(description='''
        to delete a recipe.
    ''')
    def delete(self):
        uid = authorize(request)
        rid = get_request_arg('id')

        res = db.get_one_from_collection(RECIPES, '_id', rid)
        if not res:
            abort(404, "Recipe not found")

        liked = int(res['liked_num'])
        
        db.delete_one_from_collection(RECIPES, '_id', rid)
        
        db.pop_from_nested_array(
            USER_RECIPES, 'recipe_list', 'user_id', uid, recipe_id=rid)
        
        db.update_fields_values(
            USERS, '_id', uid, recipe_num=-1, liked_num=-liked)
        return {
            'msg': 'Recipes delete success'
        }


@recipe.route('/comment', strict_slashes=False)
class Comment(Resource):
    @recipe.response(200, 'Get comment success')
    @recipe.param('id', 'ID of recipe being commented')
    @recipe.param('page', 'expected page number of comments, start from 1')
    @recipe.doc(description='Get comments of a recipe by recipe ID and page number')
    # @cache.memoize(timeout=2*60)
    def get(self):
        # Get comment page ID of requested recipe
        rid = get_request_arg('id')
        page_no = get_request_arg('page', int)
        comment_pages = db.get_one_from_collection(
            RECIPES, '_id', rid)['comments_pages']
        # If the recipe has not been commented, return no comment
        if (len(comment_pages) == 0):
            return {
                'msg': 'no comment'
            }
        elif (len(comment_pages) < page_no):
            abort(404, 'No such page')
        # Otherwise, get arry of comment ID in requested page
        page_id = comment_pages[page_no - 1]
        comment_ids = db.get_one_from_collection(
            RECIPIES_COMMENT, '_id', page_id)['comments']
        print(comment_ids)
        comments = []
        for id in comment_ids:
            comment = db.get_one_from_collection(COMMENTS, '_id', id)
            user_id = comment["user_id"]
            # get user avatar and username according to user id
            user = db.get_one_from_collection(USERS, '_id', user_id)
            if "headshot" in user:
                comment["avatar"] = user["headshot"] 
            comment["username"] = user["username"]
            comments.append(comment)
        return {
            'msg': 'success',
            'comments': comments
        }

    @recipe.response(403, 'Invalid Auth Token')
    @recipe.response(200, 'Comment success')
    @recipe.expect(auth_details, comment_details)
    @recipe.param('id', 'ID of recipe being commented')
    @recipe.doc(description='评论为微信朋友圈风格，没有评论内赞。reply_to为回复给谁，和朋友圈那个一样。')
    def post(self):
        uid = authorize(request)
        request_comment = get_request_json()
        rid = get_request_arg('id')
        cid = generate_uuid()
        # add to collection of comment_details
        db.insert_one_to_collection(COMMENTS,
                                    _id=cid,
                                    user_id=uid,
                                    content=request_comment['content'],
                                    reply_to=request_comment['reply_to'],
                                    timestamp=request_comment['timestamp']
                                    )
        # update number of pages under recipes_collection
        # get last page of comment in current recipe
        comment_pages = db.get_one_from_collection(
            RECIPES, '_id', rid)['comments_pages']
        # if the recipe has not been commented, add comment_collection for this recipe
        if (len(comment_pages) == 0):
            page_id = generate_uuid()
            db.insert_one_to_collection(RECIPIES_COMMENT,
                                        _id=page_id,
                                        recipe_id=rid,
                                        page=0,
                                        count=1,
                                        comments=[cid]
                                        )
            # update current recipe and comment_collection
            db.update_one_using_dict(RECIPES, '_id', rid, {
                                     'comments_pages': [page_id]})
        else:
            # get last page of comment
            last_page_id = comment_pages[-1]
            last_page_of_comment = db.get_one_from_collection(
                RECIPIES_COMMENT, '_id', last_page_id)
            # if count is smaller than 1,000, increament number of count and add comment id to the array of comment
            if (last_page_of_comment['count'] < COMMENT_PAGE_CAPACITY):
                # add new comment id
                db.update_fields_values(
                    RECIPIES_COMMENT, '_id', last_page_id, count=+1)
                db.push_many_into_array(
                    RECIPIES_COMMENT, 'comments', '_id', last_page_id, [cid])
                # print('comment added without adding new page')
            # if count is equal to 1,000, save as a new json into comment_collection with one more page
            elif (last_page_of_comment['count'] == COMMENT_PAGE_CAPACITY):
                page_id = generate_uuid()
                page = last_page_of_comment['page']
                db.insert_one_to_collection(RECIPIES_COMMENT,
                                            _id=page_id,
                                            recipe_id=rid,
                                            page=page+1,
                                            count=1,
                                            comments=[cid]
                                            )
                # push page id of added comment page into recipe's comment list
                db.push_many_into_array(
                    RECIPES, 'comments_pages', '_id', rid, [page_id])
                # print('comment added with adding new page')
        return {
            'msg': 'comment success'
        }

    @recipe.response(403, 'Invalid Auth Token')
    @recipe.response(200, 'Comment delete success')
    @recipe.expect(auth_details)
    @recipe.param('id', 'ID of recipe being commented')
    @recipe.doc(description='Delete comment with specific recipe ID')
    def delete(self):
        uid = authorize(request)
        cid = get_request_arg('id')
        # comment will not be deleted, but update content to indicate deletion
        db.update_one_using_dict(COMMENTS, '_id', cid, {
                                 'content': 'Comment Deleted.'})
        return {
            'msg': 'comment deleted'
        }


@recipe.route('/all', strict_slashes=False)
class AllMealTypes(Resource):
    @recipe.response(200, 'Success', recipes_collection)
    @recipe.response(403, 'Invalid Auth Token')
    @recipe.response(400, 'Malformed Request')
    @recipe.response(404, 'User Not Found')
    @cache.memoize(timeout=2*60)
    @recipe.doc(description='''
        return all cuisine types.
    ''')
    def get(self):
        return db.get_one_from_collection(MEAL_TYPES, 'types', 'other')


@recipe.route('/recommend', strict_slashes=False)
class Recommend(Resource):
    @recipe.response(200, 'Success')
    @recipe.response(404, 'Recipe Not Found')
    @recipe.param('id', 'ID of recipe being visited')
    @recipe.param('n', 'number of recommended recipes')
    @recipe.doc(description='Get list of similar recipes based on set of ingredients as recommendations in detail page')
    def get(self):
        rid = get_request_arg('id')
        n = int(get_request_arg('n'))
        # get ingredients of visited recipe
        ingredients = db.get_one_from_collection(
            RECIPES, '_id', rid)['ingredients']
        ingredient_list = []
        for x in ingredients:
            ingredient_list.append(x['ingredient'])
        cursor = db.search_by_ingredients(ingredient_list, n + 1)
        results = [x for x in cursor if x['_id'] != rid]
        if (len(results) > n):
            results = results[:n]
        return {'res': results}
