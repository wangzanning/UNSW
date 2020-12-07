from pyspark import SparkContext, SparkConf
from pyspark.sql.session import SparkSession
import pandas as pd
print("ID:z5224151, Name: ZANNING WANG")

conf = SparkConf().setAppName('Q4_sql')
sc = SparkContext('local', 'test', conf=conf)
spark = SparkSession(sc)

#initial the data
df_score = pd.DataFrame([['1','9313',80],['1','9318',75],['1','6714',70],['2','9021',70],['3','9313' ,90]], columns=['ID','Course','Score'])
df = spark.createDataFrame(df_score)
df.show()

#get the max score of each student and rename column name into max
DF_maximum = df.groupBy('ID').agg({'Score':'max'})
DF_maximum = DF_maximum.withColumnRenamed('max(score)','max')

#get the min score of each student and rename column name into min
DF_minimum = df.groupBy('ID').agg({'Score':'min'})
DF_minimum = DF_minimum.withColumnRenamed('min(score)','min')

#join two dataframe into one
DF_joint = DF_minimum.join(DF_maximum,'ID','inner')

#switch the order of min and max
order = ['ID','max','min']
DF_joint = DF_joint[order]

#print in order of ID
DF_joint.orderBy('ID').show()

