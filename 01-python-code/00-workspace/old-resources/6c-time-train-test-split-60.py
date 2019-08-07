############################################################
### Temporal split
############################################################

## create train and test dictionaries
train = {}
test = {}

from pyspark.sql.functions import lit

## 60/40 split
if 'economics' in data_array:
    date = '2018-10-22' # date used to split data
    i = 'economics'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = numer + train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} test and {denom} total')
    

if 'buddhism' in data_array:
    date = '2018-03-02 12:15:00.000'
    i = 'buddhism'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = numer + train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} test and {denom} total')

if 'fitness' in data_array:
    date = '2017-08-17'
    i = 'fitness'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = numer + train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} test and {denom} total')

if 'health' in data_array:
    date = '2018-01-20'
    i = 'health'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = numer + train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} test and {denom} total')

if 'interpersonal' in data_array:
    date = '2018-05-21 18:15:00.000'
    i = 'interpersonal'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = numer + train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} test and {denom} total')  

del(i)