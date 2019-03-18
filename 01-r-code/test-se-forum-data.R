### Brad Carruthers ###

## NEED TO FIX: a function to automatically load all the files in the current directory into R 
read_dir_xmls <- function(path) {
  setwd(path)
  require(XML)
  
  ## create list to store datasets
  dat <- NULL
  
  ## run through files in directory, storing them in something (need to fix) to return the datasets later
  for (i in 1:length(list.files())) {
    dat <- c(dat, xmlToList(xmlParse(list.files()[i])))
  }
  return(dat)
}

## load packages
packages = c("quanteda", "XML", "tidyr", "dplyr", "topicmodels", "ggplot2")
lapply(packages, require, character.only = TRUE)

## point to directory with data
setwd("/Users/brad/Dropbox/lse-msc/03-lent/qta-my459/final-assignment/data/anime.stackexchange.com")

## parse to list from xml, files larger than 45MB are a pain because they take ages when collecting columns
posts_lis <- xmlToList(xmlParse("Posts.xml"))
#posts_hist_lis <- xmlToList(xmlParse("PostHistory.xml")) 

## find out names of columns - some rows have extra columns like FavoriteCount and ClosedDate
names(posts_lis$row)

## select columns to include in dataset
Id <- NULL; PostTypeId <- NULL; Score <- NULL; ViewCount <- NULL; Body <- NULL
Title <- NULL; Tags <- NULL; AnswerCount <- NULL; CommentCount <- NULL; FavoriteCount <- NULL;

## choose amount of data to include
l <- length(posts_lis)

## collect columns
for (i in 1:l) { # for some reason working with length(posts_lis) crashes R
  # elongate vectors with consectutive entries
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

## create dataframe of both questions and answers, PostTypeId = 1 is question, = 2 is answer
sxdf <- as_tibble(data.frame(Id=Id, PostTypeId=PostTypeId, Score=Score, ViewCount=ViewCount, Body=Body, Title=Title, 
                             Tags=Tags, AnswerCount=AnswerCount, CommentCount=CommentCount))

## different question and answer datasets
sxdf_q <- sxdf[sxdf["PostTypeId"]==1,]
#sxdf_a <- sxdf[sxdf["PostTypeId"]==2,]

## delete variables not needed
rm("Id", "PostTypeId", "Score", "ViewCount", "Body", "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount", "sxdf")

## convert factor columns to numeric and character
sxdf_q$Body <- as.character(sxdf_q$Body)
sxdf_q$Title <- as.character(sxdf_q$Title)
sxdf_q$AnswerCount <- as.integer(sxdf_q$AnswerCount)
sxdf_q$CommentCount <- as.integer(sxdf_q$CommentCount)

## create response variable using pca on 4 scaled factors: 
# normed answer numbers, normed score, normed answer scores, sentiment of answers
# right now, hard to match answers and questions
# upvotes are indication that people want to see answer, not of question quality or likelihood

y1 <- sxdf_q["Score"]/sxdf_q["ViewCount"] # proxy for popularity of question 
y2 <- sxdf_q["AnswerCount"]/sxdf_q["ViewCount"] # proxy for educational engagement of question
y3 <- sxdf_q["CommentCount"]/sxdf_q["ViewCount"] # proxy for recreational engagement of question

## compute pca
y_pca <- prcomp(data.frame(y1, y2, y3),
                 center = TRUE,
                 scale. = TRUE) 

## first principal component accounts for 54% of variance
pca_nb <- summary(y_pca)$importance[2,1]*100
cat("first principal component accounts for", pca_nb, "% of variance\n")
target <- y_pca$x[,1]

## plot and compare first principal components across datasets:
#temp <- NULL
temp <- c(temp, pca_nb)
temp2 <- temp
temp_names <- c("boardgames", "law", "vegetarianism", "networkengineering", "quant", "half_rus", "anime")
df <- data.frame(Forum=temp_names, PC1_Perc=temp)
ggplot(data=df, aes(x=reorder(df$Forum, -df$PC1_Perc), y=df$PC1_Perc)) + geom_bar(stat="identity") +
  labs(x = "Fora", y = "Percentage Variance Explained by First PC")
ggsave("pca-question-data.png", plot = last_plot())

## NEED TO DISTINGUISH BETWEEN Title AND Body, just use Body for now
corp_q <- corpus(sxdf_q$Body)

## create dfm, removing urls, punctuation and stopwords
dfm_q <- dfm(corp_q, remove_url=TRUE, remove_punct = TRUE, remove=stopwords("english"), verbose=TRUE)
dfm_q <- dfm_trim(dfm_q, min_termfreq = 5, verbose=TRUE) # can't trim terms because of LDA error.

## most common words
topfeatures(dfm_q, 25)

## "best" question based on first principal component
sxdf_q[y_pca$x[,1]==max(target),]

## "best" question based only on Score/ViewCount
sxdf_q[sxdf_q$Score/sxdf_q$ViewCount==max(sxdf_q$Score/sxdf_q$ViewCount),]

## "worst" question based on first principal component
sxdf_q[y_pca$x[,1]==min(target),]

## "worst" question based only on Score/ViewCount
sxdf_q[sxdf_q$Score/sxdf_q$ViewCount==min(sxdf_q$Score/sxdf_q$ViewCount),]



## implement LDA model
K <- 10
lda <- LDA(dfm_q, k = K, method = "Gibbs", 
           control = list(verbose=25L, seed = 1777, burnin = 100, iter = 1000))

terms <- get_terms(lda, 20)
terms[,1]
topics <- get_topics(lda, 1)
head(topics)

## choose topic 22 on Korea
terms[,22]

## have a look at a random tweet in this topic
sample(tweets$text[topics==22], 1)

# add predicted topic to dataset
tweets$pred_topic <- topics











y_bin[y>0.009] <- 1 # CRUCIAL STEP choosing threshold for classification here

## create dataframe of both questions and answers, PostTypeId = 1 is question, otherwise answer
sxdf <- as_tibble(data.frame(y=y, y_Binary=y_bin, Title=Title, Body=Body))

## different question and answer datasets
sxdf_q <- sxdf[!is.na(sxdf["Title"]),]
sxdf_a <- sxdf[is.na(sxdf["Title"]),]

## "best" question
sxdf_q[sxdf_q$y==max(sxdf_q$y),]

## "worst" question
sxdf_q[sxdf_q$y==min(sxdf_q$y),]

## load packages
packages = c("doMC", "glmnet")
lapply(packages, require, character.only = TRUE)

## set seed and find train/test indices
set.seed(1777)
training <- sample(1:nrow(sxdf_q), floor(.80 * nrow(sxdf_q)))
test <- (1:nrow(sxdf_q))[1:nrow(sxdf_q) %in% training == FALSE]

## cross validation
registerDoMC(cores=3)
ridge <- cv.glmnet(dfm_q[training,], sxdf_q$y_Binary[training], 
                   family="binomial", alpha=0, nfolds=5, parallel=TRUE, intercept=TRUE,
                   type.measure="class")
plot(ridge)

### PABLO BARBERA ###

## function to compute accuracy
accuracy <- function(ypred, y){
  tab <- table(ypred, y)
  return(sum(diag(tab))/sum(tab))
}

## function to compute precision
precision <- function(ypred, y){
  tab <- table(ypred, y)
  return((tab[2,2])/(tab[2,1]+tab[2,2]))
}

## function to compute recall
recall <- function(ypred, y){
  tab <- table(ypred, y)
  return(tab[2,2]/(tab[1,2]+tab[2,2]))
}

## computing predicted values
preds <- predict(ridge, dfm_q[test,], type="class")

## confusion matrix
table(preds, sxdf_q$y_Binary[test])

## performance metrics
accuracy(preds, sxdf_q$y_Binary[test]) # we got 57% of all predictions right

precision(preds==1, sxdf_q$y_Binary[test]==1) # out of what we said, we got 57% right

recall(preds==1, sxdf_q$y_Binary[test]==1) # out of what we should have said quality, 70% were quality

precision(preds==0, sxdf_q$y_Binary[test]==0)

recall(preds==0, sxdf_q$y_Binary[test]==0)





