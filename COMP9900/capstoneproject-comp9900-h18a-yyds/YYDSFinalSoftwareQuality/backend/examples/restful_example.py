from flask import Flask, request
from flask_restful import Resource, Api
from pymongo import MongoClient
import json
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)

# for db
client = MongoClient("mongodb+srv://admin:zzYYDS9900@kitchen.5hpbe.mongodb.net/test")
db = client.kitchen
todos = db.todos

# for swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "GoToKitch"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


class ToDoSimple(Resource):
    def get(self, todo_id):
        return todos.find_one({"todo_id":todo_id})
    
    def put(self, todo_id):
        content = request.form['data']
        document = {"todo_id":todo_id, "data":content}
        # Serializing json   
        doc_json = json.dumps(document)
        todos.insert_one(document)
        return doc_json,201

api.add_resource(ToDoSimple, '/todo/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)