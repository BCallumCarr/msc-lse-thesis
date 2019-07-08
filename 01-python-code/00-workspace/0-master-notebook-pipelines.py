#!/usr/bin/env python
# coding: utf-8

# # GOALS
# 
# * Decide on viewcount threshold to eliminate views
# * Get feature columns working
# * Build an LDA model

# In[1]:


## testing printing output from console
import subprocess
cmd = [ 'echo', '"Welcome to my PySpark analysis of some StackExchange Data"' ]
output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
print(output)


# # Load PySpark

# In[2]:


get_ipython().run_line_magic('run', "-i '1-load-pyspark.py'")


# # Load Data

# In[4]:


get_ipython().run_cell_magic('time', '', "print(datetime.now().time())\n%run -i '2-load-datasets.py'")


# In[5]:


def show_spark_df(df, n=5):
    '''
    function to better print spark df entries
    '''
    display(pd.DataFrame(df.head(n), columns=df.columns))
    
show_spark_df(datasets['english'])


# # Clean Data

# In[6]:


get_ipython().run_cell_magic('time', '', "print(datetime.now().time())\n%run -i '3-clean-datasets.py'")


# # EDA (optional)

# In[9]:


get_ipython().run_cell_magic('time', '', 'print(datetime.now().time())\n%run -i \'4-eda.py\'\n\n#NB TO DO: Find threshold to delete low views to make sure users that can vote have seen the question\n\nvc_thresh_data = {}\n\n## finding means of viewcounts across fora\n\nfor i in data_array:\n    vc_thresh_data[i] = datasets[i].select("viewcount").rdd.flatMap(lambda x: x).mean()\n\nvc_thresh_data')


# # Define Ravi Target Variable

# In[10]:


get_ipython().run_cell_magic('time', '', "print(datetime.now().time())\n%run -i '5-define-target.py'")


# In[18]:


best_worst_qs['superuser']


# # Validation

# In[ ]:


"""%%time

## good/bad threshold validation for CLASSIFICATION task

## choose thresholds
threshes = np.linspace(0.05, 0.95, num=37)

## create empty list for results
result = []

## create user-defined function to add threshold columns
def thresh_cols(a, high_threshold, low_threshold):
    '''function to add threshold columns'''        
    if a > high_threshold:
        return 'good'
    elif a <= low_threshold:
        return 'bad'

thresh_cols_udf = udf(thresh_cols, StringType())
   
for i in range(len(threshes)):
    ## store thresholds, lowest represents % good questions
    lo_thresh = np.quantile(datasets['english'].select('y_ravi').
                            rdd.flatMap(lambda x: x).collect(), threshes[i])
    hi_thresh = np.quantile(datasets['english'].select('y_ravi').
                            rdd.flatMap(lambda x: x).collect(), threshes[len(threshes)-i-1])
    
    # if statement to change over at 50% threshold
    if (i > (len(threshes) - 1) / 2):
        ## label questions according to high and low thresholds AFTER 50% THRESHOLD
        # here we only need one threshold
        datasets['english'] = datasets['english'].withColumn("col." + str(round(threshes[i], 3)),
                                                             thresh_cols_udf('y_ravi', lit(hi_thresh), lit(hi_thresh)))
    else:
        ## label questions according to high and low thresholds BEFORE 50% THRESHOLD
        # here there are two mirrored threshold, where NAs fill the middle
        datasets['english'] = datasets['english'].withColumn("col." + str(round(threshes[i], 3)),
                                                             thresh_cols_udf('y_ravi', lit(hi_thresh), lit(lo_thresh)))

'''
R CODE
## get tokens and remove whitespace that messes up French and Linguistics
    toks_one <- tokens_remove(tokens(paste0(
      sxdf_q[sxdf_q[[as.character(threshes[i])]]=="good",][["Body"[1]]], collapse = " ")), 
                              "\\p{Z}", valuetype = "regex")
    toks_two <- tokens_remove(tokens(paste0(
      sxdf_q[sxdf_q[[as.character(threshes[i])]]=="bad",][["Body"[1]]], collapse = " ")), 
                              "\\p{Z}", valuetype = "regex")
    ## reassign docnames
    docnames(toks_one) <- "good"
    docnames(toks_two) <- "bad"
    
    ## we normalise the dfm by stemming, removing stopwords/punctuation and weighting proportionally
    docfm <- dfm_weight(dfm(c(toks_one, toks_two),
                            stem = TRUE, remove_punct = TRUE, remove = stopwords("english")),
                        "prop")
    
    ## bind results
    result <- rbind(result, c(threshes[i], 
                              textstat_dist(docfm, method="euclidean"), 
                              textstat_simil(docfm, method="cosine"), 
                              textstat_simil(docfm, method="jaccard"), 
                              datasets[k]))
'''
"""


# # Create Pipelines for Modeling

# In[19]:


## garbage collector to speed up computation
import gc
collected = gc.collect()
print("Garbage collector: collected %d objects." % collected)


# In[20]:


from pyspark.ml.pipeline import Pipeline


# In[21]:


target = "y_ravi"
indep_text_variables = ["title", "clean_body"]
#.drop('age').collect()


# In[22]:


## import elements from natural language toolkit
import nltk
#nltk.download('all') # uncomment after first run as admin check
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
stop_words = set(stopwords.words('english'))
table = str.maketrans('', '', string.punctuation)
lmtzr = WordNetLemmatizer()

def get_tokens(line):
    '''
    Function to parse text features
    '''
    tokens = word_tokenize(line)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuations from each word
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stopwords
    words = [w for w in words if not w in stop_words]
    # lemmatizing the words, see https://en.wikipedia.org/wiki/Lemmatisation
    '''lemmatise or stem???'''
    words = [lmtzr.lemmatize(w) for w in words]
    # remove single letters
    words = [word for word in words if not len(word)==1]
    return (words)


# In[23]:


import nltk

from pyspark import keyword_only  ## < 2.0 -> pyspark.ml.util.keyword_only
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType

## custom transformer for nltk tokenisation

class NLTKWordPunctTokenizer(Transformer, HasInputCol, HasOutputCol):

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, stopwords=None):
        super(NLTKWordPunctTokenizer, self).__init__()
        self.stopwords = Param(self, "stopwords", "")
        self._setDefault(stopwords=set())
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(self, inputCol=None, outputCol=None, stopwords=None):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def setStopwords(self, value):
        self._paramMap[self.stopwords] = value
        return self

    def getStopwords(self):
        return self.getOrDefault(self.stopwords)

    def _transform(self, dataset):
        stopwords = self.getStopwords()

        def f(s):
            tokens = nltk.tokenize.wordpunct_tokenize(s)
            return [t for t in tokens if t.lower() not in stopwords]

        t = ArrayType(StringType())
        out_col = self.getOutputCol()
        in_col = dataset[self.getInputCol()]
        return dataset.withColumn(out_col, udf(f, t)(in_col))


# In[24]:


import pyspark.sql.functions as F
from pyspark.ml import Pipeline, Transformer
from pyspark.ml.feature import Bucketizer
from pyspark.sql import DataFrame
from typing import Iterable
import pandas as pd

## custom transformer to spread spares vectors into individual columns
class VectorMLliber(Transformer):
    """
    A custom Transformer which converts a column of pyspark.ml vectors to multiple pyspark.mllib vectors.
    """

    def __init__(self, inputCol=None):
        super(VectorMLliber, self).__init__()

    def _transform(self, df: DataFrame) -> DataFrame:
        
        def f(v):
            return Vectors.sparse(v.size, v.indices, v.values)
        
        df = df.rdd.map(lambda r: as_mllib_vector(r[0]))
        return df


# In[26]:


'''def as_mllib_vector(v):
    return Vectors.sparse(v.size, v.indices, v.values)

features = {}
feature_vec_list = {}
for i in data_array:
    features[i] = word_feat_list[i].select("features")
    feature_vec_list[i] = features[i].rdd.map(lambda r: as_mllib_vector(r[0]))
    feature_vec_list[i].cache()
'''


# In[27]:


nltk_tokenizer_body = NLTKWordPunctTokenizer(
    inputCol="clean_body", outputCol="body_words",  
    stopwords=set(nltk.corpus.stopwords.words('english')))

nltk_tokenizer_title = NLTKWordPunctTokenizer(
    inputCol="title", outputCol="title_words",  
    stopwords=set(nltk.corpus.stopwords.words('english')))

from pyspark.ml.feature import CountVectorizer, VectorAssembler

cnt_vectrizr_body = CountVectorizer(inputCol="body_words", outputCol="body_features", minDF=2)

cnt_vectrizr_title = CountVectorizer(inputCol="title_words", outputCol="title_features", minDF=2)

VectorMLliber_body = VectorMLliber(inputCol="body_features")

VectorMLliber_title = VectorMLliber(inputCol="body_title")



processing_pipeline = Pipeline(stages=[
    nltk_tokenizer_body, 
    nltk_tokenizer_title,
    cnt_vectrizr_body,
    cnt_vectrizr_title
])


# In[28]:


get_ipython().run_cell_magic('time', '', "\n## check that pipeline is working (WHICH IT IS NOT)\n\ndata_processed = processing_pipeline.fit(datasets['english']).transform(datasets['english'])\n\nshow_spark_df(data_processed)\n\n#data_processed.head(2)[0].features.values")


# In[29]:


processing_ensembler = VectorAssembler(inputCols=["body_features", "title_features"], 
                                         outputCol="features")  

processing_pipeline = Pipeline(stages=[processing_pipeline, processing_ensembler])


# # Initial Modeling

# In[30]:


from pyspark.ml.regression import LinearRegression

lr = LinearRegression(maxIter=100,
                      regParam=0.3,
                      elasticNetParam=0.8,
                      featuresCol="features",
                      labelCol="y_ravi",
                      predictionCol="prediction")

# fit linear regression pipeline
pipeline = Pipeline(stages=[processing_pipeline, lr])
trained_pipeline = pipeline.fit(datasets['english'])
trained_pipeline


# In[32]:


show_spark_df(trained_pipeline.transform(datasets['english']))


# In[33]:


(trained_pipeline
 .transform(datasets['english'])
 .select(
    indep_text_variables + ["prediction"]
 )
 .write
 .parquet("linreg_prediction.parquet")
)


# In[34]:


linreg_predictions = spark.read.parquet("linreg_prediction.parquet")


# In[37]:


linreg_predictions.toPandas().head()


# In[35]:


linreg_predictions.select("prediction").describe().toPandas()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ### LDA Model

# In[ ]:


get_ipython().run_cell_magic('time', '', 'print(datetime.now().time())\n\n## fit LDA models with k=10 topics\nfrom pyspark.ml.clustering import LDA\n\nlda = LDA(k=10, maxIter=5)\n\nlda_model_list = {}\nfor i in data_array:\n    lda_model_list[i] = lda.fit(word_feat_list[i])')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'print(datetime.now().time())\n\'\'\'BOTTLENECK TIME - TAKES OVER 45 min JUST FOR ENGLISH\'\'\'\n\n# calculate the perplexity and likelihood for each forum\'s model\n\nloglik_list = {}\nlogper_list = {}\nfor i in data_array:\n    loglik_list[i] = lda_model_list[i].logLikelihood(word_feat_list[i])\n    logper_list[i] = lda_model_list[i].logPerplexity(word_feat_list[i])\n    print("Finished", i, "at", datetime.now().time())\n\n# low perplexity value indicates the model predicts the sample well\n\nfor i in data_array:\n    print("The lower bound on the log likelihood of the " +\'\\033[1m\'+ i +\'\\033[0m\'+ " corpus is: " + str(loglik_list[i]))\n    print("The upper bound on the perplexity of the " +\'\\033[1m\'+ i +\'\\033[0m\'+ " corpus is: " + str(logper_list[i]))\n    print(\'\\n\')')


# In[ ]:


get_ipython().run_cell_magic('time', '', 'print(datetime.now().time())\n\n## first 5 words of the 10 topics from the LDA models per forum\ntopic_list = {}\nfor i in data_array:\n    print("\\n------------------\\n", i, "\\n------------------\\n")\n    topic_list[i] = lda_model_list[i].describeTopics(5)\n    #print("The topics described by their top-weighted terms:\\n")\n    #topic_list[i].show(truncate=False)\n    # show the results\n    topic_j = topic_list[i].select("termIndices").rdd.map(lambda r: r[0]).collect()\n    for j in topic_j:\n        print(np.array(cntvcr_models[i].vocabulary)[j])\n    print(\'\\n\')')


# # Convert notebook to python file

# In[ ]:


get_ipython().system('jupyter nbconvert --to script 0-master-notebook.ipynb')

