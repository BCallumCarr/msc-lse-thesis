############################################################
### Temporal split
############################################################

## create train and test dictionaries
train = {}
test = {}

from pyspark.sql.functions import lit

## 80/20 split
if 'economics' in data_array:
    date = '2018-06-15' # date used to split data
    i = 'economics'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')
    

if 'buddhism' in data_array:
    date = '2018-04-01'
    i = 'buddhism'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'fitness' in data_array:
    date = '2017-05-01'
    i = 'fitness'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'health' in data_array:
    date = '2018-04-01'
    i = 'health'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'interpersonal' in data_array:
    date = '2018-09-15'
    i = 'interpersonal'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'math' in data_array:
    date = '2018-02-01'
    i = 'math'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'superuser' in data_array:
    date = '2017-04-01'
    i = 'superuser'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'rus_stackoverflow' in data_array:
    date = '2018-07-01'
    i = 'rus_stackoverflow'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'stackoverflow' in data_array:
    date = '2018-01-01'
    i = 'stackoverflow'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

if 'english' in data_array:
    date = '2018-01-01'
    i = 'english'
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')

del(i)