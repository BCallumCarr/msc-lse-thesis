#!/usr/bin/env python
# coding: utf-8

# In[9]:


## testing printing output from console
import subprocess
cmd = [ 'echo', '"Welcome to my PySpark analysis of some StackOverflow Data"' ]
output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
print(output)


# In[10]:


## import standard libraries
import re
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

#%matplotlib inline


# In[11]:


## spark stuff
import findspark # needed on local computer
findspark.init()

import pyspark
#from pyspark.sql import SparkSession

#spark = (
#    SparkSession
#    .builder
#    .master("local")
#    .getOrCreate()
#)

sc = pyspark.SparkContext()

from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)


# In[12]:


sc #spark


# In[13]:


## check default number of partitions
sc.defaultParallelism


# In[14]:


get_ipython().run_cell_magic('time', '', '\n## read in csv file\ndata = (\n    sqlContext\n    .read\n    .load("initial-data/file-01.parquet")\n)')


# In[15]:


data.printSchema()
data.show(10)


# In[16]:


def show(df, n=10):
    '''
    function to show spark df entries nicely
    '''
    display(pd.DataFrame(df.head(n), columns=df.columns))


# In[18]:


show(data)


# In[20]:


## number of rows
data.count()


# In[27]:


get_ipython().run_cell_magic('time', '', '\n## check that there are no nans\n\nfrom pyspark.sql.functions import isnan, when, count, col\n\ndata.select([count(when(isnan(c), c)).alias(c) for c in data.columns]).show()')


# 
# # define response variable

# In[ ]:





# # convert notebook to python file

# In[31]:


get_ipython().system('jupyter nbconvert --to script 1-initial-analysis.ipynb')


# In[ ]:




