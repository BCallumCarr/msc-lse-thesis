#####################################
###### LDA feature engineering ######
#####################################

## import ml libraries and define transformers
from pyspark.ml.feature import CountVectorizer, IDF

# tokenisers
nltk_tokeniser_body = nltkWordPunctTokeniser(
    inputCol='clean_body', outputCol='body_words',  
    stopwords=set(nltk.corpus.stopwords.words('english'))
    )
nltk_tokeniser_title = nltkWordPunctTokeniser(
    inputCol='title', outputCol='titl_words',  
    stopwords=set(nltk.corpus.stopwords.words('english')))
## sentenisers
nltk_senteniser_body = nltkSenteniser(
    inputCol='clean_body', outputCol='body_sents')
nltk_senteniser_title = nltkSenteniser(
    inputCol='title', outputCol='titl_sents')

# counters
cnt_vectrizr_body = CountVectorizer(inputCol='body_words', outputCol='body_feats') #!!! minDF???
cnt_vectrizr_title = CountVectorizer(inputCol='titl_words', outputCol='titl_feats')
cnt_vectrizr_sents = CountVectorizer(inputCol='body_sents', outputCol='body_sent_feats')

# to IDF matrix
to_idf_body = IDF(inputCol='body_feats', outputCol='features')
to_idf_title = IDF(inputCol='titl_feats', outputCol='features')
to_idf_sents = IDF(inputCol='body_sent_feats', outputCol='features')

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
# maxIter needs to be at least 20 to pass through whole dataset since batchsize default is 5%
lda = LDA(k=10, maxIter=20, optimizer='online', topicConcentration=0.01, docConcentration=[0.01])

lda_model_list = {}
cntvcr_models = {}

## loop through datasets for LDA modelling
for i in data_array:
    print(f'On to {i}')
    
    ### BODY TOKENS
    # body transformers
    tokens_body = nltk_tokeniser_body.transform(datasets[i])
    cntvcr_models[i] = cnt_vectrizr_body.fit(tokens_body)
    counts_body = cntvcr_models[i].transform(tokens_body)
    idf_body = to_idf_body.fit(counts_body).transform(counts_body)
    
    # fit LDA model on body tokens
    lda_model_list[i] = lda.fit(idf_body)
    datasets[i] = lda_model_list[i].transform(idf_body)
    
    # get topicDist on body tokens
    datasets[i] = datasets[i].withColumn("btd", to_array(col("topicDistribution"))).\
        select(["*"] + [col("btd")[i] for i in range(10)])
    
    # drop unnecessary columns
    datasets[i] = datasets[i].drop('features').drop('topicDistribution')
    

    ### BODY SENTENCES
    # body sentence transformer
    sents_body = nltk_senteniser_body.transform(datasets[i])
    count_sents_body = cnt_vectrizr_sents.fit(sents_body).transform(sents_body)
    idf_sents_body = to_idf_sents.fit(count_sents_body).transform(count_sents_body)

    # fit LDA model on body sentences
    #datasets[i] = lda.fit(idf_sents_body).transform(idf_sents_body)

    # get topicDist on body sentences tokens
    #datasets[i] = datasets[i].withColumn("std", to_array(col("topicDistribution"))).\
    #    select(["*"] + [col("std")[i] for i in range(10)])

    # drop unnecessary columns
    #datasets[i] = datasets[i].drop('features').drop('topicDistribution')

    ### TITLE TOKENS
    # title transformers
    tokens_title = nltk_tokeniser_title.transform(datasets[i])
    counts_title = cnt_vectrizr_title.fit(tokens_title).transform(tokens_title)
    idf_title = to_idf_title.fit(counts_title).transform(counts_title)

    # fit LDA model on title tokens
    datasets[i] = lda.fit(idf_title).transform(idf_title)
    
    # get topicDist on title tokens
    datasets[i] = datasets[i].withColumn("ttd", to_array(col("topicDistribution"))).\
        select(["*"] + [col("ttd")[i] for i in range(10)])

    # drop unnecessary columns
    datasets[i] = datasets[i].drop('btd').drop('ttd').drop('std').drop('titl_feats').\
        drop('body_feats').drop('body_sent_feats').drop('features').drop('topicDistribution')
    
#################################################
###### Print topics ######
#################################################

## first 5 words of the 10 topics from the LDA models per forum
topic_list = {}
fin_array = []
for i in data_array:
    print("\n------------------\n", i, "\n------------------\n")
    topic_list[i] = lda_model_list[i].describeTopics(7)
    #print("The topics described by their top-weighted terms:\n")
    #topic_list[i].show(truncate=False)
    # show the results
    topic_j = topic_list[i].select("termIndices").rdd.map(lambda r: r[0]).collect()
    for j in topic_j:
        fin_array.append(np.array(cntvcr_models[i].vocabulary)[j])
    print('\n')
print(pd.DataFrame(fin_array).to_latex())

#################################################
###### Character, word and sentence counts ######
#################################################

## import pyspark functions (transformers already defined)
from pyspark.sql.functions import size, length

## loop through datasets count them per row
for i in data_array:
    print(f'On to {i}')
    datasets[i] = nltk_tokeniser_body.transform(datasets[i]).withColumn('body_word_cnt', size('body_words'))
    datasets[i] = nltk_tokeniser_title.transform(datasets[i]).withColumn('titl_word_cnt', size('titl_words'))
    datasets[i] = datasets[i].drop('body_words')
    datasets[i] = datasets[i].drop('titl_words')
    datasets[i] = nltk_senteniser_body.transform(datasets[i]).withColumn('body_sent_cnt', size('body_sents'))
    datasets[i] = nltk_senteniser_title.transform(datasets[i]).withColumn('titl_sent_cnt', size('titl_sents'))
    datasets[i] = datasets[i].drop('body_sents')
    datasets[i] = datasets[i].drop('titl_sents')
    datasets[i] = datasets[i].withColumn('body_char_cnt', length('clean_body'))
    datasets[i] = datasets[i].withColumn('titl_char_cnt', length('title'))