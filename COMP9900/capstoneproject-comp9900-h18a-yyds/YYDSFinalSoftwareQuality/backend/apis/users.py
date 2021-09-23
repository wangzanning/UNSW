from app import api, db, cache
from util.helpers import *
from util.models import *
from util.request_handling import *
from flask_restx import Resource, abort
from flask import request
from configs.collection_names import *

user = api.namespace(
    'users', description='user service. CRUD of personal info. CRUD of follow/unfollow. CRUD of likes, rating. CRUD of user page.')


@user.route('/', strict_slashes=False)
class User(Resource):
    @user.response(200, 'Success', users_collection)
    @user.response(403, 'Invalid Auth Token')
    @user.response(400, 'Malformed Request')
    @user.response(404, 'User Not Found')
    @user.expect(auth_details)
    @user.param('id', '你要看谁')
    @cache.memoize(timeout=10)
    @user.doc(description='''
        return open information of a certain user. 
        if not id is give, return the one who's playing with the app.
        otherwise provide the info of the user this id belongs to .
    ''')
    def get(self):

        user = authorize(request)
        target = get_request_arg('id') 

        if target:
            info = db.get_one_from_collection(USERS, '_id', target)
            if not user:
                abort(404, "User Not Found")
        else:
            info = db.get_one_from_collection(USERS, '_id', user)

        del info['password']
        return info

    @user.response(403, 'Invalid Authorization Token')
    @user.response(200, 'Success')
    @user.response(400, 'Malformed user object')
    @user.expect(auth_details, user_update_details)
    @user.doc(description='''
        To update info of my own.
        just provide the fields that need to be changed. 
    ''')
    def put(self):

        uid = authorize(request)
        j = get_request_json()
        change_payload = {}

        try:
            new_password = j['newpassword']
            old_password = db.get_one_from_collection(
                USERS, '_id', uid)['password']
            if old_password != j['password']:
                abort(400, 'Password does not match')
            change_payload['password'] = new_password
        except:
            pass

        try:
            change_payload['username'] = j['username']
        except:
            pass

        try:
            newemail = j['email']
            if db.get_one_from_collection(USERS, 'email', newemail):
                abort(403, 'email address already taken')
            change_payload['email'] = j['email']
        except:
            pass
        try:
            # thumb = generate_thumbnail(j['headshot'])
            # change_payload['headshot'] = thumb
            change_payload['headshot'] = j['headshot']
        except:
            pass

        if change_payload == {}:
            abort(406, 'nothing to update')
        db.update_one_using_dict(USERS, '_id', uid, change_payload)
        return {
            "msg": "success"
        }


@user.route('/followings', strict_slashes=False)
class Followings(Resource):
    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success', followings_collection)
    @user.expect(auth_details)
    @user.param('id', 'Id of user to check')
    @cache.memoize(timeout=10)
    @user.doc(description='''
        return a following list. 
        default of my own. otherwise the one with the id. 
    ''')
    def get(self):
        uid = authorize(request)  
        target = get_request_arg('id')  

        if target:
            uid = target
        followings = db.get_one_from_collection(FOLLOWINGS, 'user_id', uid)

        if not followings:
            abort(404, "User Not Found")
        del followings['_id']
        return followings

    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('id', 'Id of user to follow')
    @user.doc(description='''
        To follow someone. must provide the id of the person
    ''')
    def post(self):
        uid_A = authorize(request) 
        uid_B = get_request_arg('id')
        if not uid_B:
            abort(403, 'id of the user to follow not given')

        followings = db.get_one_using_query(
            FOLLOWINGS, {'user_id': uid_A, 'followings': uid_B})
        if followings:
            abort(403, 'already following this')

        # A follow B
        db.push_many_into_array(FOLLOWINGS, 'followings',
                                'user_id', uid_A, [uid_B])
        # A following ++
        db.update_fields_values(USERS, '_id', uid_A, following_num=1)
        # B followrs list update A
        db.push_many_into_array(FOLLOWERS, 'followers',
                                'user_id', uid_B, [uid_A])
        # B fans ++
        db.update_fields_values(USERS, '_id', uid_B, follower_num=1)
        return {
            "msg": "success"
        }

    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('id', 'Id of user to unfollow')
    @user.doc(description='''
        unfollow someone. must provide the id of the person
    ''')
    def delete(self):
        uid_A = authorize(request) 
        uid_B = get_request_arg('id')
        if not uid_B:
            abort(403, 'id of the user to follow not given')

        followings = db.get_one_using_query(
            FOLLOWINGS, {'user_id': uid_A, 'followings': uid_B})
        if not followings:
            abort(403, 'not following this user')
        # A unfollow B,  followings list of A pop out B
        db.pop_many_from_array(FOLLOWINGS, 'followings',
                               'user_id', uid_A, [uid_B])
        # A following num--
        db.update_fields_values(USERS, '_id', uid_A, following_num=-1)
        # B followers list pops A
        db.pop_many_from_array(FOLLOWERS, 'followers',
                               'user_id', uid_B, [uid_A])
        # B fans--
        db.update_fields_values(USERS, '_id', uid_B, follower_num=-1)
        return {
            "msg": "success"
        }


@user.route('/followers', strict_slashes=False)
class Followers(Resource):
    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success', followings_collection)
    @user.expect(auth_details)
    @user.param('id', 'Id of user to check')
    @cache.memoize(timeout=10)
    @user.doc(description='''
        Fetch follower list of somebody specified by user id, 
        return follower list of logged-in user if no id provided.
    ''')
    def get(self):
        uid = authorize(request)
        target = get_request_arg('id')
        if target:
            uid = target
        followers = db.get_one_from_collection(FOLLOWERS, 'user_id', uid)
        # 404
        if not followers:
            abort(404, "User Not Found")
        del followers['_id']
        return followers

@user.route('/likes', strict_slashes=False)
class Likes(Resource):
    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success', likes_collection)
    @user.expect(auth_details)
    @user.param('id', 'Id of the user to check')
    @cache.memoize(timeout=15)
    @user.doc(description='''
        get the like list of someone.
        default of my own. otherwise the one with the id. 
    ''')
    def get(self):
        user = authorize(request) # mine
        target = get_request_arg('id')  # other's

        if target:
            user = target

        likes = db.get_one_from_collection(LIKES, 'user_id', user)
        # likes = db.get_one_and_project(LIKES, {'user_id':user}, {'_id':0, 'author_count':0, 'likes_list':1})
        if not likes:
            abort(404, "User Not Found")
        del likes['_id']
        # try:
        #     del likes['author_count']
        # except:
        #     pass
        return likes

    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('id', 'Id of the post to like')
    @user.doc(description='''
        likes a recipe. need the id of the recipe.
    ''')
    def post(self):
        user = authorize(request)  
        target = get_request_arg('id')  # recipe

        if not target:
            abort(400, "Must provide the id of the recipe to like")

        author_match = db.get_one_using_query(
            USER_RECIPES, {'recipe_list.recipe_id': target})
        author_id = author_match['user_id']
        
        # my like list push back this recipe id and author
        db.push_many_into_array(LIKES, 'likes_list', 'user_id', user, [
                                {'recipe_id': target, 'author_id': author_id}])
        if not db.get_one_using_query(LIKES, {'user_id': user, 'author_count.author_id': author_id}):
            db.push_many_into_array(LIKES, 'author_count', 'user_id', user, [
                                    {'author_id': author_id, 'count': 1}])
        else:
            db.update_nested_fields_values(LIKES, {
                                           'user_id': user, 'author_count.author_id': author_id}, {'author_count.$.count': 1})
        # recipe likes++
        db.update_fields_values(RECIPES, '_id', target, liked_num=1)
        db.update_nested_fields_values(USER_RECIPES, {'recipe_list.recipe_id': target}, {
                                       'recipe_list.$.liked_num': 1})
        #  author likes ++
        db.update_fields_values(USERS, '_id', author_id, liked_num=1)
        return {'msg': 'like success'}

    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('id', 'Id of the post to like')
    @user.doc(description='''
        unlike a recipe. need the id.
    ''')
    def delete(self):

        user = authorize(request)
        target = get_request_arg('id') 

        if not target:
            abort(400, "Must provide the id of the recipe to like")

        liked = db.get_one_in_nested_array(
            LIKES, 'likes_list', recipe_id=target)
        if not liked:
            abort(404, "didn't like it")

        author_match = db.get_one_using_query(
            USER_RECIPES, {'recipe_list.recipe_id': target})
        author_id = author_match['user_id']
        # pop out the recipe and author in my like list
        db.pop_many_from_array(LIKES, 'likes_list', 'user_id', user,  [
                               {'recipe_id': target, 'author_id': author_id}])
        db.update_nested_fields_values(LIKES, {
                                       'user_id': user, 'author_count.author_id': author_id}, {'author_count.$.count': -1})
        # likes of the recipe--
        db.update_fields_values(RECIPES, '_id', target, liked_num=-1)
        db.update_nested_fields_values(USER_RECIPES, {'recipe_list.recipe_id': target}, {
                                       'recipe_list.$.liked_num': -1})
        # likes of the author--
        db.update_fields_values(USERS, '_id', author_id, liked_num=-1)
        return {'msg': 'dislike success'}


@user.route('/rates', strict_slashes=False)
class Rates(Resource):
    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('id', 'Id of the recipe to rate')
    @cache.memoize(timeout=20)
    @user.doc(description='''
        check how much score I give to a recipe. need the id of the recipe.
    ''')
    def get(self):
        uid = authorize(request)
        rid = get_request_arg('id')
        record = db.get_one_projected_using_query(RATES, {'user_id': uid, 'rates_list.recipe_id': rid}, {
                                                  '_id': 0, 'rates_list': {'$elemMatch': {'recipe_id': rid}}})
        print(record)
        if not record:
            return {'rate': None}

        rate = record['rates_list'][0]['rate']
        return {'rate': rate}

    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('rate', 'rate to the recipe')
    @user.param('id', 'Id of the recipe to rate')
    @user.doc(description='''
        rate a recipe. need the rate and the id of the recipe. 
    ''')
    def post(self):
        uid = authorize(request)
        rid = get_request_arg('id')
        
        # if already rated, 403.
        rate = get_request_arg('rate')
        if not rate or not rid:
            abort(403, 'rate/recipe_id required')

        record = db.get_one_projected_using_query(RATES, {'user_id': uid, 'rates_list.recipe_id': rid}, {
                                                  '_id': 0, 'rates_list': {'$elemMatch': {'recipe_id': rid}}})
        if record:
            abort(403, 'already rated')
        # push back to my rating list
        db.push_many_into_array(RATES, 'rates_list', 'user_id', uid, [
                                {'recipe_id': rid, 'rate': int(rate)}])
        # updat the rate of the recipe.
        db.update_fields_values(RECIPES, '_id', rid,
                                rate_sum=int(rate), rate_by=1)
        return {'msg': 'successful'}

    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('id', 'Id of the user to check')
    @user.param('rate', 'rate to the recipe')
    @user.doc(description='''
        change the rate of a recipe I rated. 
    ''')
    def put(self):
        uid = authorize(request)
        rate = int(get_request_arg('rate'))
        rid = get_request_arg('id')

        # if not rated yet, 403
        if not rate or not rid:
            abort(403, 'rate/recipe_id required')

        record = db.get_one_projected_using_query(RATES, {'user_id': uid, 'rates_list.recipe_id': rid}, {
                                                  '_id': 0, 'rates_list': {'$elemMatch': {'recipe_id': rid}}})

        if not record:
            abort(400, 'have not rated yet')
        record = record['rates_list'][0]['rate']
        db.update_fields_in_array(RATES, {'user_id': uid, 'rates_list.recipe_id': rid}, {
                                  'rates_list.$.rate': rate})

        db.update_fields_values(RECIPES, '_id', rid, rate_sum=rate-record)
        return {'msg': 'successful'}

    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('id', 'Id of the user to check')
    @user.doc(description='''
        delete a rate to a recipe. 
    ''')
    def delete(self):
        uid = authorize(request)  
        rid = get_request_arg('id') 

        record = db.get_one_projected_using_query(RATES, {'user_id': uid, 'rates_list.recipe_id': rid}, {
                                                  '_id': 0, 'rates_list': {'$elemMatch': {'recipe_id': rid}}})
        if not record:
            abort(404, 'haven not rated')
        record = record['rates_list'][0]['rate']
        db.pop_many_from_array(RATES, 'rates_list', 'user_id', uid, [
                               {'recipe_id': rid, 'rate': record}])
        db.update_fields_values(RECIPES, '_id', rid,
                                rate_sum=-record, rate_by=-1)
        return {'msg': 'success'}


@user.route('/recipes', strict_slashes=False)
class UsersRecipe(Resource):
    @user.response(403, 'Invalid Auth Token')
    @user.response(200, 'Success')
    @user.expect(auth_details)
    @user.param('id', 'id of the user to check')
    @cache.memoize(timeout=5)
    @user.doc(description='''
        check all recipes someone has posted. 
        default of my own. if given an id, then the one with the id. 
    ''')
    def get(self):
        uid = authorize(request) 
        target = get_request_arg('id') 

        allrecipes = 0

        if target:
            allrecipes = db.get_one_from_collection(
                USER_RECIPES, 'user_id', target)
            if not allrecipes:
                abort(404, "User Not Found")
        else:
            allrecipes = db.get_one_from_collection(
                USER_RECIPES, 'user_id', uid)

        del allrecipes['_id']
        return allrecipes
