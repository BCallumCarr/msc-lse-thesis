linguistic_descriptives <- function(dta, target=dta$y, subcats='Body', reverse_levels=TRUE) {
  
  if (reverse_levels==TRUE) {
    target <- relevel(target, levels(target)[2])
  }
  
  # print out levels
  message('First level is:', levels(target)[1])
  message('Second level is:', levels(target)[2])
  
  # create skeleton matrix
  result <- NULL
  
  ##### character length #####
  one <- mean(nchar(dta[target==levels(target)[1],][[subcats[1]]]))
  two <- mean(nchar(dta[target==levels(target)[2],][[subcats[1]]]))
  result <- rbind(result, c('character length', one, two, one-two))
  
  ##### token length #####
  one <- mean(ntoken(dta[target==levels(target)[1],][[subcats[1]]]))
  two <- mean(ntoken(dta[target==levels(target)[2],][[subcats[1]]]))
  result <- rbind(result, c('token length', one, two, one-two))
  
  ##### punctuation types #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_punct=FALSE), 'types')) -
    length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_punct=TRUE), 'types'))
  
  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_punct=FALSE), 'types')) -
    length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_punct=TRUE), 'types'))
  
  result <- rbind(result, c('punctuation types', one, two, one-two))
  
  ##### url text #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]]), 'types')) -
    length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_url=TRUE), 'types'))
  
  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]]), 'types')) -
    length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_url=TRUE), 'types'))
  
  result <- rbind(result, c('url text', one, two, one-two))
  
  ##### stopwords #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]]), 'types')) -
    length(attr(tokens_remove(tokens(dta[target==levels(target)[1],][[subcats[1]]]), stopwords('english')), 'types'))
  
  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]]), 'types')) -
    length(attr(tokens_remove(tokens(dta[target==levels(target)[2],][[subcats[1]]]), stopwords('english')), 'types'))
  
  result <- rbind(result, c('stopwords', one, two, one-two))
  
  ##### lexical diversity #####
  ld_df <- textstat_lexdiv(tokens(dta[[subcats[1]]]), measure=c('TTR', 'R', 'S'))[,-1]
  ld_df_means <- rbind(colMeans(ld_df[target==levels(target)[1],]), 
                       colMeans(ld_df[target==levels(target)[2],]),
                       colMeans(ld_df[target==levels(target)[1],]) - colMeans(ld_df[target==levels(target)[2],]))
  ld_df_means <- rbind(c('Type-to-Token Ratio', "Guiraud's Root TTR", "Summer's Index"), ld_df_means)
  colnames(ld_df_means) <- NULL
  result <- rbind(result, t(ld_df_means))
  
  ##### readability #####
  rd_df <- textstat_readability(dta[[subcats[1]]], measure=c('Flesch.Kincaid', 'FOG'))[,-1]
  rd_df_means <- rbind(colMeans(rd_df[target==levels(target)[1],]), 
                       colMeans(rd_df[target==levels(target)[2],]),
                       colMeans(rd_df[target==levels(target)[1],]) - colMeans(rd_df[target==levels(target)[2],]))
  rd_df_means <- rbind(c('Flesch-Kincaid', "Gunning's Fog Index"), rd_df_means)
  colnames(rd_df_means) <- NULL
  result <- rbind(result, t(rd_df_means))
  
  ##### sentiment #####
  require(quanteda.dictionaries)
  data(data_dictionary_geninqposneg)
  
  ## construct a dictionary object
  dict_sntmt <- dictionary(list(positive = data_dictionary_geninqposneg[['positive']],
                                negative = data_dictionary_geninqposneg[['negative']]))
  
  ## apply it to dfm which is normalised by stemming, removing stopwords/punctuation and weighting proportionally
  sntmt <- dfm_weight(dfm(dta[[subcats[1]]], dictionary = dict_sntmt, stem = TRUE, remove_punct = TRUE,
                          remove = stopwords('english')), 
                      'prop')
  
  ## add it to dataframe
  dta$sntmt_score <- as.numeric(sntmt[,1]) - as.numeric(sntmt[,2])
  
  result <- rbind(result, c('sentiment', mean(dta[target==levels(target)[1],]$sntmt_score), 
                            mean(dta[target==levels(target)[2],]$sntmt_score),
                            mean(dta[target==levels(target)[1],]$sntmt_score) - mean(dta[target==levels(target)[2],]$sntmt_score)))
  
  ##### moral values #####
  require(quanteda.dictionaries)
  data(data_dictionary_MFD)
  
  ## construct a dictionary object
  dict_moral <- dictionary(list(care.virtue = data_dictionary_MFD[['care.virtue']],
                                fairness.virtue = data_dictionary_MFD[['fairness.virtue']],
                                loyalty.virtue = data_dictionary_MFD[['loyalty.virtue']],
                                authority.virtue = data_dictionary_MFD[['authority.virtue']],
                                sanctity.virtue = data_dictionary_MFD[['sanctity.virtue']],
                                fairness.vice = data_dictionary_MFD[['fairness.vice']],
                                loyalty.vice = data_dictionary_MFD[['loyalty.vice']],
                                care.vice = data_dictionary_MFD[['care.vice']],
                                authority.vice = data_dictionary_MFD[['authority.vice']],
                                sanctity.vice = data_dictionary_MFD[['sanctity.vice']]))
  
  ## apply it to dfm which is normalised by stemming, removing stopwords/punctuation and weighting proportionally
  moral <- dfm_weight(dfm(dta[[subcats[1]]], dictionary = dict_moral, stem = TRUE, remove_punct = TRUE,
                          remove = stopwords('english')), 
                      'prop')
  
  ## add it to dataframe
  dta$moral_score <- rowSums(as.matrix(moral[,1:5]) - as.matrix(moral[,6:10]))
  
  result <- rbind(result, c('moral values', mean(dta[target==levels(target)[1],]$moral_score), 
                            mean(dta[target==levels(target)[2],]$moral_score),
                            mean(dta[target==levels(target)[1],]$moral_score) - mean(dta[target==levels(target)[2],]$moral_score)))
  
  ##### distance #####
  
  ## we normalise the dfm by stemming, removing stopwords/punctuation and weighting proportionally
  ndfm <- dfm_weight(dfm(c(dta[target==levels(target)[1],][[subcats[1]]], 
                           dta[target==levels(target)[2],][[subcats[1]]]), 
                         stem = TRUE, remove_punct = TRUE, remove = stopwords('english')), 
                     'prop')
  
  result <- rbind(result, c('euclidean distance', NA, NA, mean(textstat_dist(ndfm, method='euclidean'))))
  result <- rbind(result, c('cosine similarity', NA, NA, mean(textstat_simil(ndfm, method='cosine'))))
  result <- rbind(result, c('jaccard similarity', NA, NA, mean(textstat_simil(ndfm, method='jaccard'))))
  
  
  ## name columns and collect results
  tib <- tibble(as.character(result[,1]), 
                round(as.numeric(result[,2]), 3), 
                round(as.numeric(result[,3]), 3),
                round(as.numeric(result[,4]), 3))
  colnames(tib) <- c('metric', levels(target)[1], levels(target)[2], 'difference')
  return(tib)
}