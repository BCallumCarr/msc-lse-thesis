#####################################
###### LDA feature engineering ######
#####################################

## import ml libraries and define transformers
from pyspark.ml.feature import CountVectorizer, IDF

# tokenisers
nltk_tokeniser_body = nltkWordPunctTokeniser(
    inputCol='clean_body', outputCol='body_words',  
    stopwords=set(nltk.corpus.stopwords.words('english')))
nltk_tokeniser_title = nltkWordPunctTokeniser(
    inputCol='title', outputCol='titl_words',  
    stopwords=set(nltk.corpus.stopwords.words('english')))

# counters
cnt_vectrizr_body = CountVectorizer(inputCol='body_words', outputCol='body_feats') #!!! minDF???
cnt_vectrizr_title = CountVectorizer(inputCol='titl_words', outputCol='titl_feats')

# to IDF matrix
to_idf_body = IDF(inputCol='body_feats', outputCol='features')
to_idf_title = IDF(inputCol='titl_feats', outputCol='features')

## function to spread topicDist column later
from pyspark.sql.functions import udf, col
from pyspark.sql.types import ArrayType, DoubleType

def to_array(col):
    def to_array_(v):
        return v.toArray().tolist()
    return udf(to_array_, ArrayType(DoubleType()))(col)

## choose LDA model !!!!!! NB STEP
from pyspark.ml.clustering import LDA
# docCon is alpha, or parameter of Dirichlet prior on distribution of topics over docs
# topicCon is rho/delta, or parameter of Dirichlet prior on distribution of words over topics
lda = LDA(k=10)#, maxIter=100)#, topicConcentration=0.01) #, docConcentration=0.01)


## loop through datasets for LDA modelling
for i in data_array:
    print(f'On to {i}')
    # body transformers
    tokens_body = nltk_tokeniser_body.transform(datasets[i])
    counts_body = cnt_vectrizr_body.fit(tokens_body).transform(tokens_body)
    idf_body = to_idf_body.fit(counts_body).transform(counts_body)
    
    # fit LDA model on body
    datasets[i] = lda.fit(idf_body).transform(idf_body)
    
    # get topicDist on body
    datasets[i] = datasets[i].withColumn("btd", to_array(col("topicDistribution"))).\
        select(["*"] + [col("btd")[i] for i in range(10)])
    
    # drop unnecessary columns
    datasets[i] = datasets[i].drop('features').drop('topicDistribution')
    
    # title transformers
    tokens_title = nltk_tokeniser_title.transform(datasets[i])
    counts_title = cnt_vectrizr_title.fit(tokens_title).transform(tokens_title)
    idf_title = to_idf_title.fit(counts_title).transform(counts_title)

    # fit LDA model on title
    datasets[i] = lda.fit(idf_title).transform(idf_title)
    
    # get topicDist on title
    datasets[i] = datasets[i].withColumn("ttd", to_array(col("topicDistribution"))).\
        select(["*"] + [col("ttd")[i] for i in range(10)])

    # drop unnecessary columns
    datasets[i] = datasets[i].drop('btd').drop('ttd').drop('titl_feats').drop('body_feats').\
        drop('features').drop('topicDistribution')
    

#################################################
###### Character, word and sentence counts ######
#################################################

## import pyspark functions and define transformers
import pyspark.sql.functions as F

# tokenisers
## already imported

## sentenisers
nltk_senteniser_body = nltkSenteniser(
    inputCol='clean_body', outputCol='body_sents')
nltk_senteniser_title = nltkSenteniser(
    inputCol='title', outputCol='titl_sents')

## loop through datasets count them per row
for i in data_array:
    print(f'On to {i}')
    datasets[i] = nltk_tokeniser_body.transform(datasets[i]).withColumn('body_word_cnt', F.size('body_words'))
    datasets[i] = nltk_tokeniser_title.transform(datasets[i]).withColumn('titl_word_cnt', F.size('titl_words'))
    datasets[i] = datasets[i].drop('body_words')
    datasets[i] = datasets[i].drop('titl_words')
    datasets[i] = nltk_senteniser_body.transform(datasets[i]).withColumn('body_sent_cnt', F.size('body_sents'))
    datasets[i] = nltk_senteniser_title.transform(datasets[i]).withColumn('titl_sent_cnt', F.size('titl_sents'))
    datasets[i] = datasets[i].drop('body_sents')
    datasets[i] = datasets[i].drop('titl_sents')
    datasets[i] = datasets[i].withColumn('body_char_cnt', F.length('clean_body'))
    datasets[i] = datasets[i].withColumn('titl_char_cnt', F.length('title'))


##################################################
###### Don't have to define y_ravi response ######
##################################################

## create response variable normalised by views
'''for i in data_array:
    datasets[i] = datasets[i].withColumn('y_ravi', datasets[i]['score']/datasets[i]['viewcount'])
    round_mean = round(datasets[i].select("y_ravi").rdd.flatMap(lambda x: x).mean(),7)
    print(f"The average value of \033[94m{i}\033[0m y_ravi is {round_mean}")'''