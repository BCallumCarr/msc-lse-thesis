%%time

## tokenise and lemmatise using nltk function from import step
body_rdd = {}
for i in data_array:
    body_rdd[i] = datasets[i].select('clean_body').rdd.flatMap(lambda r: r).map(lambda line: (1, get_tokens(line)))

%%time

## look at first 10 terms from first post in english
print(body_rdd['english'].take(1)[0][1][:30])

'''RUN LATER'''

# get rid of stop words
doc_stopwords = {}
for i in data_array:
    doc_stopwords[i] = body_rdd[i].flatMap(lambda r: r[1]).map(lambda r: (r,1)).reduceByKey(lambda a,b: a+b)
    # here we assume that words that appear very frequently are stop words
    doc_stopwords[i] = doc_stopwords[i].filter(lambda a: a[1]>3000).map(lambda r: r[0]).collect()
    '''3000 threshold needs attention!'''
    # remove stopwords and single letters
    body_rdd[i] = body_rdd[i].map(lambda r: (r[0],[w for w in r[1] if not w in doc_stopwords[i] and not len(w)==1]))

'''BOTTLENECK TIME - JUST USE english FOR NOW'''
data_array = ['english']

%%time

from pyspark.ml.feature import CountVectorizer

## convert tokens into sparse vectors
body_df = {}
for i in data_array:
    body_df[i] = spark.createDataFrame(body_rdd[i], ["dummy","words"])
    body_df[i].cache()

%%time
## check first english post vector
show_spark_df(body_df['english'])

## garbage collector to speed up computation
import gc
collected = gc.collect()
print("Garbage collector: collected %d objects." % collected)

%%time
print(datetime.now().time())

cntvcr = CountVectorizer(inputCol="words", outputCol="features", minDF=2)

cntvcr_models = {}
word_feat_list = {}
for i in data_array:
    cntvcr_models[i] = cntvcr.fit(body_df[i])
    word_feat_list[i] = cntvcr_models[i].transform(body_df[i])
    word_feat_list[i].cache()

## show word vectors and feature counts for fora:
for i in data_array:
    print("\n------------------\n", i, "\n------------------\n")
    word_feat_list[i].show(10)

%%time
print(datetime.now().time())

# converting pyspark.ml vectors to pyspark.mllib vectors

from pyspark.mllib.linalg import Vectors
def as_mllib_vector(v):
    return Vectors.sparse(v.size, v.indices, v.values)

features = {}
feature_vec_list = {}
for i in data_array:
    features[i] = word_feat_list[i].select("features")
    feature_vec_list[i] = features[i].rdd.map(lambda r: as_mllib_vector(r[0]))
    feature_vec_list[i].cache()

## print first pyspark.mllib vector across fora:
for i in data_array:
    print("\n------------------\n", i, "\n------------------\n")
    print(feature_vec_list[i].take(1))

## look at the first 100 words of the vocabulary
for i in data_array:
    print("\n------------------\n", i, "\n------------------\n")
    print ("Vocabulary from CountVectorizerModel is:\n")
    print(cntvcr_models[i].vocabulary[:100])
    print("\n---\n")

    M = len(cntvcr_models[i].vocabulary)
    print("Number of terms M = ", M)

###################################################################################################
############################################ LDA MODEL ############################################
###################################################################################################

%%time
print(datetime.now().time())

## fit LDA models with k=10 topics
from pyspark.ml.clustering import LDA

lda = LDA(k=10, maxIter=5)

lda_model_list = {}
for i in data_array:
    lda_model_list[i] = lda.fit(word_feat_list[i])

%%time
print(datetime.now().time())
'''BOTTLENECK TIME - TAKES OVER 45 min JUST FOR ENGLISH'''

# calculate the perplexity and likelihood for each forum's model

loglik_list = {}
logper_list = {}
for i in data_array:
    loglik_list[i] = lda_model_list[i].logLikelihood(word_feat_list[i])
    logper_list[i] = lda_model_list[i].logPerplexity(word_feat_list[i])
    print("Finished", i, "at", datetime.now().time())

# low perplexity value indicates the model predicts the sample well

for i in data_array:
    print("The lower bound on the log likelihood of the " +'\033[1m'+ i +'\033[0m'+ " corpus is: " + str(loglik_list[i]))
    print("The upper bound on the perplexity of the " +'\033[1m'+ i +'\033[0m'+ " corpus is: " + str(logper_list[i]))
    print('\n')

%%time
print(datetime.now().time())

## first 5 words of the 10 topics from the LDA models per forum
topic_list = {}
for i in data_array:
    print("\n------------------\n", i, "\n------------------\n")
    topic_list[i] = lda_model_list[i].describeTopics(5)
    #print("The topics described by their top-weighted terms:\n")
    #topic_list[i].show(truncate=False)
    # show the results
    topic_j = topic_list[i].select("termIndices").rdd.map(lambda r: r[0]).collect()
    for j in topic_j:
        print(np.array(cntvcr_models[i].vocabulary)[j])
    print('\n')