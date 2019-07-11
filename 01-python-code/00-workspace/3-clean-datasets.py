## dropping index columns
for i in datasets:
    datasets[i] = datasets[i].drop('__index_level_0__')

from functools import reduce

## sanitising column names

for i in data_array:
    oldColumns = datasets[i].schema.names
    newColumns = ["body", "title", "viewcount", "score"]
    datasets[i] = reduce(lambda data, idx: data.withColumnRenamed(oldColumns[idx], newColumns[idx]), range(len(oldColumns)), datasets[i])

## changing numeric columns to long type

for i in data_array:
    for j in ['viewcount', 'score']:
        datasets[i] = datasets[i].withColumn(j, datasets[i][j].cast("long"))

import re
from pyspark.sql.types import *
from pyspark.sql.functions import udf

## create regex user-defined function to clean body column

def clean_body(a):
    '''regex function to clean html tags from body content'''
    x = re.sub("\n|<.*?>", " ", a)
    return x

clean_body_udf = udf(clean_body, StringType())

## create clean_body column for all datasets

for i in data_array:
    datasets[i] = datasets[i].withColumn("clean_body", clean_body_udf('body'))

## check columns are the right types and names
print('\n\033[1m checking columns are the right types and names \033[0m\n')
for i in data_array:
    print("----- " + i + " -----")
    print(datasets[i].printSchema())

## double check that there are no nans
print('\n\033[1m checking that there are no nans \033[0m\n')
from pyspark.sql.functions import isnan, when, count, col, lit

for i in data_array:
    print("----- " + i + " -----")
    datasets[i].select([count(when(isnan(c), c)).alias(c) for c in datasets[i].columns]).show()