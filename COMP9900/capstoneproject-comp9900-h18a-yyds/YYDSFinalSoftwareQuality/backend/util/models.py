from app import api
from flask_restx import fields
from configs.default import COMMENT_PAGE_CAPACITY

# what users collection store
users_collection = api.model('users_collection', {
    '_id': fields.String(example='60c0a31f819244b540ad0c8c'),
    'username': fields.String(example='shabi'),
    'email': fields.String(example='shabi@dashabi.com'),
    'password': fields.String(required=True, example='alphanumeric'),
    'recipe_num': fields.Integer(min='0'),
    'following_num': fields.Integer(min='0'),
    'follower_num': fields.Integer(min='0'),
    'liked_num': fields.Integer(min=0),
    'headshot':fields.String
})

signup_details = api.model('signup_details',{
    'username': fields.String(required=True, example='someone'),
    'email': fields.String(required=True,example='someone@gmail.com'),
    'password': fields.String(required=True, example='alphanumeric'),
})
login_details = api.model('login_details',{
    'email': fields.String(required=True,example='someone@gmail.com'),
    'password': fields.String(required=True, example='alphanumeric'),
})
email_details = api.model('email_details',{
    'email': fields.String(required=True,example='someone@gmail.com')
})
user_update_details = api.model('user_update_details',{
    'username': fields.String(example='someone'),
    'email': fields.String(example='someone@gmail.com'),
    'password': fields.String(example='alphanumeric'),
    'newpassword':fields.String(example='alphanumeric'),
    'headshot':fields.String
})
token_details = api.model('token_details',{
    'token': fields.String
})

# token request format
auth_details = api.parser().add_argument('Token', help="just token string",location='headers')

# followings stores who is following who
followings_collection = api.model('followings_collection', {
    'user_id':fields.String(example='c65c1fcfa34da3307d69bf'),
    'followings':fields.List(fields.String)
})

# followers stores who are my fans
followers_collection = api.model('followers_collection', {
    'user_id':fields.String(example='c65c1fcfa34da3307d69bf'),
    'followers':fields.List(fields.String)
})


# likeds stores what I have liked and from which author.
recipe_author_details = api.model('recipe_author_details', {
    'recipe_id':fields.String,
    'author_id':fields.String,
})
author_count_details = api.model('author_count_details', {
    'author_id':fields.String,
    'count':fields.Integer,
})
likes_collection = api.model('likes_collection',{
    'user_id':fields.String(example='c65c1fcfa34da3307d69bf'),
    'likes_list':fields.List(fields.Nested(recipe_author_details)),
    'author_count':fields.List(fields.Nested(author_count_details)),
})

# my ratings to recipes. 
rate_details = api.model('rate_details',{
    'recipe_id':fields.String,
    'rate': fields.Integer,
})
rate_upload_details =  api.model('rate_details',{
    'rate': fields.Integer,
})
rate_collection = api.model('rate_collection', {
    'user_id':fields.String(example='c65c1fcfa34da3307d69bf'),
    'rates_list':fields.List(fields.Nested(rate_details))
})

# myposts stores what I have posted 
recipe_details = api.model('recipe_details',{
    'recipe_id': fields.String(example='c65c1fcfa34da3307d69bf'),
    'liked_num': fields.Integer,
    'last_modified': fields.Float
})
user_recipes_collection = api.model('user_recipes_collection', {
    'user_id': fields.String(example='c65c1fcfa34da3307d69bf'),
    'recipe_list': fields.List(fields.String)
})


method_details = api.model('method_details',{
    'thumbnail':fields.String,
    'method': fields.String
})
ingredient_details = api.model('ingredient_details',{
    'ingredient':fields.String(example='猪大肠'),
    'volume': fields.Integer(min=0),
    'unit': fields.String(example='根')
})
# 'last_modified': fields.Nested(datetime_details),
recipes_collection = api.model('recipes_collection', {
    'author_id':fields.String(example='c65c1fcfa34da3307d69bf'),
    'title':fields.String(example='蜂蜜猪大肠'),
    'last_modified': fields.Float(example=1624247873.6764615),
    'abstract':fields.String(required=False, example='一道老北京传统小吃，蜂蜜猪大肠，非常解腻'),
    'image':fields.String(required=False),
    'liked_num':fields.Integer(min=0),
    'rate_sum':fields.Integer(min=0),
    'rate_by':fields.Integer(min=0),
    'meal_type':fields.List(fields.String(example='北京菜')),
    'methods':fields.List(fields.Nested(method_details)),
    'ingredients': fields.List(fields.Nested(ingredient_details)),
    'comments_pages':fields.List(fields.String(example='评论页的_id'))
})

recipes_uploading_details = api.model('recipes_uploading_details',{
    'title':fields.String(example='蜂蜜猪大肠'),
    'abstract':fields.String(required=False, example='一道老北京传统小吃，蜂蜜猪大肠，非常解腻'),
    'image':fields.String(required=False),
    'meal_type':fields.List(fields.String(example='北京菜')),
    'methods':fields.List(fields.Nested(method_details)),
    'ingredients': fields.List(fields.Nested(ingredient_details)),
})


# comments_collection, each comment page.
comment_details = api.model('comment_details',{
    'user_id':fields.String(example='60c0a31f819244b540ad0c8c'),
    'content':fields.String(example='猪大肠真香阿'),
    'reply_to':fields.String(example='60c0a31f819244b540ad0c8c'),
    'timestamp':fields.Float
})
comments_collection = api.model('comments_collection', {
    'recipe_id': fields.String(example='c65c1fcfa34da3307d69bf'),
    'page': fields.Integer(min=0, max=COMMENT_PAGE_CAPACITY),
    'count':fields.Integer(min=0),
    'comments':fields.List(fields.Nested(comment_details))
})