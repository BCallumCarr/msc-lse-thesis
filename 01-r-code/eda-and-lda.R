### Brad Carruthers ###

#####################################################################
############################# LOAD DATA #############################
#####################################################################

## choose datasets
datasets <- c(
  #"anime",
  #"boardgames",
  #"buddhism",
  #"emacs",
  #"law",
  #"networkengineering",
  #"quant",
  #"rus",
  "beer",
  "opensource"
)

## load packages
packages = c("quanteda", "XML", "tidyr", "dplyr", "topicmodels", "ggplot2", "caret", "quanteda.dictionaries", "stargazer")
lapply(packages, require, character.only = TRUE)

## set random seed
set.seed(1777)

### LOOP THROUGH ALL DATASETS
dataset_stats <- list()
for (k in 1:length(datasets)) {
  
  ## point to directory with data
  cat("\n------------------\n", datasets[k], "\n------------------\n")
  dir <- paste("/Users/brad/Dropbox/lse-msc/03-lent/qta-my459/final-assignment/data/", datasets[k], ".stackexchange.com/Posts.xml",
               sep = "")
  
  ## parse to list from xml, files larger than 45MB are a pain because they take ages when collecting columns
  posts_lis <- xmlToList(xmlParse(dir))
  
  ## find out names of columns - some rows have extra columns like FavoriteCount and ClosedDate
  names(posts_lis$row)
  
  ## select columns to include in dataset
  Id <- NULL; PostTypeId <- NULL; Score <- NULL; ViewCount <- NULL; Body <- NULL
  Title <- NULL; Tags <- NULL; AnswerCount <- NULL; CommentCount <- NULL; FavoriteCount <- NULL;
  
  ## choose amount of data to include
  l <- length(posts_lis)
  
  ## collect columns
  for (i in 1:l) { # for some reason working with length(posts_lis) crashes R
    # elongate vectors with consecutive entries
    # remember: these include both answers and questions
    Id <- as.integer(c(Id, posts_lis[i]$row['Id']))
    PostTypeId <- as.integer(c(PostTypeId, posts_lis[i]$row['PostTypeId']))
    Score <- as.integer(c(Score, posts_lis[i]$row['Score']))
    ViewCount <- as.integer(c(ViewCount, posts_lis[i]$row['ViewCount']))
    Body <- as.character(c(Body, posts_lis[i]$row['Body']))
    Title <- as.character(c(Title, posts_lis[i]$row['Title']))
    Tags <- as.character(c(Tags, posts_lis[i]$row['Tags']))
    AnswerCount <- as.character(c(AnswerCount, posts_lis[i]$row['AnswerCount']))
    CommentCount <- as.character(c(CommentCount, posts_lis[i]$row['CommentCount']))
    # don't include FavoriteCount because of missing values
  }
  
  for (i in 1:length(Body)) {
    ## get rid of some html ugliness
    Body[i] <- gsub('\n|<.*?>'," ", Body[i])
  }
  
  ## create dataframe of both questions and answers, PostTypeId = 1 is question, = 2 is answer and convert factor columns
  sxdf <- as_tibble(data.frame(Id=Id, PostTypeId=PostTypeId, Score=Score, ViewCount=ViewCount, Body=Body, 
                               Title=as.character(Title), Tags=Tags, AnswerCount=as.integer(AnswerCount), 
                               CommentCount=as.integer(CommentCount)))
  
  ## convert to character
  sxdf$Body <- as.character(sxdf$Body)
  sxdf$Title <- as.character(sxdf$Title)
  
  ## different question and answer datasets
  sxdf_q <- sxdf[sxdf["PostTypeId"]==1,]
  #sxdf_a <- sxdf[sxdf["PostTypeId"]==2,]
  cat("This forum has", nrow(sxdf_q), "questions\n")
  
  ## delete variables not needed
  rm("Id", "PostTypeId", "Score", "ViewCount", "Body", "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount", "sxdf")
  
  
  
  #####################################################################
  ######################### BINARY CLASSIFIER #########################
  #####################################################################
  
  ## plot cumulative view counts
  ggplot(as.data.frame(sxdf_q$ViewCount), aes(sxdf_q$ViewCount)) + 
    stat_ecdf(geom = "step") + scale_x_continuous(trans='log10') + 
    labs(x = "ViewCount", y = "Cumulative % of Question Posts")
  
  ## find threshold for views
  thresh <- round(quantile(sxdf_q$ViewCount, .40), -1)
  
  ## focus on questions above threshold to address possibility of users that can vote not seeing question
  temp <- nrow(sxdf_q)
  sxdf_q <- sxdf_q[sxdf_q$ViewCount > thresh,]
  temp <- temp - nrow(sxdf_q)
  cat("Removed", temp, "questions above threshold of", thresh, "views\n")
  
  ## create response variable normalised by views
  sxdf_q$y <- sxdf_q["Score"]/sxdf_q["ViewCount"]
  cat("The average value of y is", round(mean(sxdf_q$y$Score),3), '\n')
  cat("Conditioned on positive y the average is", round(mean(sxdf_q$y[sxdf_q$y>0]),3), "\n")
  
  ## MUST INCORPORATE INTO FUNCTION
  ## "best" question based on Score/ViewCount
  sxdf_q[sxdf_q$y==max(sxdf_q$y),][,c("Score", "ViewCount", "Body", "y")]
  
  ## "worst" question based on Score/ViewCount
  sxdf_q[sxdf_q$y==min(sxdf_q$y),][,c("Score", "ViewCount", "Body", "y")]
  
  ## label questions
  # Ravi et al randomly choose y>0.001 as threshold for quality question? 
  y_thresh <- round(mean(sxdf_q$y$Score),3)/2 ## CRITICAL STEP
  sxdf_q$y <- factor(ifelse(sxdf_q$y <= y_thresh, 0, 1), labels=c("bad","good"))
  cat("With an arbitrarily chosen y threshold of", y_thresh, "there are apparently", sum(sxdf_q$y=="good"), 
      "good questions, (", round(sum(sxdf_q$y=="good")/nrow(sxdf_q),2)*100, "%)\n\n")
  
  
  
  #####################################################################
  ########################### VALIDATION ##############################
  #####################################################################
   
  linguistic_descriptives <- dget("/Users/brad/Dropbox/lse-msc/03-lent/qta-my459/final-assignment/r-code/linguistic_descriptives.R")
  dataset_stats[[k]] <- data.frame(linguistic_descriptives(sxdf_q))
  
  ### END LOOP FOR NOW
} 













################### word predictors of quality ###################

## Body
head(textstat_keyness(dfm(sxdf_q[sxdf_q$y=='good',]$Body)))
head(textstat_keyness(dfm(sxdf_q[sxdf_q$y=='bad',]$Body)))

## Title
head(textstat_keyness(dfm(sxdf_q[sxdf_q$y=='good',]$Title)))
head(textstat_keyness(dfm(sxdf_q[sxdf_q$y=='bad',]$Title)))


################### topic predictors of quality ###################

## create lda dfm

#corp_q <- corpus(sxdf_q$Body)
#corp_q_shuff <- corpus_sample(corp_q, size = nrow(sxdf_q))
#dfm_rem <- c(stopwords("english"), "amp", "don", "#x200b", "b", "m", "r", "s", "t", "http", "https", "1", "2", "3", "4")
dfm_q <- dfm(sxdf_q$Body, 
             #remove_url=TRUE, 
             remove_punct = TRUE, 
             remove_numbers=TRUE, 
             remove=stopwords("english"), 
             verbose=TRUE)

## eda lda model
K <- 30
eda_lda <- LDA(dfm_q, k = K, method = "Gibbs", 
               control = list(verbose=25L, seed = 1777, burnin = 100, iter = 1000))

## have a look at the topics
terms <- get_terms(eda_lda, 12)
terms

## assign topics
topics <- get_topics(eda_lda, 1)
sxdf_q$pred_topic <- as.factor(topics)

## have a look at a random post with a topic
sample(sxdf_q$Body[topics==23], 1)

## create dataframe skeleton
topic_df <- tibble(topic = 1:K, prop = rep(NA))

## find out which topics associated with good questions
for (i in 1:K) {
  topic_df[i,1] <- paste(terms[1:12,i], collapse=", ")
  topic_df[i,2] <- 2-mean(as.numeric(sxdf_q$y[sxdf_q$pred_topic==i]))
}

## print
topic_df[order(topic_df$prop, decreasing=TRUE),]
topic_df[order(topic_df$prop, decreasing=FALSE),]




if (FALSE) {
  ## get terms and explore terms of first topic
  terms <- get_terms(lda, 20)
  terms[,1]
  ## get topics and explore documents' primary topic
  head(topics)
  ## have a look at random question related to a topic
  terms[,1]
  sample(sxdf_q$Body[topics==1], 1)
}

glob_topic <- get_topics(lda, 1)

# add predicted topic to dataset
sxdf_q$pred_glob_topic <- glob_topic



#####################################################################
########################### PREDICTION ##############################
#####################################################################

## just using Body for now, NEED TO INCLUDE Title
# shuffle corpus
corp_q <- corpus(sxdf_q$Body)
corp_q_shuff <- corpus_sample(corp_q, size = 1961)

## create dfm with tri-grams, removing urls, punctuation and stopwords
dfm_q <- dfm(corp_q_shuff, 
             #remove_url=TRUE, 
             ngrams = c(2, 3), 
             remove_punct = TRUE, 
             remove=stopwords("english"), 
             verbose=TRUE)

dfm_q <- dfm_trim(dfm_q, min_termfreq = 20, verbose=TRUE)

## most common words
topfeatures(dfm_q, 25)



## load packages
packages = c("doMC", "glmnet")
lapply(packages, require, character.only = TRUE)
registerDoMC(cores=3)

## RAVI: DOWNSAMPLE GOOD QUESTIONS TO CREATE EQUAL DISTRIBUTION OF GOOD/BAD SAMPLES
# create target vector
in_train <- as.numeric(createDataPartition(sxdf_q$y_bin, p = 0.7, list = FALSE))
target <- sxdf_q$y_bin

######################################################################################################################################

## VIEW AND ANSWER COUNT MODEL

log_reg_vc <- glm(target[in_train] ~ sxdf_q$ViewCount[in_train] + sxdf_q$AnswerCount[in_train],
                  family="binomial"
)

## predicting labels for test set
preds <- predict(log_reg_vc, newdata=as.data.frame(X[-in_train,]), type="response")
preds <- preds[-in_train]
preds[preds>0.5] <- 1
preds[preds<0.5] <- 0

## computing the confusion matrix
cm <- table(preds, target[-in_train])

### classification metrics function
classif_metrics <- function(mytable, verbose=TRUE, reverse=FALSE) {
  if (reverse==TRUE) {
    mytable <- mytable[2:1, 2:1]
  }
  truePositives <- mytable[1,1]
  falsePositives <- sum(mytable[1,]) - truePositives
  falseNegatives <- sum(mytable[,1]) - truePositives
  precision <- truePositives / (truePositives + falsePositives)
  recall <- truePositives / (truePositives + falseNegatives)
  f1_score <- 2*precision*recall / (precision + recall)
  accuracy <- (mytable[1,1]+mytable[2,2])/sum(mytable)
  if (verbose) {
    print(mytable)
    cat("\n accuracy =", round(accuracy, 2),
        "\n precision =", round(precision, 2), 
        "\n recall =", round(recall, 2),
        "\n F1 Score =", round(f1_score, 2), "\n")
  }
  invisible(c(precision, recall, f1_score, accuracy))
}

## metrics for positive category
classif_metrics(cm, reverse=F)


######################################################################################################################################

## FEATURE ENGINEERING

## global topic
K <- 1
global_lda <- LDA(dfm_q, k = K, method = "Gibbs", 
                  control = list(verbose=25L, seed = 1777, burnin = 100, iter = 1000))

if (FALSE) {
  ## get terms and explore terms of first topic
  terms <- get_terms(lda, 20)
  terms[,1]
  ## get topics and explore documents' primary topic
  head(topics)
  ## have a look at random question related to a topic
  terms[,1]
  sample(sxdf_q$Body[topics==1], 1)
}

glob_topic <- get_topics(lda, 1)

# add predicted topic to dataset
sxdf_q$pred_glob_topic <- glob_topic

######################################################################################################################################

## create feature matrix
X <- colbind(dfm_q, topics)

## cross validation
ridge <- cv.glmnet(x=X[in_train,], y=target[in_train], 
                   family="binomial", alpha=1, nfolds=10, parallel=TRUE, 
                   type.measure ="class",
                   intercept=TRUE
)
plot(ridge)

## predicting labels for test set
(preds <- predict(ridge, X[-in_train,] , type="class"))

## computing the confusion matrix
cm <- table(preds, target[-in_train])

## metrics for positive category
classif_metrics(cm, reverse=F)


