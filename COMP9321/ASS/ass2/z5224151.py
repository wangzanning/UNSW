# z5224151  Zanning Wang
# COMP9321  Ass02
# platform: Mac

from flask import Flask
from flask import request
from flask_restx import Resource, Api
from flask_restx import fields
from flask_restx import inputs
from flask_restx import reqparse
import os
import json
import time
import re
import copy
import sqlite3
import urllib.request as req

host_name = "127.0.0.1"
port_number = 8888
app = Flask(__name__)
api = Api(app, default="TV shows", title="COMP9321 Assigment2", description="This is the assignment of COMP9321, you can "
                                                                            "import the tv-show from the website into database"
                                                                            "You can also update, browse ,delete the data "
                                                                            "and so on.")
database_name = "z5224151.db"


# execute the sql command and return the result
def database_exec(command):
    data_connection = sqlite3.connect("z5224151.db")
    current_cursor = data_connection.cursor()
    # check the number of sql command
    if len(re.findall(';', command)) >= 2:
        current_cursor.executescript(command)
    else:
        current_cursor.execute(command)
    data_result = current_cursor.fetchall()
    data_connection.commit()
    data_connection.close()
    return data_result


def create_database(database):
    if os.path.exists(database):
        print("Error, z5224151.db already exists")
        return False
    print("Please wait, Database is creating...")
    database_all = '''
        CREATE TABLE Data_All(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tvmaze_id INTEGER NOT NULL, 
        last_update DATE,
        type VARCHAR(100),
        language VARCHAR(100),
        genres TEXT,
        status VARCHAR(100),
        running_time INTEGER,
        premiered DATE,
        officalSite TEXT,
        schedule JSON,
        rating VARCHAR(100),
        weight VARCHAR(100),
        network JSON,
        summary TEXT
        );
    '''
    database_exec(database_all)
    return True


# send request and load data as json
def load_data(name):
    url = "http://api.tvmaze.com/search/shows?q=" + name
    url_resource = req.Request(url)
    data = req.urlopen(url_resource).read()
    data = json.loads(data)
    return data[0]['show']


# Question1 return JSON
def q1_json(res):
    return {
        "id": res[0],
        "last-update": res[3],
        "tvmaze-id": res[2],
        "_links": {
            "self": {
                "href": "http://" + str(host_name) + ":" + str(port_number) + "/tv-shows/" + str(res[0])
            }
        },
    }


# Question2 return JSON
def q2_json(res):
    return {
        "tvmaze-id": res[2],
        "id": res[0],
        "last-update": res[3],
        "name": res[1],
        "type": res[4],
        "language": res[5],
        "genres": res[6].split("-"),
        "status": res[7],
        "runtime": res[8],
        "premiered": res[9],
        "officialSite": res[10],
        "schedule": json.loads(res[11]),
        "rating": json.loads(res[12]),
        "weight": res[13],
        "network": json.loads(res[14]),
        "summary": res[15],
        "_links": {
            "self": {
                "href": "http://" + str(host_name) + ":" + str(port_number) + "/tv-shows/" + str(res[0])
            },
            "previous": {
                "href": "http://" + str(host_name) + ":" + str(port_number) + "/tv-shows/" + str(res[0]-1)
            },
            "next": {
                "href": "http://" + str(host_name) + ":" + str(port_number) + "/tv-shows/" + str(res[0]+1)
            },
        }
    }


# tackle the argument in the url
parser1 = reqparse.RequestParser()
parser2 = reqparse.RequestParser()
parser3 = reqparse.RequestParser()
parser1.add_argument('name', type=str, location="args")
parser2.add_argument('order_by', type=str, location='args')
parser2.add_argument('page', type=int, location='args')
parser2.add_argument('page_size', type=int, location='args')
parser2.add_argument('filter', type=str, location='args')
parser3.add_argument('format', type=str, location='args')
parser3.add_argument('by', type=str, location='args')

# Answer for Q1
@api.route("/tv-shows/import")
class Q1(Resource):
    # Q1: import a TV Show
    @api.response(200, 'OK')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.response(404, 'Not Found')
    @api.param('name', 'The tv show name (e.g."good-girls")')
    @api.doc(parser=parser1, description="import a TV Show by name")
    def post(self):
        name = parser1.parse_args()['name']
        url_name = copy.deepcopy(name)
        # check the user input a TV name
        if not name:
            return {"message": "please input a name for TV-shows"}, 400
        name = name.upper().replace(' ', '-')
        url_name = url_name.replace(' ',"%20")
        movie_query = database_exec("SELECT * FROM Data_All where name = '" + name + "';")
        # check the query_data exist in database
        if movie_query:
            return q1_json(movie_query[0]), 200
        else:
            movie_show_data = load_data(url_name)
            if not movie_show_data:
                return {"message": name + "has not found on this website"}, 404
            last_update_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
            # insert the query moive into the database
            insert_command = "INSERT INTO Data_All (name, tvmaze_id, last_update, type, language, genres, status, " \
                             "running_time, premiered, officalSite, schedule, rating, weight, network, summary) VALUES" \
                             " ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');" \
                .format(name, movie_show_data['id'], last_update_time, movie_show_data['type'],
                        movie_show_data['language'], '-'.join(movie_show_data['genres']), movie_show_data['status'],
                        movie_show_data['runtime'],
                        movie_show_data['premiered'], movie_show_data['officialSite'], json.dumps(movie_show_data['schedule']),
                        json.dumps(movie_show_data['rating']),
                        movie_show_data['weight'], json.dumps(movie_show_data['network']), movie_show_data['summary'])
            database_exec(insert_command)
            query_result = database_exec("SELECT * FROM Data_All WHERE name = '" + name + "';")

            print(query_result)
            return q1_json(query_result[0]), 201

# Answer for Q2,Q3,Q4
@api.route('/tv-shows/<int:id>')
@api.doc(params={'id':'the movie ID in the database.e.g:1'})
class Q2andQ3andQ4(Resource):
    # Q2: Retrieve a TV Show
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(404, 'Not Found')
    @api.doc(description="Retrieve a TV Show by ID")
    def get(self, id):
        print(id)
        if not id:
            return {"message": "please input the ID before retrieve a TV show"}, 400
        query_result = database_exec("SELECT * FROM Data_All WHERE id = '" + str(id) + "';")
        print(query_result)
        if query_result:
            return q2_json(query_result[0]), 200
        else:
            return {"message": "ID" + str(id) + " not found in database"}, 404

    # Q3: Delete a TV Show
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(404, 'Not Found')
    @api.doc(description="Delete a TV Show by ID")
    def delete(self, id):
        if not id:
            return {"message": "please input the ID before delete a TV show"}, 400
        query_result = database_exec("SELECT * FROM Data_All WHERE id = '" + str(id) + "';")
        if query_result:
            database_exec("DELETE FROM Data_All WHERE id = '" + str(id) + "';")
            return {"message": "The tv show with id '" + str(id) + "' was removed form database!", "id": id}, 200
        else:
            return {"message": "tv-show '" + str(id) + "'was not exists in database"}, 400

    # Q4: Update a TV Show
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(404, 'Not Found')
    @api.param('request','the json used to change the data')
    @api.doc(description="Update a TV Show by ID")
    def patch(self, id):
        # get the payload
        update_data = request.json
        if not id:
            return {"message": "please input the ID before update a TV show"}, 400

        query_result = database_exec("SELECT * FROM Data_All WHERE id = '" + str(id) + "';")
        # check the id should have not be changed
        if update_data['id'] != query_result[0][1]:
            return {"message": "ID must not be changed!"}, 400
        for key in update_data:
            command = "UPDATE Data_All SET {} = \'{}\' WHERE id = {}".format(key, update_data[key], id)
            database_exec(command)
        # update last update time
        last_update_time = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
        update_time_command = "UPDATE Data_All SET last_update = {} WHERE id = {}".format(last_update_time, id)
        database_exec(update_time_command)
        return {
            "id": id,
            "last-update": last_update_time,
            "_links": {
                "self": {
                    "href": "http://" + str(host_name) + ":" + str(port_number) + "/tv-shows/" + str(id)
                },
            }
        }, 200


@api.route("/tv-shows")
class Q5(Resource):
    # Q5: Retrieve a TV Show according different condition
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(404, 'Not Found')
    @api.doc(parser=parser2,description="Retrieve a TV Show according different condition")
    def get(self):
        order_by = parser2.parse_args()['order_by']
        page = parser2.parse_args(['page'])
        page_size = parser2.parse_args()['page_size']
        filter_para = parser2.parse_args()['filter']
        if not order_by or not page or not page_size or not filter_para:
            return {"message": "Miss parameter"}, 400
        permitted_para_list = ["+id", "-id", "+name", "-name", "+runtime", "-runtime",
                               "+premiered", "-premiered", "+rating-average", "-rating-average"]
        # check order_by parameter legal or not
        for i in order_by:
            if i not in permitted_para_list:
                return {"message": "please input legal parameter"}, 400
        # translate +/- into ASC and DESC
        new_order_by = ""
        for para in order_by:
            if para[0] == '+':
                new_order_by += para.split("+")[1] + 'ASC,'
            elif para[0] == '-':
                new_order_by += para.split("-")[1] + 'DESC,'
            else:
                return {"message": "Input Error"}, 400
        new_filter = filter_para.join(",")
        query_command = "SELECT {} FROM Data_All ORDER BY {};".format(new_filter, new_order_by)
        query_result = database_exec(query_command)
        # check current page have content or not
        if int(len(query_result) / page_size) >= page:
            if (len(query_result) > page_size * page):
                page_result = query_result[page_size * (page - 1):page_size * page]
            else:
                page_result = query_result[page_size * (page - 1):len(query_result)]
        else:
            return {
                "page": page,
                "page_size": page_size,
                "tv-shows": [],
                "_links": {},
            }
        tv_show_list = []
        for i in page_result:
            tv_show_list.append(i)
        return {
            "page": page,
            "page_size": page_size,
            "tv-shows": tv_show_list,
            "_links": {
                "self": {
                    "href": "http://" + str(host_name) + ":" + str(port_number) + "/tv-shows/?order_by" + order_by + "&page="
                            + str(page) + "&page_size=" + str(page_size) + "&filter=" + new_filter
                },
            },
        }


@api.route("/tv-shows/statistics")
class Q6(Resource):
    # Q6: get the statistics of the existing TV Show
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    @api.response(404, 'Not Found')
    @api.doc(parser=parser3,description="get the statistics of the existing TV Show")
    def get(self):
        format_para = parser3.parse_args()['format']
        by_para = parser3.parse_args(['by'])
        permitted_by_para = ["language", "genres", "status", "type"]
        query_command = "SELECT {} FROM Data_All;".format(by_para)
        total_number = len(query_command)

        if format_para == "json":
            return {
                "total": temp,
                "total-updated": temp,
                "values": temp,
            }


if __name__ == "__main__":
    create_database(database_name)
    app.run(host=host_name, port=port_number, debug=True)
