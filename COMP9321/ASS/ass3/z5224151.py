# Zanning Wang
# z5224151
# COMP9321 Ass03

import os
import sys
import ast
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import metrics
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score)

# data
preprocess_col = ['cast', 'crew', 'genres', 'production_countries', 'production_companies', 'spoken_languages']
drop_col = ['revenue', 'movie_id', 'rating', 'original_title', 'original_language', 'overview', 'status',
            'keywords', 'tagline', ]
awesome_production_company = list(['Warner Bros', 'New Line Cinema', 'Sony Pictures', 'Walt Disney', 'Marvel Studios',
                                   'Pixar Animation', 'Twentieth Century Fox Film Corporation', 'Universal Pictures'
                                                                                                'Paramount Pictures',
                                   'Columbia Pictures'])
# From website: https://www.imdb.com/list/ls058011111/
awesome_cast = list(['Robert DeNiro', 'Mark Hamill', 'Harrison Ford', 'Robert Downey Jr', 'Cameron Diaz'
                                                                                          'Scarlett Johansson',
                     'Andy Serkis', 'Anthony Daniels', 'Tom Cruise', 'Eddie Murphy',
                     'Stanley Tucci', 'Idris Elba', 'Johnny Depp', 'Ian McKellan', 'Bradley Cooper', 'Don Cheadle',
                     'Vin Diesel', 'Michael Caine', 'Gary Oldman', 'Dwayne Johnson', 'Zoe Saldana', 'Stellan Skarsgard',
                     'Robin Williams', 'Bruce Willis', 'Mark Wahlberg', 'Owen Wilson', 'Julia Roberts',
                     'Morgan Freeman',
                     'Emma Watson', 'Will Smith', 'Matt Damon', 'Orlando Bloom', 'Steve Carell', 'Simon Pegg',
                     'Cameron Diaz', 'Liam Neeson', 'Mark Ruffalo', 'Carrie Fisher', 'Elizabeth Banks',
                     'Forest Whitaker',
                     'Helena Bonham Carter', 'Ralph Fiennes', 'Chris Pratt', 'Chris Evans', 'Chris Hemsworth',
                     'Ben Stiller', 'Adam Sandler', 'Samuel L. Jackson', 'Woody Harrelson', 'Cate Blanchett',
                     'Tom Hanks', 'Robert De Niro', 'Jack Nicholson', 'Marlon Brando', 'Denzel Washington',
                     'Katharine Hepburn',
                     'Humphrey Bogart', 'Meryl Streep', 'Daniel Day-Lewis', 'Tom Hanks', 'Leonardo DiCaprio',
                     'Cate Blanchett',
                     'Audrey Hepburn', 'Shah Rukh Khan', 'Halle Berry', 'Bruce Lee', 'Jodie Foster', 'Morgan Freeman'])
# From website: https://www.studiobinder.com/blog/best-movie-directors-of-all-time/
awesome_crew = list(
    ['Guillermo del Toro', 'Guillermo del Toro', 'Stanley Kubrick', 'Alfred Hitchcock', 'Akira Kurosawa',
     'Steven Spielberg', 'Martin Scorsese', 'Quentin Tarantino', 'Ingmar Bergman', 'John Ford', 'Sergei Eisenstein',
     'Charlie Chaplin', 'Denis Villeneuve', 'Paul Thomas Anderson', 'Federico Fellini', 'Francis Ford Coppola',
     'Orson Welles', 'Yasujiro Ozu', 'David Lynch', 'Jean-Luc Godard', 'David Fincher', 'F.W. Murnau',
     'Christopher Nolan', 'Billy Wilder', 'Roman Polanski', 'John Cassavetes', 'Alfonso Cuarón', 'David Lean',
     'Andrei Tarkovsky', 'Fritz Lang', 'The Coen Brothers', 'Terrence Malick', 'D.W. Griffith', 'Frank Capra',
     'Elizabeth Banks', 'Ron Howard', 'Steven Spielberg', 'Stephen McFeely', 'Andrew Stanton', 'Lawrence Kasdan',
     'Gore Verbinski', 'Chris Columbus', 'Tim Burton', 'Ron Howard'])


# public function
def nor_col(item):
    if isinstance(item, list):
        res = []
        for i in range(len(item)):
            res.append(item[i]['name'])
        return ','.join(res)


def preprocess_runtime(data):
    if data < 50:
        return 1
    elif 51 <= data < 100:
        return 2
    elif 101 <= data < 200:
        return 3
    else:
        return 4


def preprocess_production_countries(data):
    if "United States of America" in data and data.count(',') == 0:
        return 1
    else:
        return 0


def preprocess_spoken_language(data):
    if "English" in data and data.count(',') == 0:
        return 1
    else:
        return 0


def preprocess_production_companies(data):
    if any(com in data for com in awesome_production_company) and data.count(',') == 0:
        return 2
    elif any(com in data for com in awesome_production_company) and data.count(',') >= 1:
        return 1
    else:
        return 0


def preprocess_cast(data):
    counter = 0
    for item in awesome_cast:
        if item in data:
            counter += 5
    if 0 <= counter < 5:
        return 0
    elif 5 <= counter < 20:
        return 3
    elif 25 <= counter < 50:
        return 4
    else:
        return 8


def preprocess_crew(data):
    counter = 0
    for item in awesome_crew:
        if item in data:
            counter += 1
    if 0 <= counter < 2:
        return 0
    elif 2 <= counter < 5:
        return 1
    elif 5 <= counter < 10:
        return 5
    else:
        return 10


def preprocess_homepage(data):
    if data:
        return 1
    else:
        return 0


def preprocess_release_date(item):
    if item in ['05', '06', '12']:
        return 1
    else:
        return 0


def preprocess_genres(item):
    return len(item.split(','))


# read the train and test data
zid = os.path.basename(sys.argv[0])[0:8]
df_read_train = pd.read_csv(sys.argv[1])
df_read_test = pd.read_csv(sys.argv[2])

df_train_copy = df_read_train.copy()
df_test_copy = df_read_test.copy()

# preprocess the train data and normalize data:
for col in preprocess_col:
    for data in df_read_train[col]:
        data = ast.literal_eval(data)

for col in preprocess_col:
    for data in df_train_copy[col]:
        data = nor_col(data)
# preprocess runtime，production_companies，production_countries，genres, spoken_languages, cast, crew

df_train_copy['runtime'] = df_train_copy['runtime'].apply(preprocess_runtime)
df_train_copy['production_companies'] = df_train_copy['production_companies'].apply(preprocess_production_companies)
df_train_copy['production_countries'] = df_train_copy['production_countries'].apply(preprocess_production_countries)
df_train_copy['spoken_languages'] = df_train_copy['spoken_languages'].apply(preprocess_spoken_language)
df_train_copy['genres'] = df_train_copy['genres'].apply(preprocess_genres)
df_train_copy['cast'] = df_train_copy['cast'].apply(preprocess_cast)
df_train_copy['crew'] = df_train_copy['crew'].apply(preprocess_crew)
df_train_copy['homepage'] = df_train_copy['homepage'].apply(preprocess_homepage)
df_train_copy['release_date'] = df_train_copy['release_date'].apply(preprocess_release_date)

# preprocess the test data
# preprocess the test data and normalize data:
for col in preprocess_col:
    for data in df_read_test[col]:
        data = ast.literal_eval(data)

for col in preprocess_col:
    for data in df_test_copy[col]:
        data = nor_col(data)
# preprocess runtime，production_companies，production_countries，genres, spoken_languages, cast, crew
df_test_copy['runtime'] = df_test_copy['runtime'].apply(preprocess_runtime)
df_test_copy['production_countries'] = df_test_copy['production_countries'].apply(preprocess_production_countries)
df_test_copy['production_companies'] = df_test_copy['production_companies'].apply(preprocess_production_companies)
df_test_copy['spoken_languages'] = df_test_copy['spoken_languages'].apply(preprocess_spoken_language)
df_test_copy['genres'] = df_test_copy['genres'].apply(preprocess_genres)
df_test_copy['cast'] = df_test_copy['cast'].apply(preprocess_cast)
df_test_copy['crew'] = df_test_copy['crew'].apply(preprocess_crew)
df_test_copy['homepage'] = df_test_copy['homepage'].apply(preprocess_homepage)
df_test_copy['release_date'] = df_test_copy['release_date'].apply(preprocess_release_date)
# print(df_train_copy['production_companies'])

# part 1
# predict the "revenue" of movies
data_train_x = df_train_copy.drop(drop_col, axis=1).values
data_train_y_revenue = df_train_copy['revenue'].values
data_test_x = df_test_copy.drop(drop_col, axis=1).values
data_test_y_revenue = df_test_copy['revenue'].values

id = df_test_copy['movie_id'].values

# RandomForestRegressor model
Regression_model = RandomForestRegressor(random_state=0)
Regression_model.fit(data_train_x, data_train_y_revenue)
predicted_revenue = Regression_model.predict(data_test_x)

# # LinearRegression model
# Linear_model = LinearRegression()
# Linear_model.fit(data_train_x, data_train_y_revenue)
# predicted_revenue = Linear_model.predict(data_test_x)

# # LogisticRegression model
# Logistic_model = LogisticRegression()
# Logistic_model.fit(data_train_x, data_train_y_revenue)
# predicted_revenue = Logistic_model.predict(data_test_x)

# calculate the msr, pcc adn print the csv
output_msr = metrics.mean_squared_error(predicted_revenue, data_test_y_revenue)
output_pcc, _ = pearsonr(predicted_revenue, data_test_y_revenue)
print_df = pd.DataFrame({'movie_id': id, 'predicted_revenue': predicted_revenue}, columns=[
    'movie_id', 'predicted_revenue'])
print_df.to_csv(zid + '.PART1.output.csv', index=False)
print_df = pd.DataFrame([[zid, round(output_msr, 2), round(output_pcc, 2)]], columns=['zid', 'MSR', 'correlation'])
print_df.to_csv(zid + '.PART1.summary.csv', index=False)


# part 2
# predict the rating of a movie
# df_train_copy['runtime'] = df_read_train['runtime']
# df_test_copy['runtime'] = df_read_test['runtime']

data_train_x = df_train_copy[['runtime', 'budget', 'cast', 'crew', 'production_companies', 'homepage']].values
data_train_y_rating = df_train_copy['rating'].values
data_test_x = df_test_copy[['runtime', 'budget', 'cast', 'crew', 'production_companies', 'homepage']].values
data_test_y_rating = df_test_copy['rating'].values

# GradientBoostingClassifier()
Classification_model = GradientBoostingClassifier()
Classification_model.fit(data_train_x, data_train_y_rating)
predicted_rating = Classification_model.predict(data_test_x)

# # KNN
# KNN_model = KNeighborsClassifier()
# KNN_model.fit(data_train_x, data_train_y_rating)
# predicted_rating = KNN_model.predict(data_test_x)

# # BaggingClassifier
# Bagging_model = BaggingClassifier()
# Bagging_model.fit(data_train_x, data_train_y_rating)
# predicted_rating = Bagging_model.predict(data_test_x)

# calculate the output_precision, output_recall, output_accuracy and print the csv
output = metrics.classification_report(data_test_y_rating, predicted_rating, output_dict=True)
output_precision = round(output['macro avg']['precision'], 2)
output_recall = round(output['macro avg']['recall'], 2)
output_accuracy = round(output['accuracy'], 2)
print_pd = pd.DataFrame({'movie_id': id, 'predicted_rating': predicted_rating}, columns=[
    'movie_id', 'predicted_rating'])
print_pd.to_csv(zid + '.PART2.output.csv')
print_pd = pd.DataFrame([[zid, output_precision, output_recall, output_accuracy]], columns=[
    'zid', 'average_precision', 'average_recall', 'accuracy'])
print_pd.to_csv(zid + '.PART2.summary.csv')
