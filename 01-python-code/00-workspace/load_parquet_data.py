def load_parquet_data(dataArray, kind='clean', gcpath='', printSchema=False):
        '''
        function to read in parquet files which are all named file-01.parquet in respective folders
        '''        

        # dictionary to store datasets
        datasets = {}

        # load initial datasets
        if kind=="initial":
                for i in dataArray:
                        datasets[i] = (
                                spark
                                .read
                                # type can either be clean or initial
                                .load(f'{gcpath}{kind}-data/{i.lower()}.stackexchange.com/file-01.parquet')
                        )
        
        # load clean datasets
        else:
                for i in dataArray:
                        datasets[i] = (
                                spark
                                .read
                                .load(f'{gcpath}{kind}-data/{i.lower()}.parquet')
                        )

        # print schema option
        if printSchema:
                for i in dataArray:
                        print("------------------------")
                        print(i)
                        print("------------------------")
                        datasets[i].printSchema()
                        datasets[i].show(3)

        # return dictionary and data array
        return datasets