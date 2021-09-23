# import secrets
import uuid
from flask_restx import abort
from app import db
from PIL import Image
from io import BytesIO
import base64
from math import *
from flask_jwt_extended import create_access_token, decode_token
import numpy as np


def unpack(j, *args, **kargs):
    if kargs.get("required", True):
        not_found = [arg for arg in args if arg not in j]
        if not_found:
            expected = ", ".join(map(str, not_found))
            abort(kargs.get("error", 400),
                  "Expected request object to contain: " + expected)
    return [j.get(arg, None) for arg in args]


def generate_uuid():
    # generate a unique id of 32 digit hex
    # for user id and recipe id
    return uuid.uuid1().hex

def generate_token(user_id):
    # create a token based on user_id
    # can know who that is from decoding the token
    return create_access_token(identity=user_id,  expires_delta=False)


def authorize(request):
    # return : dict
    token = request.headers.get('Token', None)
    if not token:
        abort(403, 'Unsupplied Authorization Token')
    id = decode_token(token)['sub']

    if not id:
        abort(403, 'Invalid Authorization Token')
    return id


def generate_thumbnail(src: str):
    try:
        size = (150, 150)
        im = Image.open(BytesIO(base64.b64decode(src)))
        im.thumbnail(size, Image.ANTIALIAS)
        buffered = BytesIO()
        im.save(buffered, format='PNG')
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except:
        abort(400, 'Image Data Could Not Be Processed')


def calculate_distance(list_A: list, list_B: list):
    # Calculate distance between the score rated to the recipes by two users
    distance = 0
    # get commen rate recipe
    for rate_A in list_A:
        for rate_B in list_B:
            if rate_B['recipe_id'] == rate_A['recipe_id']:
                distance += pow(float(rate_A['rate'])-float(rate_B['rate']), 2)
    return 1/(1+sqrt(distance))


def calculate_similarity(list_A: list, list_B: list):
    common_recipes = []
    score_A = []
    score_B = []
    for rate_A in list_A:
        for rate_B in list_B:
            if (rate_A['recipe_id'] == rate_B['recipe_id']):
                common_recipes.append(rate_A['recipe_id'])
                score_A.append(rate_A['rate'])
                score_B.append(rate_B['rate'])
    
    if len(common_recipes) == 0:
        return 0, 0
    similarity = cosine_similarity(np.array(score_A),np.array(score_B))
    return similarity, len(common_recipes)


def cosine_similarity(x, y):
    num = x.dot(y.T)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    return num / denom
