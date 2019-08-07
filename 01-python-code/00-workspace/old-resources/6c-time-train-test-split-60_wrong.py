############################################################
### Temporal split
############################################################

## create train and test dictionaries
train = {}
test = {}

from pyspark.sql.functions import lit

## 60/40 split
if 'economics' in data_array:
    date = '2017-12-22' # date used to split data
    i = 'economics'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')
    

if 'buddhism' in data_array:
    date = '2017-09-04'
    i = 'buddhism'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'fitness' in data_array:
    date = '2016-04-08'
    i = 'fitness'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'health' in data_array:
    date = '2017-09-04'
    i = 'health'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'interpersonal' in data_array:
    date = '2018-07-13'
    i = 'interpersonal'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

del(i)