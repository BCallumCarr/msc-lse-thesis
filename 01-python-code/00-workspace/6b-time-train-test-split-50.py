############################################################
### Temporal split
############################################################

## create train and test dictionaries
train = {}
test = {}

# import pyspark.sql functions
from pyspark.sql.functions import lit, col, row_number
from pyspark.sql.window import Window  

# select date column to sort
w = Window.orderBy('clean_date') 

## 50/50 split
for i in data_array:
    
    # store middle question count
    hlfwy_mrk = datasets[i].count()/2

    # add index column with sorted data
    datasets[i] = datasets[i].withColumn('index', row_number().over(w))
    train[i] = datasets[i].filter(datasets[i]['index'] <= lit(hlfwy_mrk))
    test[i] = datasets[i].filter(datasets[i]['index'] > lit(hlfwy_mrk))
    numer = test[i].count()
    denom = numer + train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} test and {denom} total')