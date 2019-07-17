import pandas as pd
import xml.etree.ElementTree as ET

root = ET.parse('../initial-data/superuser.stackexchange.com/Posts.xml').getroot() #create an ElementTree object

## function to extract row tag attributes
def iter_rows(_root):
    for i in root.iter('row'):
        df_dict = i.attrib.copy()
        df_dict.update(i.attrib)
        yield (df_dict)

## put everything in a pd.df
df = pd.DataFrame(list(iter_rows(root)))

## convert post_type column to numeric to be able to index
df['PostTypeId']=pd.to_numeric(df['PostTypeId'])

## index post_type==1 to get questions, and choose columns
df = df[df['PostTypeId']==1][['Body', 'Title', 'ViewCount', 'Score', 'CreationDate']]

## write to parquet
df.to_parquet("../initial-data/superuser.stackexchange.com/file-01.parquet") # uses pyarrow, which fixes a spark java error
