#################################################
#                Name: Sibo Zhang
#                 zID: z5252570
#################################################

import json
import requests
import pandas as pd 
import sqlite3
from flask import Flask, request 
from flask_restplus import Resource
from flask_restplus import Api
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
from datetime import datetime
from sqlite3 import Error

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('indicator_id', required=True)

parser2 = reqparse.RequestParser()
parser2.add_argument('order_by', action="split")

parser3 = reqparse.RequestParser()
parser3.add_argument('q', type=int)

# indicator_model = api.model('indicator',
#                             {"indicator_id": fields.String})

@api.route("/collections")
class Indicator(Resource):
    @api.response(400, "Validation Error")
    @api.response(404, "Indicator_id not found")
    @api.response(201, "Created")
    @api.expect(parser)
    # @api.expect(indicator_model, validate=True)
    # Question 1
    def post(self):
        # Idea:  request data from worldbank based on indicator_id
        #        load data into 3 seperate dataframes
        #        upload dataframes into 3 sqlite tables
        #        return message 
        # step1: request data from worldbank.orgs

        # indicator = request.json
        args = parser.parse_args()
        indicator_id = args.get('indicator_id')

        # #   check invalid input
        # if 'indicator_id' not in indicator:
        #     return {"message": "Missing indicator_id"}, 400
        # indicator_id = indicator['indicator_id']

        #   Get data from worldbank.org
        url = f"http://api.worldbank.org/v2/countries/all/indicators/{indicator_id}?date=2012:2017&format=json&per_page=1000"
        r = requests.get(url)
        
        #   convert to json
        data = r.json()

        #   check if indicator_id does not exists
        #   invalid value responseexample: 
        #   [{"message": [{"id": "120","key": "Invalid value","value": "The provided parameter value is not valid"}]}]
        if len(data) == 1:
            message = data[0].get('message')
            if message and message[0].get('key') == "Invalid value":
                return {"message": "Indicator_id does not exists"}, 404


        # step2: load data into dataframes

        df_indicator = read_from_sqlite(DATABASE, TABLE1)          
    
        data = data[1]                                             # second element of data

        #  check whether indicator already in database
        if indicator_id in df_indicator['indicator_id'].values:
            return {"message": f"Indicator_id: {indicator_id} already in database."}, 400

        #   create empty dataframes (will insert into sqlite database later)
        #   indicator dataframe
        indicator_cols = ['indicator_id', 'indicator_value', 'creation_time']
        df_indicator = pd.DataFrame(columns=indicator_cols)
        # df_indicator.set_index('indicator_id')
    
        #   country dataframe
        country_cols = ['indicator_id', 'country_id', 'country_value']
        df_country = pd.DataFrame(columns=country_cols)
        # df_country.set_index(['indicator_id', 'country_id'])
    
        #   date and value datafrme
        date_and_value_cols = ['country_id', 'date', 'value']
        df_date_and_value = pd.DataFrame(columns=date_and_value_cols)
        # df_country_data.set_index('country_id')


        #   loop through json data and append records into dataframe
        for i in range(len(data)):
            # handle indicator data
            indicator_id = data[i]['indicator']['id']
            indicator_value = data[i]['indicator']['value']
            create_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")                              # fix time format
            if indicator_id not in df_indicator['indicator_id'].values:
                indicator_data = {'indicator_id': indicator_id,                                         # str
                                  'indicator_value': indicator_value,                                   # str                          # str
                                  'creation_time': create_time}                                         # str
                df_indicator = df_indicator.append(indicator_data, ignore_index=True)
    
            # handle country data
            country_id = data[i]['country']['id']
            country_value = data[i]['country']['value']
            if country_id not in df_country['country_id'].values:
                country_data = {'indicator_id': indicator_id,                   # str
                                'country_id': country_id,                       # str
                                'country_value': country_value}                 # str
                df_country = df_country.append(country_data, ignore_index=True)
    
            # handle date and value data
            date = data[i]['date']
            value = data[i]['value']
            date_and_value_data = {'country_id': country_id,                    # str
                                   'date': int(date),                           # int
                                   'value': value}                              # int
            df_date_and_value = df_date_and_value.append(date_and_value_data, ignore_index=True)
            df_date_and_value.dropna(subset=['value'], inplace=True)            # drop row if 'value' is NONE

        #  insert data into database
        write_in_sqlite(df_indicator, DATABASE, TABLE1)
        write_in_sqlite(df_country, DATABASE, TABLE2)
        write_in_sqlite(df_date_and_value, DATABASE, TABLE3)

        #  retrieve id just created by indicator table
        df_indicator_from_sql = read_from_sqlite(DATABASE, TABLE1)
        table1_id = df_indicator_from_sql[df_indicator_from_sql.indicator_id == indicator_id].id.item()    
        #  explain for above expression:
        #    1) df_indicator_from_sql.[df_indicator_from_sql.indicator_id == indicator_id]
        #       this line returns a dataframe by selecting indicator_id col == current input indicator_id
        #    2) df[...].id.item()
        #       this line return a series which is 'id' col, 
        #       .item() return first item of that series as a scalar

        return {"uri": f"/collections/{table1_id}", 
                "id":  table1_id,  
                "creation_time": create_time,
                "indicator_id" : indicator_id}, 201

    @api.response(200, "Successful")
    @api.response(400, "Bad request")
    @api.expect(parser2)
    # Question3
    def get(self):
        args = parser2.parse_args()
        order_by = args.get('order_by')                 # list of strings i,e, +ID, -creation_time, indicator

        # step1: read data from table1 into dataframe
        df = read_from_sqlite(DATABASE, TABLE1)

        # step2: sort the dataframe based on the order_by request
        ascendings = []
        cols = []
        for order in order_by:
            if order[0] == "-":
                ascendings.append(False)
            elif order[0] == "+":
                ascendings.append(True)
            else:
                return {"message": "Bad request"}, 400

            if order[1:] == 'indicator':
                cols.append('indicator_id')
            else:
                cols.append(order[1:])

        df = df.sort_values(by=cols, ascending=ascendings)
        df.rename(columns={'indicator_id':'indicator'}, inplace=True)
        df.drop(columns='indicator_value', inplace=True)
        df['uri'] = df.apply(lambda row: '/collections/' + str(row.id), axis=1)
        # step3: return data into json format
        res = df.to_dict("records")

        return res, 200

@api.route("/collections/<int:id>")
class individual_indicator(Resource):
    @api.response(404, "Collection id not found")
    @api.response(200, "Successful")
    @api.doc(description="Delete a colletion by its ID")
    # Question 2
    def delete(self, id):
        # step1: check if id in the database table
        df_indicator = read_from_sqlite(DATABASE, TABLE1)
        if id not in df_indicator.id.values:
            api.abort(404, f"collection id: {id} does not exists")

        # step2: find id from each table
        #   do a inner join of the three table to find out all records
        conn = sqlite3.connect(DATABASE)
        sql = f"select \
                    {TABLE1}.id as `t1_id`,\
                    {TABLE2}.id as `t2_id`,\
                    {TABLE3}.id as `t3_id`\
                from {TABLE1} \
                    INNER JOIN {TABLE2} on {TABLE1}.indicator_id = {TABLE2}.indicator_id\
                    INNER JOIN {TABLE3} on {TABLE2}.country_id = {TABLE3}.country_id\
                where {TABLE1}.id = {id}"
        df_delete = pd.read_sql_query(sql, conn)
        #   select all id need to delete
        s1 = df_delete.t1_id.unique() 
        s2 = df_delete.t2_id.unique() 
        s3 = df_delete.t3_id.values 

        # step3: delete row by id from each table
        for row_id in s3:      
            row_id = int(row_id) 
            delete_sqlite_rows_by_id(DATABASE, TABLE3, row_id)
        for row_id in s2:   
            row_id = int(row_id)
            delete_sqlite_rows_by_id(DATABASE, TABLE2, row_id)
        for row_id in s1:
            row_id = int(row_id)
            delete_sqlite_rows_by_id(DATABASE, TABLE1, row_id)

        conn.close()
        return {
                "message" : f"The collection {id} was removed from the database!",
                "id": id
                }, 200

    @api.response(200, "Successful")
    @api.response(404, "Collection ID not found")
    @api.doc(description="Get collections by its ID")
    # Question 4
    def get(self, id):
        # step1: create first part of the json (everything expect "entries")
        df1 = read_from_sqlite(DATABASE, TABLE1)
        if id not in df1.id.values:
            api.abort(404, f"collection id {id} does not exists")
        df1.rename(columns={'indicator_id': 'indicator'}, inplace=True)
        df1 = df1.loc[df1['id'] == id]                                              # filter df base on id
        # step2: create the "entries" part
        #   inner join the all three tables
        conn = sqlite3.connect(DATABASE)
        sql = f"select \
                    {TABLE2}.country_value as `country`,\
                    {TABLE3}.date          as `date`,\
                    {TABLE3}.value         as `value`\
                from {TABLE1} \
                    INNER JOIN {TABLE2} on {TABLE1}.indicator_id = {TABLE2}.indicator_id\
                    INNER JOIN {TABLE3} on {TABLE2}.country_id = {TABLE3}.country_id\
                where {TABLE1}.id = {id}"
        df2 = pd.read_sql_query(sql, conn)
        conn.close()
        # step3: combine above dataframes and return in the right format
        entry1 = df1.to_dict("records")[0]     
        entry2 = df2.to_dict("records")                                            # entries is a list                   
        entry1['entries'] = entry2
        return entry1, 200

@api.route("/collections/<int:id>/<int:year>/<country>")
class collection_id_year_country(Resource):
    @api.response(200, "Successful")
    @api.response(404, "Collection id not found")
    @api.doc(description="Get a collection info by its ID, year, country")
    # Question 5
    def get(self, id, year, country):
        # step1: check if id exists in database
        df_indicator = read_from_sqlite(DATABASE, TABLE1)
        if id not in df_indicator.id.values:
            api.abort(404, f"collection id: {id} does not exists")

        # step2: find value in the database
        #   inner join the all three tables
        conn = sqlite3.connect(DATABASE)
        country = f"'{country}'"
        sql = f"select \
                    {TABLE1}.id            as `id`,\
                    {TABLE1}.indicator_id  as `indicator`,\
                    {TABLE2}.country_value as `country`,\
                    {TABLE3}.date          as `year`,\
                    {TABLE3}.value         as `value`\
                from {TABLE1} \
                    INNER JOIN {TABLE2} on {TABLE1}.indicator_id = {TABLE2}.indicator_id\
                    INNER JOIN {TABLE3} on {TABLE2}.country_id = {TABLE3}.country_id\
                where {TABLE1}.id = {id}\
                  and {TABLE2}.country_value = {country}\
                  and {TABLE3}.date = {year}\
                "
        df = pd.read_sql_query(sql, conn)
        conn.close()
        # step3: convert dataframe into json and return
        return df.to_dict("records")[0], 200

# Question 6
@api.route("/collections/<int:id>/<int:year>")
class collections_id_year(Resource):
    @api.response(404, "Collection id not found")
    @api.response(200, "Successful")
    @api.doc(description="Get collection info by id, year and optional query")
    @api.expect(parser3)
    def get(self, id, year):
        args = parser3.parse_args()
        top = args.get('q', 100)                                        # since optional, set default to 100 if no query passed 
        if not top:                                                     # deal with None input
            top = 100

        # step1: check if id exists in database
        df1 = read_from_sqlite(DATABASE, TABLE1)
        if id not in df1.id.values:
            api.abort(404, f"collection id: {id} does not exists")

        # step2: handle "indicator" and "indicator_value"
        df1.rename(columns={'indicator_id': 'indicator'}, inplace=True)
        df1 = df1.loc[df1['id'] == id]                                  # filter df base on id
        df1.drop(columns=['id', 'creation_time'], inplace=True)
        # step3: handle "entries"
        #   find value in database
        #   inner join the all three tables
        conn = sqlite3.connect(DATABASE)
        sql = f"select \
                    {TABLE2}.country_value as `country`,\
                    {TABLE3}.value         as `value`\
                from {TABLE1} \
                    INNER JOIN {TABLE2} on {TABLE1}.indicator_id = {TABLE2}.indicator_id\
                    INNER JOIN {TABLE3} on {TABLE2}.country_id = {TABLE3}.country_id\
                where {TABLE1}.id = {id}\
                  and {TABLE3}.date = {year}\
                "
        df2 = pd.read_sql_query(sql, conn)
        #   sort df based on value
        df2 = df2.sort_values(by='value', ascending=False)
        conn.close()
        #   slicing data base on user query
        if top >= 0:
            df2 = df2[:top].copy()                     # top num of countries
        else:
            df2 = df2[top:].copy()                     # bottom num of countries

        # step4: combine above df1 and df2 and return in the right format
        entry1 = df1.to_dict("recores")[0]
        entry2 = df2.to_dict("records")
        entry1['entries'] = entry2
        return entry1, 200

#################################################
#                Helper Functions
#################################################
def create_database(database_name):
    """
    create a database by create a connection
    """
    conn = None
    try:
        conn = sqlite3.connect(database_name)
        print(f"Database created: {database_name}")
        print("Database version:",sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table(database_name, create_table_sql):
    """
    create a table from the input sql
    """
    conn = sqlite3.connect(database_name)
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)
    conn.close()

def write_in_sqlite(dataframe, database_file, table_name):
    """
    write dataframe into a sqlite database table. 
    if table already exists, append data, if not create
    new table. function does not return anything
    """
    conn = sqlite3.connect(database_file)
    dataframe.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()


def read_from_sqlite(database_file, table_name):
    """
    read data from a sqlite table. select all 
    data in the table and return as a dataframe
    """
    conn = sqlite3.connect(database_file)
    sql = f'select * from {table_name}'
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def delete_sqlite_rows_by_id(database_file, table_name, id):
    """
    delete records in a sqlite table by id
    """
    conn = sqlite3.connect(database_file)
    sql = f'DELETE FROM {table_name} where id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Global variables
    DATABASE = "z5252570.db"
    TABLE1 = "indicator"
    TABLE2 = "country"
    TABLE3 = "date_and_value"
    # INDICATOR_ID = 1

    # Q1:  Import a collection from the data service
    #   1) create class and POST method
    #   2) create a sqlite database (for storing)
    #   3) GET data from worldbank.org based on user
    #      input "indicator"
    #   4) load the data into dataframe
    #   5) load the dataframe into sqlite database
    #   6) return appropriate message to the user

    #  create SQLite database
    create_database(DATABASE)

    #  create 3 tables
    sql_create_TABLE1 = """
                        CREATE TABLE IF NOT EXISTS indicator(
                            id              integer PRIMARY KEY,
                            indicator_id    text    NOT NULL,
                            indicator_value text,
                            creation_time   text    NOT NULL
                        );
                        """
    sql_create_TABLE2 = """
                        CREATE TABLE IF NOT EXISTS country(
                            id              integer PRIMARY KEY,
                            indicator_id    text    NOT NULL,
                            country_id      text    NOT NULL,
                            country_value   text,
                            FOREIGN KEY (indicator_id) REFERENCES indicator (indicator_id)
                        );
                        """

    sql_create_TABLE3 = """
                        CREATE TABLE IF NOT EXISTS date_and_value(
                            id              integer PRIMARY KEY,
                            country_id      text    NOT NULL,
                            `date`          int,
                            value           numeric,
                            FOREIGN KEY (country_id) REFERENCES country (country_id)
                        );
                        """
    create_table(DATABASE, sql_create_TABLE1)
    create_table(DATABASE, sql_create_TABLE2)
    create_table(DATABASE, sql_create_TABLE3)

    app.run(debug=True)

#################################################
#                    TESTING
#################################################

# if __name__ == '__main__':
#     indicator_id = "NY.GDP.MKTP.CD"
#     url = f"http://api.worldbank.org/v2/countries/all/indicators/{indicator_id}?date=2012:2017&format=json&per_page=1000"
#     # url = "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?date=2000:2001"
#     r = requests.get(url)
#     print("Status Code:" + str(r.status_code) + str(type(r.status_code)))
#     data = r.json()[1]
#     # print(type(data))
#     # print(type(data[1]))


    # # create SQLite database and 3 tables
    # DATABASE = "z5252570.db"
    # TABLE1 = "indicator"
    # TABLE2 = "country"
    # TABLE3 = "date_and_value"

    # create_database(DATABASE)

    # sql_create_TABLE1 = """
    #                     CREATE TABLE IF NOT EXISTS indicator(
    #                         id              integer PRIMARY KEY,
    #                         indicator_id    text    NOT NULL,
    #                         indicator_value text,
    #                         uri             text    NOT NULL,
    #                         creation_time   text    NOT NULL
    #                     );
    #                     """
    # sql_create_TABLE2 = """
    #                     CREATE TABLE IF NOT EXISTS country(
    #                         id              integer PRIMARY KEY,
    #                         indicator_id    text    NOT NULL,
    #                         country_id      text    NOT NULL,
    #                         country_value   text,
    #                         FOREIGN KEY (indicator_id) REFERENCES indicator (id)
    #                     );
    #                     """

    # sql_create_TABLE3 = """
    #                     CREATE TABLE IF NOT EXISTS date_and_value(
    #                         id              integer PRIMARY KEY,
    #                         country_id      text    NOT NULL,
    #                         `date`          int,
    #                         value           numeric,
    #                         FOREIGN KEY (country_id) REFERENCES country (id)
    #                     );
    #                     """

    # create_table(DATABASE, sql_create_TABLE1)
    # create_table(DATABASE, sql_create_TABLE2)
    # create_table(DATABASE, sql_create_TABLE3)


    # read from sqlite table and create 3 dataframes
    
    # df_indicator = read_from_sqlite(DATABASE, TABLE1)          # indicator dataframe
    # df_country = read_from_sqlite(DATABASE, TABLE2)            # country dataframe    
    # df_date_and_value = read_from_sqlite(DATABASE, TABLE3)     # country_data datafrme

    # # initial id for df_indicator
    # id_df_indicator = 1                                             # make this a attribute of the class

    # # loop through json data and append records into dataframe
    # for i in range(len(data)):
    #     # handle indicator data
    #     indicator_id = data[i]['indicator']['id']
    #     indicator_value = data[i]['indicator']['value']
    #     if indicator_id not in df_indicator['indicator_id'].values:
    #         indicator_data = {'id': id_df_indicator,                                                #int
    #                           'indicator_id': indicator_id,                                         #str
    #                           'indicator_value': indicator_value,                                   #str
    #                           'uri': "/collections/"+str(id_df_indicator),                          #str
    #                           'creation_time': datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}    #str
    #         df_indicator = df_indicator.append(indicator_data, ignore_index=True)
    #         id_df_indicator += 1

    #     # handle country data
    #     country_id = data[i]['country']['id']
    #     country_value = data[i]['country']['value']
    #     if country_id not in df_country['country_id'].values:
    #         country_data = {'indicator_id': indicator_id,                   # str
    #                         'country_id': country_id,                       # str
    #                         'country_value': country_value}                 # str
    #         df_country = df_country.append(country_data, ignore_index=True)

    #     # handle date and value data
    #     date = data[i]['date']
    #     value = data[i]['value']
    #     date_and_value_data = {'country_id': country_id,                    # str
    #                            'date': int(date),                           # int
    #                            'value': value}                              # int
    #     df_date_and_value = df_date_and_value.append(date_and_value_data, ignore_index=True)

   
    # # insert data into database
    # write_in_sqlite(df_indicator, DATABASE, TABLE1)
    # write_in_sqlite(df_country, DATABASE, TABLE2)
    # write_in_sqlite(df_date_and_value, DATABASE, TABLE3)

    # # testing the database
    # df_test1 = read_from_sqlite(DATABASE, TABLE1)
    # df_test2 = read_from_sqlite(DATABASE, TABLE2)
    # df_test3 = read_from_sqlite(DATABASE, TABLE3)

    # print("------ TABLE1 ------")
    # print(df_test1)
    # test_id = 'NY.GDP.MKTP.CD'
    # df_test2 = df_test1[df_test1.indicator_id == test_id].id.item()
    # print("-----")
    # print(df_test2, type(df_test2))

    # print("------ TABLE2 ------")
    # print(df_test2)
    # print("------ TABLE3 ------")
    # print(df_test3)


    # print("Indicator dataframe:")
    # print(df_indicator)
    # print("Country dataframe:")
    # print(df_country)
    # print(df_country.columns)
    # print("Date and value dataframe:")
    # print(df_date_and_value)
    # print(df_date_and_value.columns)



