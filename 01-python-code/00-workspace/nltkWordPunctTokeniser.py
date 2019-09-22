#######################
###### TOKENISER ######
#######################

import nltk
from nltk.stem import PorterStemmer
ps = PorterStemmer()
from pyspark import keyword_only  ## < 2.0 -> pyspark.ml.util.keyword_only
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType

## custom transformer for nltk word tokenisation
class nltkWordPunctTokeniser(Transformer, HasInputCol, HasOutputCol):

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, stopwords=None):
        super(nltkWordPunctTokeniser, self).__init__()
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
            # get tokens with separate punctuation
            tokens = nltk.tokenize.wordpunct_tokenize(s)
            # sort out russian stopwords
            #if ('я' in tokens):
            #    tokens = [t for t in tokens if t not in nltk.corpus.stopwords.words('russian')]
            # remove english stopwords
            tokens = [t for t in tokens if t not in stopwords]
            # remove extra stopwords
            tokens = [t for t in tokens if t not in ['lt', 'ol', 'gt', 'xA', 'lt', 'li', 'td', 'tr']]
            # remove single letters (and single punctuation as well)
            tokens = [t for t in tokens if not len(t)==1]
            # stemming the words
            tokens = [ps.stem(t) for t in tokens]
            # remove punctuation
            tokens = [t.lower() for t in tokens if t.isalpha()] #
            # convert to lower case
            return [t.lower() for t in tokens]
    
        t = ArrayType(StringType())
        out_col = self.getOutputCol()
        in_col = dataset[self.getInputCol()]
        return dataset.withColumn(out_col, udf(f, t)(in_col))