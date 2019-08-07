## export clean data with target
def export_parquet_data(dataArray, datasetDict):
    for i in dataArray:
        print(f'On to {i}')
        datasetDict[i].write.parquet(f'clean-data/{i}.parquet')