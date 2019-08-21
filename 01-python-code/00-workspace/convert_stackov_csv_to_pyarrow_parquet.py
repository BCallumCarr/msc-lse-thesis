def convert_stackov_csv_to_pyarrow_parquet(strDirect='initial-data/stackoverflow.stackexchange.com/'):
        '''
        function to convert stackoverflow .json files into .parquet
        '''
        import os
        import pandas as pd

        ## encode string directory
        directory = os.fsencode(strDirect)

        ## counter
        cntr = 1

        ## loop through all files in directory
        for file in os.listdir(directory):
                filename = os.fsdecode(file)
                print (f'On to file {filename}')
                if filename.endswith('.json'):
                        ## load in csv
                        csv = pd.read_csv(f'{strDirect}{filename}')
                        print(csv.head(5))

                        ## conversion to parquet
                        # uses pyarrow, which fixes a spark java error
                        csv.to_parquet(f'{strDirect}file-0{cntr}.parquet')

                        ## test that data converted successfully
                        data = pd.read_parquet(f'{strDirect}file-0{cntr}.parquet', engine='pyarrow')
                        print(data.head(5))

                        ## increment counter
                        cntr = cntr + 1

