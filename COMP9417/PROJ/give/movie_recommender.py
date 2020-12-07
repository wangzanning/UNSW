import pandas as pd
from math import pow, sqrt
import csv
import os
path = os.getcwd()

class Recommander():
    def __init__(self,ratingfile,moviefile):
        self.rating_data=pd.read_csv(ratingfile,usecols=['userId','movieId','rating'],\
                                dtype={'movieId':'int64','movieId':'int64','rating':'float64'},encoding = 'utf8')

        self.movie_data=pd.read_csv(moviefile,usecols=['movieId','title','genres'],\
                            dtype={'movieId':'int64','title':'str'},encoding = 'utf8')
        self.movie_data = self.movie_data.rename(columns = {'genres':'features'})
        self.movie_ratingmean = pd.DataFrame(self.rating_data.groupby('movieId').mean().round(decimals=2))
        self.movie_num = self.movie_data.shape[0]
        self.user_num = pd.DataFrame(self.rating_data.groupby('userId')).shape[0]  
        self.movie_ratingmean = self.movie_ratingmean.reset_index()
        self.mmean = list(zip(self.movie_ratingmean['movieId'].tolist(),self.movie_ratingmean['rating'].tolist()))
        #{movieId:average_rating}
        self.mean_rating = {i:e for i,e in self.mmean}
        self.mf = list(zip(self.movie_data['movieId'].tolist(),self.movie_data['features'].tolist()))
        #{movieId:[features]}
        self.m_f = {i:e.split('|') for i,e in self.mf}
        #print(self.m_f)
        self.mt = list(zip(self.movie_data['movieId'].tolist(),self.movie_data['title'].tolist()))
        #{movieId:title}
        self.idx_movie = {i:e for i,e in self.mt}
        #{title:movieId}
        self.movie_idx = {e:i for i,e in self.mt}
        self.new = pd.merge(self.movie_data,self.rating_data,on = 'movieId')
        self.new[['userId','movieId','title','rating','features']].sort_values('userId').to_csv(r'C:/new.csv',index=False)
        self.data = {}
        with open('C:/new.csv','r',encoding='UTF-8') as file:
            miao = csv.reader(file)
            for line in miao:
                if line[0] == 'userId' or line[0] == '':
                    continue
                if not line[0] in self.data.keys():
                    self.data[line[0]] = {line[2]:line[3]}
                else:
                    self.data[line[0]][line[2]] = line[3]
    def distance(self,user1,user2):
        user1_data=self.data[user1]
        user2_data=self.data[user2]
        distance = 0
        for key in user1_data.keys():
            if key in user2_data.keys():
                distance += pow(float(user1_data[key])-float(user2_data[key]),2)     
        return 1/(1+sqrt(distance))      
    def top10_similar(self,userID):
        res = []
        for userid in self.data.keys():
            if not userid == userID:
                sim = self.distance(userID, userid)
                res.append((userid, sim))
        res.sort(key=lambda val:val[1], reverse=True)        
        return res[:10]

    def recommend(self,user,k=10):
        recomm = []
        top = self.top10_similar(user)
        most_sim_user = top[0][0]
        items = self.data[most_sim_user]
        for item in items.keys():
            if item not in self.data[user].keys():
                recomm.append((item, items[item]))
        recomm.sort(key=lambda val:val[1], reverse=True)       
        result = recomm[:k]
        #print(result)
        print('Recommendations:')
        for i in range(k):
            print(i+1,result[i][0])
        return result
    def point(self,user,k=10):
        m_feature = {}
        fuck = []
        result = self.recommend(user,k)
        rate_point = 0
        rp = 0
        for i in range(k):
            rate_point += self.mean_rating[self.movie_idx[result[i][0]]] * (k-i-1)/k
            features = self.m_f[self.movie_idx[result[i][0]]]
            for f in features:
                fuck.append(f)
                if f in m_feature:
                    m_feature[f]+=1
                else:
                    m_feature[f] = 1
        ff = sorted([v for k,v in m_feature.items()],reverse=True)
        feature_point = 7*ff[0] + 5*ff[1] + 2*ff[2]
        final = round( rate_point + feature_point )
        print('Get point:',final)

#enter your file path and userId here
rating_file_path = 'C:/users/z5233940/Desktop/file/ratings.csv'
movie_file_path = 'C:/users/z5233940/Desktop/file/movies.csv'
user_id = '5'


re = Recommander(rating_file_path,movie_file_path)
re.point(user_id)
