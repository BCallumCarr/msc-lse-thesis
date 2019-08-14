def trim_betw_dates(dataArray, datasetDict, dates=('2010-09-01', '2011-09-01')):
    '''
    function to trim data to get data between certain dates, format: yyyy-mm-dd
    '''
    ## import pyspark function set
    from pyspark.sql.functions import col, lit

    ## create new dataset dictionary to store results
    newDict = {}

    ## select between dates to trim data
    for i in dataArray:
            # sort and get most recent questions
            #datasets[i] = datasets[i].sort(col('clean_date').desc()).limit(3120)
            # to get all questions past a certain date
            #datasets[i] = datasets[i].filter(datasets[i]['clean_date'] >= lit('2017-06-30'))
            #datasetDict[i] = datasetDict[i].filter("clean_date BETWEEN '2010-04-01' AND '2011-04-01'")
            newDict[i] = datasetDict[i].where(col('clean_date').between(*dates))
    
    return newDict