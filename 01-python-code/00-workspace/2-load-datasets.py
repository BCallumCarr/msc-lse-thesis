## read in parquet files which are all named file-01.parquet
for i in data_array:
    datasets[i] = (
        spark
        .read
        .load(f'initial-data/{i}.stackexchange.com/file-01.parquet')
)

for i in data_array:
    print("------------------------")
    print(i)
    print("------------------------")
    datasets[i].printSchema()
    datasets[i].show(3)