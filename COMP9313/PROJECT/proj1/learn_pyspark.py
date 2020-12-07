from pyspark import SparkConf, SparkContext
import pickle
from time import time

def createSC():
    conf = SparkConf()
    conf.setMaster("local[*]")
    conf.setAppName("CSH")
    sc = SparkContext(conf = conf)
    return sc

with open("toy/toy_hashed_data", "rb") as file:
    data = pickle.load(file)

with open("toy/toy_hashed_query", "rb") as file:
    query_hashes = pickle.load(file)

sc = createSC()
data_hashes = sc.parallelize([(index, x) for index, x in enumerate(data)])

print(query_hashes)
data_hashes = data_hashes.keys()
collection_data = data_hashes.take(10)
for line in collection_data:
    print(line)
