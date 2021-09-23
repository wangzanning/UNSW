from flask import Flask, request
from flask_restx import Api, Resource, fields, inputs, reqparse
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app, version='1.0', title='Go To Kitchen API', description='zz YYDS')
# app.config['SWAGGER_UI_JSONEDITOR'] = True
user_model = api.model('user',{
    'name':fields.String, 
    'email':fields.String
})

# for db
client = MongoClient("mongodb+srv://admin:zzYYDS9900@kitchen.5hpbe.mongodb.net/test")
db = client.kitchen
user = db.user

parser = reqparse.RequestParser()
parser.add_argument('order', choices=list(column for column in user_model.keys()))
parser.add_argument('ascending', type=inputs.boolean)

# api
@api.route('/users')
class UserList(Resource):
    @api.response(201, ' user added ')
    @api.doc(description='add a new new')
    @api.response(400, 'Validation Error')
    @api.expect(user_model, validate=True)
    def post(self):
        payload = request.json
        print(payload)
        # doc_json = json.dumps(document)
        user.insert_one(payload)
        return {"message": "user {} is created, email {}".format(payload['name'],payload['email'])}, 201


@api.route('/users/<string:name>')
#@api.route('/user/<name>')
class User(Resource):
    @api.doc(description='get the user')
    @api.response(404, 'User was not found')
    @api.response(200, 'Successful')
    def get(self, name):
        res = user.find_one({"name":name})
        if not res:
            api.abort(404, 'user doest not exist')
        del res['_id']
        return res, 200
    
    @api.response(200, 'Successful')
    @api.doc(description='delete a user by the name')
    def delete(self, name):
        if not user.find_one({"name":name}):
            api.abort(404, 'user doest not exist')
        user.delete_one({"name":name})
        return {"message": "user {} is deleted".format(name)}, 201

    @api.response(200, 'Successful')
    @api.expect(user_model, validate=False)
    #@api.marshal_with(user_model)
    def put(self, name):
        payload = request.json
        # print(payload)
        user.find_and_modify({"name":payload['name']}, payload)
        return {"message": "user {} is updated, email {}".format(payload['name'],payload['email'])}, 201

if __name__ == '__main__':
    app.run(debug=True)