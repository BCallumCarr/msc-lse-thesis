%%time

##### load in a csv to spark results in messed up columns #####

data = sqlContext.read.csv("initial-data/file-000000000000.csv/", header=True, inferSchema=True)

## show schema and show top 10 rows with messed up columns
data.printSchema()
data.show(10)
