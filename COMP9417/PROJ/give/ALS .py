import os
import time

# spark imports
from pyspark.sql import SparkSession
from pyspark.mllib.recommendation import ALS
import pandas as pd

from pyspark.sql.functions import UserDefinedFunction, explode, desc
from pyspark.sql.types import StringType, ArrayType

# data science imports
import math
import numpy as np

# visualization imports
import seaborn as sns
import matplotlib.pyplot as plt


# spark config
spark = SparkSession \
    .builder \
    .appName("movie recommendation") \
    .config("spark.driver.maxResultSize", "96g") \
    .config("spark.driver.memory", "96g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.master", "local[12]") \
    .getOrCreate()
# get spark context
sc = spark.sparkContext

movies = spark.read.csv('C:/Users/kongg/Desktop/9417/project/litele data/movies.csv',
                        header=True, inferSchema=True)
ratings = spark.read.csv('C:/Users/kongg/Desktop/9417/project/litele data/ratings.csv',
                         header=True, inferSchema=True)
input_data_path = "file:///Users/kongg/Desktop/9417/project/litele data/ratings.csv"
movie_rating = sc.textFile(input_data_path)
header = movie_rating.take(1)[0]
rating_data = movie_rating \
    .filter(lambda line: line!=header) \
    .map(lambda line: line.split(",")) \
    .map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2]))) \
    .cache()

def user_inference(train_data, moviesDF, movies_list):
    # get new user id
    new_user = train_data.map(lambda r: r[0]).max() + 1
    return moviesDF.rdd \
        .map(lambda r: r[0]) \
        .distinct() \
        .filter(lambda x: x not in movies_list) \
        .map(lambda x: (new_user, x))


def make_recommendation(model_pars, ratingsDF, moviesDF,
                        favorite_movies, recommends_num, spark_context):
    # add user likes into ratings dataframe
    movies_list = []
    for movie in favorite_movies:
        movieIds = moviesDF \
            .filter(movies.title.like('%{}%'.format(movie))) \
            .select('movieId') \
            .rdd \
            .map(lambda r: r[0]) \
            .collect()
        movies_list.extend(movieIds)
    # get new user id
    new_user = ratingsDF.map(lambda r: r[0]).max() + 1
    user_rating = ratingsDF.map(lambda r: r[2]).max()
    user_rows = [(new_user, movieId, user_rating) for movieId in movies_list]
    new_user_rdd = spark_context.parallelize(user_rows)
    train_data = ratingsDF.union(new_user_rdd)

    # train ALS
    model = ALS.train(
        ratings=train_data,
        iterations=model_pars.get('iterations', None),
        rank=model_pars.get('rank', None),
        lambda_=model_pars.get('lambda_', None),
        seed=99)

    inference_rdd = user_inference(ratingsDF, moviesDF, movies_list)

    model_predict = model.predictAll(inference_rdd).map(lambda r: (r[1], r[2]))

    recommend_movies = model_predict.sortBy(lambda r: r[1], ascending=False).take(recommends_num)
    recommend_movies_ids = [r[0] for r in recommend_movies]

    return moviesDF.filter(movies.movieId.isin(recommend_movies_ids)) \
        .select('title') \
        .rdd \
        .map(lambda r: r[0]) \
        .collect()

# my favorite movies
my_favorite_movies = ['Iron Man']

# get recommends
recommends = make_recommendation(
    model_pars={'iterations': 10, 'rank': 20, 'lambda_': 0.05},
    ratingsDF = rating_data,
    moviesDF = movies,
    favorite_movies=my_favorite_movies,
    recommends_num=10,
    spark_context=sc)

print('Recommendations for {}:'.format(my_favorite_movies[0]))
result = []
for i, title in enumerate(recommends):
    result.append((title,i))
    print('{0}: {1}'.format(i+1, title))

def point(ratingfile,moviefile,result):
    rating_data=pd.read_csv(ratingfile,usecols=['userId','movieId','rating'],\
                                    dtype={'movieId':'int64','movieId':'int64','rating':'float64'},encoding = 'utf8')
    movie_data=pd.read_csv(moviefile,usecols=['movieId','title','genres'],\
                        dtype={'movieId':'int64','title':'str'},encoding = 'utf8')
    movie_data = movie_data.rename(columns = {'genres':'features'})
    movie_ratingmean = pd.DataFrame(rating_data.groupby('movieId').mean().round(decimals=2))
    movie_ratingmean = movie_ratingmean.reset_index()
    mmean = list(zip(movie_ratingmean['movieId'].tolist(),movie_ratingmean['rating'].tolist()))
    #{movieId:average_rating}
    mean_rating = {i:e for i,e in mmean}
    mf = list(zip(movie_data['movieId'].tolist(),movie_data['features'].tolist()))
    #{movieId:[features]}
    m_f = {i:e.split('|') for i,e in mf}
    mt = list(zip(movie_data['movieId'].tolist(),movie_data['title'].tolist()))
    #{movieId:title}
    idx_movie = {i:e for i,e in mt}
    #{title:movieId}
    movie_idx = {e:i for i,e in mt}
    print('Reading successful!')
    m_feature = {}
    fuck = []
    rate_point = 0
    k = len(result)
    print('k is:',k)
    for i in range(k):
        print(movie_idx[result[i][0]])

        rate_point += mean_rating[movie_idx[result[i][0]]] * (k-i-1)/k
        features = m_f[movie_idx[result[i][0]]]
        for f in features:
            fuck.append(f)
            if f in m_feature:
                m_feature[f]+=1
            else:
                m_feature[f] = 1
    ff = sorted([v for k,v in m_feature.items()],reverse=True)
    feature_point = 7*ff[0] + 5*ff[1] + 2*ff[2]
    final = round( rate_point + feature_point )
    print('Get point: ',final)
    return final

#enter your file path here
rating_file_path = 'C:/users/z5233940/Desktop/file/ratings.csv'
movie_file_path = 'C:/users/z5233940/Desktop/file/movies.csv'

point(rating_file_path,movie_file_path,result)