from flask import Flask
from flask_restx import Api
from util.database import DB
from flask_cors import CORS
from configs import default
from flask_jwt_extended import JWTManager
from flask_caching import Cache # redis
from flask_mail import Mail

# for db
db = DB()


app = Flask(__name__)
app.config.from_object(default)
cache = Cache(app)
CORS(app)
api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)