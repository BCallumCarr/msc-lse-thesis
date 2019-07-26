# need to find spark on local computer
import findspark 
findspark.init()

import pyspark

spark = (
    pyspark.sql.SparkSession
    .builder
    .master("local[4]") # use [X] to limit the number of cores spark uses
    .getOrCreate()
)

p = spark.sparkContext.defaultParallelism
print(f'The Spark UI is available at: http://192.168.0.26:4040/ and the defaultParallelism is {p}')