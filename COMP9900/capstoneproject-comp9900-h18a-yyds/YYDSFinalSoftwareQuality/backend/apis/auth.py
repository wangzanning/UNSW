from app import db, api, mail
from flask_restx import Resource, abort
from util.models import login_details, signup_details, token_details, email_details
from util.request_handling import *
from util.helpers import *
from configs.collection_names import *
from flask_mail import Message

auth = api.namespace('auth', description='auth serive')

# 注册
@auth.route('/signup', endpoint='auth',strict_slashes=False)
class Signup(Resource):
    @auth.response(200, 'Success',token_details)
    @auth.response(400, 'Missing Username/Password/email')
    @auth.response(409, 'Username Taken')
    @auth.expect(signup_details)
    @auth.doc(description='''
        on signing up, it requires a username, an email address, and the password.
        The email should be unique, otherwise error may occur.
        username can be non-unique.
        If successful, a token will be returned.
    ''')
    def post(self):
        j = get_request_json()
        (uname,mail,pword) = unpack(j,'username','email','password')
        
        if uname=='' or mail=='' or pword=='':
            abort(400, 'Username or email or password cannot be empty')

        if db.get_one_from_collection('users', 'email', mail):
            abort(409, 'email already registered')

        uid = generate_uuid()
        t = generate_token(uid)

        # new user data
        db.insert_one_to_collection(USERS,
            _id=uid,
            username=uname,
            email=mail,
            password=pword,
            recipe_num = 0,
            following_num = 0,
            follower_num = 0,
            liked_num = 0
        )
        
        db.insert_one_to_collection(FOLLOWINGS,
            user_id=uid,
            followings=[]
        )

        db.insert_one_to_collection(FOLLOWERS,
            user_id=uid,
            followers=[]
        )
        
        db.insert_one_to_collection(LIKES,
            user_id=uid,
            likes_list=[],
            author_count=[]
        )
        
        db.insert_one_to_collection(USER_RECIPES,
            user_id=uid,
            recipe_list=[]
        )
        
        db.insert_one_to_collection(RATES, 
            user_id=uid,
            rates_list=[]
        )
        return {
            'token': t
        }


@auth.route('/login', strict_slashes=False)
class Login(Resource):
    @auth.response(200, 'Success',token_details)
    @auth.response(400, 'Missing Username/Password')
    @auth.response(403, 'Invalid Username/Password')
    @auth.expect(login_details)
    @auth.doc(description='''
        email+password is required here to log in.
        if successful, a token will be returned.
    ''')
    def post(self):
        j = get_request_json()
        
        (mail,pword) = unpack(j,'email','password')
        
        if mail == '' or pword == '':
            abort(400, 'Username and password cannot be empty')
        # look up
        res = db.get_one_from_collection(USERS, 'email', mail)
        
        if not res:
            abort(403,'User doesnt exist')
        
        if res['password'] != pword:
            abort(403,'Invalid Password')
        
        t = generate_token(res['_id'])
        return {
            'token': t
        }

@auth.route('/reset', strict_slashes=False)
class Reset(Resource):
    @auth.response(200, 'Success',token_details)
    @auth.response(400, 'Missing email detail')
    @auth.response(403, 'Invalid')
    @auth.response(404, 'no such user')
    @auth.expect(email_details)
    @auth.doc(description='''
        An api to ask for a password resetting link sent to user's email.
        An email with a link to reset the password will be sent to the provided address 
    ''')
    def put(self):
        
        j = get_request_json()
        
        (email) = unpack(j,'email')[0]
        
        if email == '':
            abort(400, 'email cannot be empty')
        
        res = db.get_one_from_collection(USERS, 'email', email)
        
        if not res:
            abort(403,'User doesnt exist')
        
        t = generate_token(res['_id'])
        
        msg = Message("Account Reset", recipients=[email])
        msg.body = "click the link to reset your password:\nhttp://localhost:3000/#/forgetword?token={}".format(t)
        mail.send(msg)
        return {'msg':'successful'}
    
    @auth.response(200, 'Success',token_details)
    @auth.response(400, 'missing password')
    @auth.response(403, 'invalid password')
    @auth.param('token', 'token of this user')
    @auth.expect(login_details)
    @auth.doc(description='''
        An api to update the password of a user based on the token and email address provided.
    ''')
    def post(self):
        t = get_request_arg('token')
        j = get_request_json()
        
        email, password = unpack(j,'email', 'password')
        
        if email == '' or password == '':
            abort(400, 'email or password cannot be empty')
        
        res = db.get_one_from_collection(USERS, 'email', email)
        
        if not res:
            abort(403,'User doesnt exist')
        uid = res['_id']
        if uid != id:
            abort(403,'User token does not match')

        payload = {'password':password}
        
        db.update_one_using_dict(USERS, '_id', uid, payload)
        t = generate_token(res['_id'])
        return {
            'token': t
        }