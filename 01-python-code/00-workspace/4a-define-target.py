## create response variable normalised by views
for i in data_array:
    datasets[i] = datasets[i].withColumn('y_ravi', datasets[i]['score']/datasets[i]['viewcount'])
    round_mean = round(datasets[i].select("y_ravi").rdd.flatMap(lambda x: x).mean(),7)
    print(f"The average value of \033[94m{i}\033[0m y_ravi is {round_mean}")

## content of "best" and "worst" questions based on y_ravi
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

## look at certain fora best and worst questions
pd.DataFrame.from_dict(best_worst_qs['fitness'][['title', 'viewcount', 'score', 'clean_body', 'y_ravi']])

## save results to csv
for i in data_array:
    best_worst_qs[i].to_csv(f'best_worst_qs/bwqs{i}.csv')

## pickle best/worst results
import pickle

with open('best_worst_qs/best_worst_qs.pickle', 'wb') as handle:
    pickle.dump(best_worst_qs, handle, protocol=pickle.HIGHEST_PROTOCOL)

## load pickle file to check
best_worst_qs = []
with (open("best_worst_qs/best_worst_qs.pickle", "rb")) as openfile:
    while True:
        try:
            best_worst_qs.append(pickle.load(openfile))
        except EOFError:
            break

## loading from pickle puts it in a list, so put it back in dictionary:
best_worst_qs = best_worst_qs[0]