#Data Resource:  https://www.kaggle.com/bakostamas/movie-recommendation-algorithm/data?select=ratings.csv

import os
import time
import math
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# utils import
from fuzzywuzzy import fuzz
import seaborn as sns
import matplotlib.pyplot as plt



plt.style.use('ggplot')
rating_data=pd.read_csv(rating_file_path,usecols=['userId','movieId','rating'],\
                        dtype={'movieId':'int64','movieId':'int64','rating':'float64'},encoding = 'utf8')

movie_data=pd.read_csv(movie_file_path,usecols=['movieId','title','genres'],\
                      dtype={'movieId':'int64','title':'str'},encoding = 'utf8')
movie_data = movie_data.rename(columns = {'genres':'features'})
movie_ratingmean = pd.DataFrame(rating_data.groupby('movieId').mean().round(decimals=2))
movie_ratingmean=movie_ratingmean.reset_index()
useryoc = list(zip(movie_ratingmean['movieId'].tolist(),movie_ratingmean['rating'].tolist()))
m_rm = {i:e for i,e in useryoc}
mf = list(zip(movie_data['movieId'].tolist(),movie_data['features'].tolist()))
m_f = {i:e for i,e in mf}
for k,v in m_f.items():
    m_f[k] = v.split('|')

df_movies_cnt = pd.DataFrame(rating_data.groupby('movieId').size(), columns=['count'])

#movie
#print(df_movies_cnt['count'].quantile(np.arange(1, 0.6, -0.05)))
popularity_thres = 20
popular_movies = list(set(df_movies_cnt.query('count >= @popularity_thres').index))
df_ratings_drop_movies = rating_data[rating_data.movieId.isin(popular_movies)]
df_users_cnt = pd.DataFrame(df_ratings_drop_movies.groupby('userId').size(), columns=['count'])

#rating
#print(df_users_cnt['count'].quantile(np.arange(1, 0.5, -0.05)))
ratings_thres = 150

active_users = list(set(df_users_cnt.query('count >= @ratings_thres').index))
df_ratings_drop_users = df_ratings_drop_movies[df_ratings_drop_movies.userId.isin(active_users)]
movie_user_mat = df_ratings_drop_users.pivot(index='movieId', columns='userId', values='rating').fillna(0)

#create mapper from movie title to index
movie_to_idx = {
     movie: i+1 for i, movie in
    enumerate(list(movie_data.set_index('movieId').loc[movie_user_mat.index].title))}   

# # transform matrix to scipy sparse matrix
movie_user_mat_sparse = csr_matrix(movie_user_mat.values)

#Different metric parameters
model = NearestNeighbors(n_neighbors=7,algorithm='brute',metric='cosine', n_jobs=-1)      #72
#model = NearestNeighbors(n_neighbors=7,algorithm='brute',metric='minkowski', n_jobs=-1)  #60
#model = NearestNeighbors(n_neighbors=7,algorithm='brute',metric='manhattan', n_jobs=-1)  #59
#model = NearestNeighbors(n_neighbors=7,algorithm='brute',metric='euclidean', n_jobs=-1)  #60
#model = NearestNeighbors(n_neighbors=7,algorithm='brute',metric='mahalanobis', n_jobs=-1)#60

def find_likely_movie(movie_to_idx,target):
    match = []
    for movie, index in movie_to_idx.items():
        similar = fuzz.ratio(movie.lower(),target.lower())
        if similar >= 60:
            match.append((movie, index, similar))
    # sort
    match = sorted(match, key=lambda x: x[2],reverse=True)
    if not match:
        print('No movie was found similar to target movie')
    else:
        return match[0][1]

def point(former_k):
    k = len(former_k)
    rate_point = 0
    rp = 0
    for i in range(k):
        rate_point += m_rm[former_k[i]] * (k-i-1)/k
    m_feature = {}
    fuck = []
    for idx in former_k:
        rp += m_rm[idx]
        for f in m_f[idx]:
            fuck.append(f)
            if f in m_feature:
                m_feature[f] += 1
            else:
                m_feature[f] = 1
    ff = sorted([v for k, v in m_feature.items()], reverse=True)
    feature_point = 7*ff[0] + 5*ff[1] + 2*ff[2]
    final = round( rate_point + feature_point )
    print('Get point:',final)


def find_recommandation(model,movie_user_matrix,movie_index,target,recommandation_number):
    model.fit(movie_user_matrix)
    #print('user-like-movie: ',target)
    idx = find_likely_movie(movie_index,target)
    #print('Recommandation start:')
    distances,indices = model.kneighbors(movie_user_matrix[idx],n_neighbors=recommandation_number)#+1
    movie_recommands = list(zip(indices.squeeze().tolist(),distances.squeeze().tolist()))
    movie_recommands = sorted(movie_recommands,key=lambda x:x[1])
    index_movie = {v: k for k, v in movie_index.items()}
    print('Recommendations for',target,': ')
    former_k = []
    for i, (idx, dist) in enumerate(movie_recommands):
        former_k.append(idx)
        print(i+1,index_movie[idx])
    point(former_k)



#enter your file path and movie title here
rating_file_path = 'C:/users/z5233940/Desktop/file/ratings.csv'
movie_file_path = 'C:/users/z5233940/Desktop/file/movies.csv'
target_movie = 'Iron man'
find_recommandation(model, movie_user_mat_sparse, movie_to_idx,target_movie, 9)
