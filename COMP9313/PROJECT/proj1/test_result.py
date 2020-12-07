from pyspark import SparkContext, SparkConf
from time import time
import pickle
import final
def createSC():
    conf = SparkConf()
    conf.setMaster("local[*]")
    conf.setAppName("C2LSH")
    sc = SparkContext(conf = conf)
    return sc

with open("hashed_data", "rb") as file:
    data = pickle.load(file)

with open("hashed_query", "rb") as file:
    query_hashes = pickle.load(file)

alpha_m = 20
beta_n = 10

length = len(data) - 1
sc = createSC()
data_hashes = sc.parallelize([(length - index, x) for index, x in enumerate(data)])
res = final.c2lsh(data_hashes, query_hashes, alpha_m, beta_n).collect()
sc.stop()

print('Number of candidate: ', len(res))
print('set of candidate: ', set(res))