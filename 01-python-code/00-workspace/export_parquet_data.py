## export clean data with target
def export_parquet_data(dataArray, datasetDict, folder='clean-data'):
    for i in dataArray:
        print(f'On to {i}')
        datasetDict[i].write.parquet(f'{folder}/{i.lower()}.parquet')