
def convert_csv_to_pyarrow_parquet(str_dir='initial-data/stackoverflow.stackexchange.com/'):
        '''
        function to convert stackoverflow .json files into .parquet
        '''
        import os
        import pandas as pd

        ## encode string directory
        directory = os.fsencode(str_dir)

        ## counter
        cntr = 1

        ## loop through all files in directory
        for file in os.listdir(directory):
                filename = os.fsdecode(file)
                print (f'On to file {filename}')
                if filename.endswith('.json'):
                        ## load in csv
                        csv = pd.read_csv(f'initial-data/stackoverflow.stackexchange.com/{filename}')
                        print(csv.head(5))

                        ## conversion to parquet
                        # uses pyarrow, which fixes a spark java error
                        csv.to_parquet(f'initial-data/stackoverflow.stackexchange.com/file-{cntr}.parquet')

                        ## test that data converted successfully
                        data = pd.read_parquet(f'initial-data/stackoverflow.stackexchange.com/file-{cntr}.parquet', engine='pyarrow')
                        print(data.head(5))

                        ## increment counter
                        cntr = cntr + 1

