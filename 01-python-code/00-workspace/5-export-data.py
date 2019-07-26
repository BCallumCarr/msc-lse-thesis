## export clean data with target
for i in data_array:

    datasets[i].write.parquet(f'clean-data/{i}.parquet')