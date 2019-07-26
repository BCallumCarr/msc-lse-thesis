## create train and test dictionaries
train = {}
test = {}

from pyspark.sql.functions import lit

if 'stackoverflow' not in data_array:
    raise ValueError("It doesn't look like you're dealing with big data")

## first run to assign train and test sets, based on 80/20 split
for i in data_array:
    date = '2018-01-01' # date used to split data
    train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
    test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
    numer = test[i].count()
    denom = train[i].count()
    frac = numer/denom
    print(f'{i}: {frac}, from {numer} and {denom}')
    
date = '2018-02-01'
i = 'math'
train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
numer = test[i].count()
denom = train[i].count()
frac = numer/denom
print(f'{i}: {frac}, from {numer} and {denom}')

date = '2017-04-01'
i = 'superuser'
train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
numer = test[i].count()
denom = train[i].count()
frac = numer/denom
print(f'{i}: {frac}, from {numer} and {denom}')

date = '2018-07-01'
i = 'rus_stackoverflow'
train[i] = datasets[i].filter(datasets[i]['clean_date'] < lit(date))
test[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit(date))
numer = test[i].count()
denom = train[i].count()
frac = numer/denom
print(f'{i}: {frac}, from {numer} and {denom}')

del(i)