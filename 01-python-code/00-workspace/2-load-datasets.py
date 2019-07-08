## array of dataset names to loop through in analysis
data_array = [
    "english",
    "math",
    "rus_stackoverflow",
    "stackoverflow",
    "superuser"
]

datasets = {}    

## read in parquet files which are all named file-01.parquet
for i in data_array:
    datasets[i] = (
        spark
        .read
        .load("initial-data/" + i + ".stackexchange.com/file-01.parquet")
)

for i in data_array:
    print("------------------------")
    print(i)
    print("------------------------")
    datasets[i].printSchema()
    datasets[i].show(3)