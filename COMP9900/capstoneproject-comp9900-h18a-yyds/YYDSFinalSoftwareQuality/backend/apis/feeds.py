from app import db, api, cache
from flask_restx import Resource, abort
from util.models import auth_details
from util.request_handling import *
from util.helpers import *
from configs.collection_names import *
from random import randint

feed = api.namespace('feeds', description='Feeds service')


@feed.route('/', endpoint='feeds', strict_slashes=False)
class Feeds(Resource):
    @feed.response(200, 'Success')
    @feed.response(400, 'invalid token')
    @feed.expect(auth_details)
    # @feed.param('n','Number of posts to fetch, 10 by default')
    # @feed.param('p','What post to start at, 0 by default')
    @cache.memoize(timeout=15)
    @feed.doc(description='''
        To get the feed of all recipes of all authors a user is following. 
    ''')
    def get(self):
        user = authorize(request)
        # n = get_request_arg('n', int, default=10)
        # p = get_request_arg('p', int, default=0)
        followings = db.get_one_from_collection(
            FOLLOWINGS, 'user_id', user)['followings']
        res = []
        for f in followings:
            res.extend(db.get_one_from_collection(
                USER_RECIPES, 'user_id', f)['recipe_list'])
        
        return {'msg': res}


@feed.route('/hot', strict_slashes=False)
class FeedHot(Resource):
    @feed.response(200, 'Success')
    @feed.response(400, 'invalid token')
    @feed.doc(description='''
        To return some hot recipes. 
    ''')
    def get(self):
        cursor = db.search_by_range(RECIPES, 1, None, 100, {'_id': 1, 'liked_num': 1})
        pool = []
        pool.extend(cursor)
        n = len(pool)
        res = {'res': []}
        if n < 10:
            res['res'].extend(pool)
            return res

        picks = []
        for _ in range(10):
            i = randint(0, n-1)
            while i in picks:
                i = randint(0, n-1)
            picks.append(i)

        for i in picks:
            res['res'].append(pool[i])
        return res


@feed.route('/users', strict_slashes=False)
class FeedUsers(Resource):
    @feed.response(200, 'Success')
    @feed.response(400, 'invalid token')
    @feed.param('n', 'Number of users that expect to be recommended in feed page')
    @feed.expect(auth_details)
    @feed.doc(description='''
        Return users who have similar rating with me. Will not serach on all users, but find out neighbours first.
        Neighbours are the user who is following one of the same contributors as me. 
        If number of neighbours is less than the expected number, will search from logged-in user's followers, 
        then from popular users who have the most number of likes.
    ''')
    def get(self):
        user_id = authorize(request)
        n = int(get_request_arg('n'))
        rate_list = db.get_one_from_collection(
            RATES, 'user_id', user_id)["rates_list"]
        following_list = db.get_one_from_collection(
            FOLLOWINGS, 'user_id', user_id)['followings']
        
        # if the user has not rate any reicpes or follow any contributors, give top n users who have most likes
        if (len(rate_list) == 0 or len(following_list) == 0):
            top_users = db.search_by_range(USERS, 1, None, n, {
                '_id': 1, 'username': 1, 'headshot': 1, 'liked_num': 1})
            res = {
                'msg': 'Have not rate any recipes or have not followed anyone', 
                'res': []
            }
            res['res'].extend(top_users)
            return res
        
        # find my neighbours
        neighbours = set()  # avoid duplicate users
        neighbours_similarity = []
        for following_id in following_list:
            cur_follower_list = db.get_one_from_collection(
                FOLLOWERS, 'user_id', following_id)['followers']
            if (cur_follower_list == None):
                continue
            for follower_id in cur_follower_list:
                if (follower_id != user_id):
                    neighbours.add(follower_id)

        if (len(neighbours) < n):
            # find from my followers
            follower_list = db.get_one_from_collection(
                FOLLOWERS, 'user_id', user_id)['followers']
            neighbours.union(set(follower_list))

        if (len(neighbours) < n):
            # find out from popular users
            popular_users = db.search_by_range(USERS, 1, None, 2 * n, {'_id': 1})
            for user in popular_users:
                if (user['_id'] != user_id):
                    neighbours.add(user['_id'])

        # return list(neighbours)
        # calculate similarity between neighbours
        for neighbour in neighbours:
            # calculate similarity
            rate_list_ngb = db.get_one_from_collection(
                RATES, 'user_id', neighbour)['rates_list']
            user = db.get_one_from_collection(
                USERS, '_id', neighbour)
            similarity, common = calculate_similarity(
                rate_list, rate_list_ngb)
            user_res = {
                '_id': user['_id'],
                'username': user['username'],
                'similarity': similarity,
                'no_common': common,
            }
            if ('headshot' in user.keys()): user_res['headshot'] = user['headshot']
            neighbours_similarity.append(user_res)

        neighbours_similarity.sort(key=lambda val: (val['similarity'], val['no_common']), reverse=True)
        neighbours_similarity = neighbours_similarity[:n]
        return {
            'res': neighbours_similarity
        }
