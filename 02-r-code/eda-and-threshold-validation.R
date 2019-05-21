### Brad Carruthers ###

## save file
rstudioapi::documentSave(rstudioapi::getActiveDocumentContext()$id)

#################################################################
############################# SETUP #############################
#################################################################

## choose datasets
datasets <- c(
  # total is 49 min
  # "buddhism", #2226 20min 6min
  "economics" #2458 40min 7min
  # "fitness", #2504 40min 9min
  # "health", #1866 15min 3min
  #"interpersonal" #1398 6min 3min 6minFULL
  # "linguistics", #2411 42min 7min
  # "outdoors", #1885 13min 4min
  # "spanish" #2135 8min
  
  # TOO BIG:
  #"emacs" - 5584, "quant" - 4248, "networkengineering" - 3753, "gardening" - 3863, "anime" - 3209 & 57min
  #"french" - 2889 & 55min, "law" - 3649, "boardgames" - 3527 & 49min, "astronomy" - 2448 & 29min, "robotics" - 1333 & 17min
  
  # SMALL:
  # "vegetarianism", #220
  # "beer" #320,
  # "opensource" #806 - weird stuff happens here - WHAT WEIRD STUFF??
)

## load packages
packages = c("quanteda", 
             "quanteda.dictionaries",
             "XML", 
             "tidyverse", 
             "topicmodels", 
             "stargazer", 
             "stringi",
             "scales", 
             "caret"  
             )
lapply(packages, require, character.only = TRUE)

## set random seed
set.seed(1777)

## store result lists
dataset_stats <- list() # to store results from linguistic_descriptives
best_worst_qs <- list() # to store example questions
init_viewcount_list <- list() # to store example questions
threshold_list <- list() # to store threshold similarity and jaccard similarity values
count_desc_list <- list() # to store counts
score_desc_list <- list() # to store scores

## timing
start_time <- Sys.time()


#####################################################################
############################# LOAD DATA #############################
#####################################################################

for (k in 1:length(datasets)) {
  
  ## garbage collection and timing
  gc()
  loop_start_time <- Sys.time()
  
  ## point to directory with data
  cat("\n------------------\n", datasets[k], "\n------------------\n")
  cat("The time is", format(Sys.time(), "%X"), "\n\n")
  dir <- paste("/Users/brad/Dropbox/lse-msc/03-lent/qta-my459/final-assignment/data/", datasets[k], 
               ".stackexchange.com/Posts.xml", sep = "")
  
  ## parse to list from xml, files larger than 45MB are a pain because they take ages when collecting columns
  posts_lis <- xmlToList(xmlParse(dir))
  
  ## find out names of columns - some rows have extra columns like FavoriteCount and ClosedDate
  names(posts_lis$row)
  
  ## select columns to include in dataset
  Id <- NULL; PostTypeId <- NULL; AcceptedAnswerId <- NULL; CreationDate <- NULL; Score <- NULL; ViewCount <- NULL; 
  Body <- NULL; OwnerUserId <- NULL; LastEditorUserId <- NULL; LastEditDate <- NULL; LastActivityDate <- NULL; 
  Title <- NULL; Tags <- NULL; AnswerCount <- NULL; CommentCount <- NULL; FavoriteCount <- NULL; ClosedDate <- NULL;
  
  ## choose amount of data to include
  l <- length(posts_lis)
  
  ## collect columns
  for (i in 1:l) { # for some reason working with length(posts_lis) here crashes R
    # elongate vectors with consecutive entries
    # remember: these include both answers and questions, AND apparently mod comments/answers
    #Id <- as.integer(c(Id, posts_lis[i]$row["Id"])) # comment out to speed up
    PostTypeId <- as.integer(c(PostTypeId, posts_lis[i]$row["PostTypeId"]))
    #AcceptedAnswerId <- as.integer(c(AcceptedAnswerId, posts_lis[i]$row["AcceptedAnswerId"])) # comment out to speed up
    #CreationDate <- as.character(c(CreationDate, posts_lis[i]$row["CreationDate"])) # comment out to speed up
    Score <- as.integer(c(Score, posts_lis[i]$row["Score"]))
    ViewCount <- as.integer(c(ViewCount, posts_lis[i]$row["ViewCount"]))
    Body <- as.character(c(Body, posts_lis[i]$row["Body"]))
    #OwnerUserId <- as.integer(c(OwnerUserId, posts_lis[i]$row["OwnerUserId"])) # comment out to speed up
    #LastEditorUserId <- as.integer(c(LastEditorUserId, posts_lis[i]$row["LastEditorUserId"])) # comment out to speed up
    #LastEditDate <- as.character(c(LastEditDate, posts_lis[i]$row["LastEditDate"])) # comment out to speed up
    #LastActivityDate <- as.character(c(LastActivityDate, posts_lis[i]$row["LastActivityDate"])) # comment out to speed up
    Title <- as.character(c(Title, posts_lis[i]$row["Title"]))
    #Tags <- as.character(c(Tags, posts_lis[i]$row["Tags"])) # comment out to speed up
    #AnswerCount <- as.integer(c(AnswerCount, posts_lis[i]$row["AnswerCount"]))
    #CommentCount <- as.integer(c(CommentCount, posts_lis[i]$row["CommentCount"]))
    #FavoriteCount <- as.integer(c(FavoriteCount, posts_lis[i]$row["FavoriteCount"])) # comment out to ignore due to NAs
    #ClosedDate <- as.character(c(ClosedDate, posts_lis[i]$row["ClosedDate"])) # comment out to speed up
  }
  
  ## reading in timing
  cat("After reading the data in we're at", round(Sys.time()-loop_start_time), "minutes\n")
  
  ## testing
  index <- PostTypeId %in% c(1, 2)
  head(cbind(Id[index], PostTypeId[index], AcceptedAnswerId[index]), 20)
  
  for (i in 1:length(Body)) {
    ## get rid of some html ugliness
    Body[i] <- gsub("\n|<.*?>"," ", Body[i])
  }
  
  ## create dataframe of both questions and answers, PostTypeId = 1 is question, = 2 is answer and convert factor columns
  sxdf <- as_tibble(data.frame(
    #Id=Id, # comment out to speed up
    PostTypeId=PostTypeId,
    #AcceptedAnswerId=AcceptedAnswerId, # comment out to speed up
    #CreationDate=date(CreationDate), # comment out to speed up
    Score=Score,
    ViewCount=ViewCount,
    Body=as.character(Body),
    #OwnerUserId=OwnerUserId, # comment out to speed up
    #LastEditorUserId=LastEditorUserId, # comment out to speed up
    #LastEditDate=date(LastEditDate), # comment out to speed up
    #LastActivityDate=date(LastActivityDate), # comment out to speed up
    Title=as.character(Title)
    #Tags=Tags, # comment out to speed up
    #AnswerCount=as.integer(AnswerCount),
    #CommentCount=as.integer(CommentCount),
    #FavoriteCount=as.integer(FavoriteCount) # comment out to speed up
    #ClosedDate=date(ClosedDate) # comment out to speed up
    ))
  
  ## convert to character
  sxdf$Body <- as.character(sxdf$Body)
  sxdf$Title <- as.character(sxdf$Title)
  
  ## different question and answer datasets
  sxdf_q <- sxdf[sxdf["PostTypeId"]==1,]
  #sxdf_a <- sxdf[sxdf["PostTypeId"]==2,]
  cat("This forum has", nrow(sxdf_q), "questions\n")
  
  ## keep variables and delete rest
  rm(list=setdiff(ls(), c("datasets",
                          "dataset_stats",
                          "best_worst_qs",
                          "loop_start_time",
                          "init_viewcount_list",
                          "threshold_list",
                          "count_desc_list",
                          "score_desc_list",
                          "start_time",
                          "sxdf_q",
                          "k"
                          )))
  
  ## garbage collection
  gc()
  
  ## save wordcloud plot for QUESTIONS
  # file_name <- paste(datasets[k], "-q-wordcloud-plot.png", sep="")
  # png(file_name, units="in", width=5, height=5, res=300)
  # textplot_wordcloud(dfm(sxdf_q$Body, remove=c(stopwords("english"), ",", ".", "-", ";", "can"), 
  #                        remove_punct=TRUE, remove_numbers=TRUE, tolower=TRUE, stem=FALSE, verbose=TRUE), 
  #                    rotation=0, min_size=.75, max_size=3, max_words=50, min_count=10)
  # dev.off()
  
  ## save descriptives for plotting later
  init_viewcount_list[[datasets[k]]] <- sxdf_q$ViewCount
  score_desc_list[[datasets[k]]] <- sxdf_q$Score
  count_desc_list[[datasets[k]]] <- nrow(sxdf_q)
  
  
  ###########################################################################
  ############################# DEFINE RESPONSE #############################
  ###########################################################################
  
  ## find threshold for views, focus on above this for possibility users that can vote not seeing question
  ## NOT GOING TO DO THIS BECAUSE THE DATASETS ARE SO SMALL???
  thresh <- round(quantile(sxdf_q$ViewCount, .40), -1)
  temp <- nrow(sxdf_q)
  # sxdf_q <- sxdf_q[sxdf_q$ViewCount > thresh,]
  # temp <- temp - nrow(sxdf_q)
  # cat("Removed", temp, "questions below chosen threshold of", thresh, "views\n")
  cat("\nDID NOT remove any questions below a threshold of", thresh, "views\n")
  
  ##### RAVI ET AL #####
  
  ## create response variable normalised by views
  sxdf_q$y_ravi <- sxdf_q["Score"]/sxdf_q["ViewCount"]
  cat("\nThe average value of y_ravi is", round(mean(sxdf_q$y_ravi$Score),5), "\n")
  cat("Conditioned on positive y_ravi the average is", round(mean(sxdf_q$y_ravi[sxdf_q$y_ravi>0]),5), "\n")
  
  ## title of "best" and "worst" question based on Score/ViewCount
  best_worst_qs[[datasets[k]]][["ravi"]] <- rbind(
    sxdf_q[sxdf_q$y_ravi==max(sxdf_q$y_ravi),][,c("Score", "ViewCount", "Title", "y_ravi")],
    sxdf_q[sxdf_q$y_ravi==min(sxdf_q$y_ravi),][,c("Score", "ViewCount", "Title", "y_ravi")])
  
  
  #####################################################################
  ########################### VALIDATION ##############################
  #####################################################################
  
  ## choose thresholds
  threshes <- as.matrix(seq(0.05, 0.95, by=0.025))
  result <- NULL
  
  for (i in 1:length(threshes)) {
    
    ## store thresholds, lowest represents % good questions
    # if statement to change over at 50% threshold
    lo_thresh <- quantile(sxdf_q$y_ravi$Score, threshes[i])
    hi_thresh <- quantile(sxdf_q$y_ravi$Score, threshes[length(threshes)-i+1])
    
    if (i > (length(threshes) + 1) / 2) {
      ## label questions according to high and low thresholds AFTER 50% THRESHOLD
      sxdf_q[[as.character(threshes[i])]] <- factor(ifelse(sxdf_q$y_ravi > hi_thresh, 1, 0), labels=c("bad","good"))
    } else {
      ## label questions according to high and low thresholds BEFORE 50% THRESHOLD
      sxdf_q[[as.character(threshes[i])]] <- factor(ifelse(sxdf_q$y_ravi < lo_thresh, 0, 
                                                           ifelse(sxdf_q$y_ravi > hi_thresh, 1, NA)), labels=c("bad","good"))
    }
    
    ## calculate similarities
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
  }
  
  ## store result
  threshold_list[[datasets[k]]] <- result
  
  
  #####################################################################
  ####################### FINAL VALIDATION ############################
  #####################################################################
  
  ## labeling for RAVI
  y_ravi_thresh <- quantile(sxdf_q$y_ravi$Score, 1 - 0.6)
  sxdf_q$y_ravi_fin <- factor(ifelse(sxdf_q$y_ravi <= y_ravi_thresh, 0, 1), labels=c("bad","good"))
  cat("\nWith an arbitrarily chosen Ravi threshold of", y_ravi_thresh, "there are apparently", sum(sxdf_q$y_ravi_fin=="good"),
      "good questions, (", round(sum(sxdf_q$y_ravi_fin=="good")/nrow(sxdf_q),2)*100, "%)\n")
  
  ## labeling for CARR
  y_carr_thresh <- quantile(sxdf_q$y_ravi$Score, 1 - 0.75)
  sxdf_q$y_carr_fin <- factor(ifelse(sxdf_q$y_ravi <= y_carr_thresh, 0, 1), labels=c("bad","good"))
  cat("With an arbitrarily chosen Carr threshold of", y_carr_thresh, "there are apparently", sum(sxdf_q$y_carr_fin=="good"),
      "good questions, (", round(sum(sxdf_q$y_carr_fin=="good")/nrow(sxdf_q),2)*100, "%)\n\n")
  
  ## load in function for table of statistical differences
  final_ling_descs <- dget("/Users/brad/Dropbox/lse-msc/03-lent/qta-my459/final-assignment/r-code/final_ling_descs.R")
  
  ## run function
  dataset_stats[[datasets[k]]] <- data.frame(final_ling_descs(sxdf_q, target=sxdf_q$y_ravi_fin, new_target=sxdf_q$y_carr_fin))
  
  
  ##############
  
  ## end timing
  cat("\nThis took", round(Sys.time()-loop_start_time), "minutes overall!\n")
  
  ## keep variables and delete rest
  rm(list=setdiff(ls(), c("datasets",
                          "dataset_stats",
                          "best_worst_qs",
                          "init_viewcount_list",
                          "threshold_list",
                          "count_desc_list",
                          "score_desc_list",
                          "start_time"
                          )))
}

## end-time
cat("\n------------------\n", "\nThe entire analyses took", round(Sys.time()-start_time), "minutes\n")



################################################################
########################### PLOTS ##############################
################################################################


## plot and save question count
df <- data.frame(forum=names(unlist(count_desc_list)), count=unlist(count_desc_list))
p <- ggplot(df, aes(x=reorder(df$forum, -df$count), y=df$count)) + geom_bar(stat="identity") +
  labs(x = "Fora", y = "Number of Questions") +
  theme(text = element_text(size=30), axis.text.x=element_text(angle=90,hjust=1))
png("q-count-bar-graph.png", units="in", width=12, height=9, res=300)
print(p)
dev.off()

## plot and save average score
df <- data.frame(score=unlist(score_desc_list)) %>%
  # put in to tidy format for ggplot
  mutate(forum=unlist(stri_extract_all_regex(names(unlist(score_desc_list)), "[A-Za-z]+"))) %>% 
  group_by(forum) %>%
  summarise(avg = mean(score))
p <- ggplot(df, aes(x=reorder(df$forum, -df$avg), y=df$avg)) + geom_bar(stat="identity") +
  labs(x = "Fora", y = "Average Score") +
  theme(text = element_text(size=30), axis.text.x=element_text(angle=90,hjust=1))
png("ave-score-bar-graph.png", units="in", width=12, height=9, res=300)
print(p)
dev.off()

## plot and save average view
df <- data.frame(views=unlist(init_viewcount_list)) %>%
  # put in to tidy format for ggplot
  mutate(forum=unlist(stri_extract_all_regex(names(unlist(init_viewcount_list)), "[A-Za-z]+"))) %>% 
  group_by(forum) %>%
  summarise(avg = mean(views))
p <- ggplot(df, aes(x=reorder(df$forum, -df$avg), y=df$avg)) + geom_bar(stat="identity") +
  labs(x = "Fora", y = "Average ViewCount") +
  theme(text = element_text(size=30), axis.text.x=element_text(angle=90,hjust=1))
png("ave-views-bar-graph.png", units="in", width=12, height=9, res=300)
print(p)
dev.off()

## plot and save cumulative view counts
df <- data.frame(views=unlist(init_viewcount_list)) %>%
  # put in to tidy format for ggplot
  mutate(forum=unlist(stri_extract_all_regex(names(unlist(init_viewcount_list)), "[A-Za-z]+")))
p <- ggplot(df, aes(df$views, group=df$forum, colour=df$forum)) +
  stat_ecdf(geom = "step") + scale_x_continuous(trans="log10", labels = comma) +
  labs(x = "ViewCount", y = "Cumulative % of Question Posts", colour="Fora")
png("cumul-viewcount.png", units="in", width=12, height=7, res=300)
print(p)
dev.off()


## plot and save thresholdplots
# binding dataframe
df <- NULL
for (k in 1:length(threshold_list)) {
  df <- rbind(df, threshold_list[[datasets[k]]])
}
df <- data.frame(perc=as.numeric(df[,1]), 
                 euclid=as.numeric(df[,2]), 
                 cosine=as.numeric(df[,3]), 
                 jaccard=as.numeric(df[,4]), 
                 forum=as.character(df[,5])
                 )
# plot distance line graph
p <- ggplot(df, aes(x=df$perc, y=df$euclid, group=df$forum, colour=df$forum)) +
  geom_line() +  labs(x = "Threshold: % Questions Labeled 'Good'", y = "Euclidean Distance", colour="Fora") + 
  geom_vline(xintercept=0.6)
png("threshold-euc.png", units="in", width=12, height=7, res=300)
print(p)
dev.off()

# plot cosine line graph
p <- ggplot(df, aes(x=df$perc, y=df$cosine, group=df$forum, colour=df$forum)) +
  geom_line() +  labs(x = "Threshold: % Questions Labeled 'Good'", y = "Cosine Similarity", colour="Fora") + 
  geom_vline(xintercept=0.6)
png("threshold-cos.png", units="in", width=12, height=7, res=300)
print(p)
dev.off()

# plot jaccard line graph
p <- ggplot(df, aes(x=df$perc, y=df$jaccard, group=df$forum, colour=df$forum)) +
  geom_line() +  labs(x = "Threshold: % Questions Labeled 'Good'", y = "Jaccard Similarity", colour="Fora") + 
  geom_vline(xintercept=0.6)
png("threshold-jac.png", units="in", width=12, height=7, res=300)
print(p)
dev.off()



################################################################
####################### SAVE RESULTS ###########################
################################################################

saveRDS(dataset_stats, "dataset_stats.rds")
saveRDS(best_worst_qs, "best_worst_qs.rds")
saveRDS(init_viewcount_list, "init_viewcount_list.rds")

## get stat sig stars from p-value columns and delete t-tests
for (i in datasets) {
  dataset_stats[[i]][,c("t.test.p","t.test.p.1")] <- NULL
  dataset_stats[[i]]$diff <- paste(dataset_stats[[i]]$Difference, 
                                   ifelse(is.na(dataset_stats[[i]]$wilcox.p)|dataset_stats[[i]]$wilcox.p>0.1, "",
                                          ifelse(dataset_stats[[i]]$wilcox.p>0.05, "*",
                                                 ifelse(dataset_stats[[i]]$wilcox.p>0.01, "**", "***"))), sep="")
  dataset_stats[[i]]$diff.1 <- paste(dataset_stats[[i]]$Difference.1, 
                                   ifelse(is.na(dataset_stats[[i]]$wilcox.p.1)|dataset_stats[[i]]$wilcox.p.1>0.1, "",
                                          ifelse(dataset_stats[[i]]$wilcox.p.1>0.05, "*",
                                                 ifelse(dataset_stats[[i]]$wilcox.p.1>0.01, "**", "***"))), sep="")
  dataset_stats[[i]][,c("Difference","Difference.1","wilcox.p","wilcox.p.1")] <- NULL 
}


stargazer(as.matrix(dataset_stats[["economics"]][,c("Metric", "Good", "Bad", "diff", "Good.1", "Bad.1", "diff.1")]))
stargazer(as.matrix(best_worst_qs[["spanish"]][1,]))









################### word predictors of quality ###################

## Body
head(textstat_keyness(dfm(sxdf_q[sxdf_q$y=="good",]$Body)))
head(textstat_keyness(dfm(sxdf_q[sxdf_q$y=="bad",]$Body)))

## Title
head(textstat_keyness(dfm(sxdf_q[sxdf_q$y=="good",]$Title)))
head(textstat_keyness(dfm(sxdf_q[sxdf_q$y=="bad",]$Title)))


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