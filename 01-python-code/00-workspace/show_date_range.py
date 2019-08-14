def show_date_range(dataArray, datasetDict):
    '''
    function to find range of dates for datasets
    '''
    ## import pyspark function set
    from pyspark.sql.functions import col

    for i in dataArray:
        print(f'{i}:')
        print(datasetDict[i].sort(col('clean_date')).select('clean_date').take(1)[0][0])
        print(f"{datasetDict[i].sort(col('clean_date').desc()).select('clean_date').take(1)[0][0]}\n")