# need to find spark on local computer
import findspark 
findspark.init()

# import pyspark
import pyspark

# create pyspark session
spark = (
    pyspark.sql.SparkSession
    .builder
    .master("local[4]") # use [X] to limit the number of cores spark uses
    .getOrCreate()
)

# print out relevant info
p = spark.sparkContext.defaultParallelism
v = spark.sparkContext.version
print(f'The Spark UI, version {v}, is available at: http://192.168.0.26:4040/ and the defaultParallelism is {p}')