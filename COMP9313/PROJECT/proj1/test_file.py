from pyspark import SparkContext, SparkConf
from time import time
import pickle
import version1
import submission3
import last

def createSC():
    conf = SparkConf()
    conf.setMaster("local[*]")
    conf.setAppName("C2LSH")
    sc = SparkContext(conf = conf)
    return sc

#testCases/testCase1.pkl
#testCases/testQueryHash.pkl
#toy/toy_hashed_data
#toy/toy_hashed_query

with open("hashed_data", "rb") as file:
    data = pickle.load(file)

with open("hashed_query", "rb") as file:
    query_hashes = pickle.load(file)

alpha_m  = 20
beta_n = 10

sc = createSC()
data_hashes = sc.parallelize([(index, x) for index, x in enumerate(data)])
start_time = time()
res = submission3.c2lsh(data_hashes, query_hashes, alpha_m, beta_n).collect()
end_time = time()
sc.stop()

print('running time:', end_time - start_time)
print('Number of candidate: ', len(res))
print('set of candidate: ', set(res))