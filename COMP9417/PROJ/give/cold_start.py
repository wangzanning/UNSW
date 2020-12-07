import pandas as pd
import numpy

#enter your file path and movie title here
rating_file_path = 'C:/users/z5233940/Desktop/file/ratings.csv'
movie_file_path = 'C:/users/z5233940/Desktop/file/movies.csv'
k = 10


#enter your file path and movie title here
rating_file_path = 'C:/users/z5233940/Desktop/file/ratings.csv'
movie_file_path = 'C:/users/z5233940/Desktop/file/movies.csv'

rating_data=pd.read_csv(rating_file_path,usecols=['movieId','rating'],\
                                dtype={'movieId':'int64','rating':'float64'},encoding = 'utf8')

movie_data=pd.read_csv(movie_file_path,usecols=['movieId','title'],\
                            dtype={'movieId':'int64','title':'str'},encoding = 'utf8')

#pd dataframe movie's count
movie_rating_count = pd.DataFrame(rating_data.groupby('movieId').size(),columns=['count'])
movie_rating_count = movie_rating_count.reset_index()
movie_rating_count.head()

L2 = list(zip(movie_rating_count['movieId'].tolist(),movie_rating_count['count'].tolist()))
movie_to_count = {i:e for i,e in L2}
movie_dic =[i for i,e in L2] 

movie_rating_mean = pd.DataFrame(rating_data.groupby('movieId').mean().round(decimals=2))
movie_rating_mean = movie_rating_mean.reset_index()

L = list(zip(movie_rating_mean['movieId'].tolist(),movie_rating_mean['rating'].tolist()))
movie_to_rating = {i:e for i,e in L}

L3 = list(zip(movie_data['movieId'].tolist(),movie_data['title'].tolist()))
movie_to_title = {i:e for i,e in L3}

min_rate_num = movie_rating_count['count'].quantile(0.9)
avg_rate = movie_rating_mean['rating'].mean().round(decimals=2)

def point(idx):
    score = (movie_to_count[idx]*movie_to_rating[idx]+min_rate_num*avg_rate)/(movie_to_count[idx]+min_rate_num)
    return score
result = []
for idx in movie_dic:
    result.append([movie_to_title[idx],idx,round(point(idx),3)])
result =sorted(result,key=lambda x:x[2],reverse=True)

def run(k):
    print('Start recommendation')
    for i in range(k):
        print(i+1,result[i][0])
run(k)
