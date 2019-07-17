## create response variable normalised by views

for i in data_array:
    datasets[i] = datasets[i].withColumn('y_ravi', datasets[i]['score']/datasets[i]['viewcount'])
    round_mean = round(datasets[i].select("y_ravi").rdd.flatMap(lambda x: x).mean(),7)
    print(f"The average value of \033[94m{i}\033[0m y_ravi is {round_mean}")

## content of "best" and "worst" questions based on Score/ViewCount

best_worst_qs = {}

for i in data_array:
    best_worst_qs[i] = pd.concat(
        [
            datasets[i].where(datasets[i].y_ravi == datasets[i].select('y_ravi').
                           rdd.flatMap(lambda x: x).max()).toPandas(),
            datasets[i].where(datasets[i].y_ravi == datasets[i].select('y_ravi').
                           rdd.flatMap(lambda x: x).min()).toPandas()
        ]
        , axis=0)

import pickle

## pickle best/worst results

with open('best_worst_qs.pickle', 'wb') as handle:
    pickle.dump(best_worst_qs, handle, protocol=pickle.HIGHEST_PROTOCOL)

## export clean data with target
for i in data_array:

    datasets[i].write.parquet(f'clean-data/{i}.parquet')