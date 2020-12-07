from pyspark.python.pyspark.shell import *

data = [(1,9319,80),(1,9318,75),(1,6714,70),(2,9021,70), (3,9313,90)]

column_name = ['id', 'course', 'score']
record_DF = spark.createDataFrame(data = data, schema=column_name)
record_DF.show(6)

record_DF_max = record_DF.groupBy('id').agg({'score':'max'}).withColumnRenamed('max(score)','max')
record_DF_min = record_DF.groupBy('id').agg({'score':'min'}).withColumnRenamed('min(score)','min')
maxmin = record_DF_max.join(record_DF_min, 'id', 'inner').orderBy('id', ascending = True)

maxmin.show()




