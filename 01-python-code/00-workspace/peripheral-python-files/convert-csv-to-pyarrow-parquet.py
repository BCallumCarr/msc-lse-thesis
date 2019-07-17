##### load in a csv/json to try and convert to parquet #####
import pandas as pd

csv = pd.read_csv(r"../initial-data/stackoverflow.stackexchange.com/file-000000000000.json")
print(csv.head(5))

## conversion to parquet
csv.to_parquet("../initial-data/stackoverflow.stackexchange.com/file-01.parquet") # uses pyarrow, which fixes a spark java error

## test that data converted successfully
data = pd.read_parquet('../initial-data/stackoverflow.stackexchange.com/file-01.parquet', engine='pyarrow')
print(data.head(5))
