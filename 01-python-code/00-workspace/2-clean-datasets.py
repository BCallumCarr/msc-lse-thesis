## import pyspark function set
from pyspark.sql.functions import substring, length, expr, udf, to_timestamp

## dropping index columns
for i in datasets:
    datasets[i] = datasets[i].drop('__index_level_0__')

## sanitising column names
from functools import reduce

for i in data_array:
    oldColumns = datasets[i].schema.names
    newColumns = ["body", "title", "viewcount", "score", "creation_date"]
    datasets[i] = reduce(lambda data, idx: data.
    withColumnRenamed(oldColumns[idx], newColumns[idx]), range(len(oldColumns)), datasets[i])

## changing numeric columns to long type
for i in data_array:
    for j in ['viewcount', 'score']:
        # loop through viewcount and score variables
        datasets[i] = datasets[i].withColumn(j, datasets[i][j].cast("long"))

#########################################################################
### Sorting out date columns for both Stackoverflow and others
#########################################################################

## function to check if numbers in string
def hasNumbers(inputString):
        '''
        function to check if numbers in string
        '''
        return any(char.isdigit() for char in inputString)

## changing date column to timestamp
for i in data_array:
        # weird way to check if dealing with a stackoverflow dataset
        if (hasNumbers(i)):
                # stackoverflow specific date column handling
                # delete last 4 characters of date string
                datasets[i] = datasets[i].\
                withColumn("creation_date", expr("substring(creation_date, 1, length(creation_date)-4)"))
        
        # then ALL fora date column handling
        datasets[i] = datasets[i].\
        withColumn('clean_date', to_timestamp(datasets[i].creation_date).alias('dt'))

#########################################################################

## create regex user-defined function to clean body column
import re
from pyspark.sql.types import *

def clean_body(a):
    '''regex function to clean html tags from body content'''
    x = re.sub("\n|<.*?>", " ", a)
    return x

clean_body_udf =udf(clean_body, StringType())

## create clean_body column for all datasets
for i in data_array:
    datasets[i] = datasets[i].withColumn('clean_body', clean_body_udf('body'))

## drop unneeded columns
for i in data_array:
    datasets[i] = datasets[i].drop('body').drop('creation_date')

## check columns are the right types and names
print('\n\033[1m checking columns are the right types and names \033[0m\n')
for i in data_array:
    print("----- " + i + " -----")
    print(datasets[i].printSchema())


#########################################################################
### Double check that there are no nans
#########################################################################

## import pyspark function set
from pyspark.sql.functions import count, when, isnan

print('\n\033[1m checking that there are no nans \033[0m\n')
for i in data_array:
    print("----- " + i + " -----")
    # must drop date column first, in two different places
    datasets[i].drop('clean_date').select([count(when(isnan(c), c)).\
            alias(c) for c in datasets[i].drop('clean_date').columns]).show()


#########################################################################
### DON'T delete low ViewCount qs
#########################################################################

## import pyspark function set
'''from pyspark.sql.functions import lit

# get rid of viewcounts below a certain threshold
for i in data_array:
        # thresh is first numeric argument, second is accuracy
        thresh = datasets[i].approxQuantile('viewcount', [0.1], 0.0005)[0] 
        datasets[i] = datasets[i].filter(datasets[i]['viewcount'] >= lit(thresh))'''

####################################
###### Define y_ravi response ######
####################################

## create response variable normalised by views
'''for i in data_array:
    datasets[i] = datasets[i].withColumn('y_ravi', datasets[i]['score']/datasets[i]['viewcount'])
    round_mean = round(datasets[i].select("y_ravi").rdd.flatMap(lambda x: x).mean(),7)
    print(f"The average value of \033[94m{i}\033[0m y_ravi is {round_mean}")'''


#########################################################################
### Create shifted score variable
#########################################################################

# import lit function
from pyspark.sql.functions import lit, expr

# find minimum of score for shifting
minp = 1000
for i in data_array:
    if (min(datasets[i].select('score').rdd.flatMap(lambda x: x).collect()) < minp):
        # absolute value because min score is negative
        minp = min( datasets[i].select('score').rdd.flatMap(lambda x: x).collect() )

# adjust minimum to incremented absolute value
minp = abs(minp) + 2

# create new shifted score variable
for i in data_array:
    datasets[i] = datasets[i].withColumn('new_column', lit(minp)).\
    withColumn('score_shift', expr("new_column + score")).drop('new_column')

#########################################################################
### Create logged score and viewcount variables
#########################################################################

# import log function
from pyspark.sql.functions import log

# create new logged score variable
for i in data_array:
    datasets[i] = datasets[i].withColumn('score_shift_log', log('score_shift'))
    
# create new logged viewcount variable
for i in data_array:
    datasets[i] = datasets[i].withColumn('viewcount_log', log('viewcount'))