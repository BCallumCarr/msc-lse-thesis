linguistic_descriptives <- function(dta, target=dta$y, new_target=dta$new_y, subcats='Body', reverse_levels=TRUE) {

  ### Brad Carruthers ###

  require(quanteda)
  if (reverse_levels==TRUE) {
    target <- relevel(target, levels(target)[2])
    new_target <- relevel(new_target, levels(new_target)[2])
  }

  # print out starting information
  message('Beginning linguistics analysis')
  message("First target's level is: ", levels(target)[1])
  message("Second target's level is: ", levels(target)[2])
  message("First new_target's level is: ", levels(new_target)[1])
  message("Second new_target's level is: ", levels(new_target)[2])

  # create skeleton matrix
  result <- NULL

  ##### counts #####
  one <- nrow(dta[target==levels(target)[1],])
  two <- nrow(dta[target==levels(target)[2],])
  thr <- nrow(dta[new_target==levels(new_target)[1],])
  frr <- nrow(dta[new_target==levels(new_target)[2],])
  result <- rbind(result, c('n', one, two, one-two, thr, frr, thr-frr))
  result <- rbind(result, c('n%',
                            one/nrow(dta),
                            two/nrow(dta),
                            (one-two)/nrow(dta),
                            thr/nrow(dta),
                            frr/nrow(dta),
                            (thr-frr)/nrow(dta)))

  ##### character length #####
  one <- mean(nchar(dta[target==levels(target)[1],][[subcats[1]]]))
  two <- mean(nchar(dta[target==levels(target)[2],][[subcats[1]]]))
  thr <- mean(nchar(dta[new_target==levels(new_target)[1],][[subcats[1]]]))
  frr <- mean(nchar(dta[new_target==levels(new_target)[2],][[subcats[1]]]))
  result <- rbind(result, c('character length', one, two, one-two, thr, frr, thr-frr))

  ##### token length #####
  one <- mean(ntoken(dta[target==levels(target)[1],][[subcats[1]]]))
  two <- mean(ntoken(dta[target==levels(target)[2],][[subcats[1]]]))
  thr <- mean(ntoken(dta[new_target==levels(new_target)[1],][[subcats[1]]]))
  frr <- mean(ntoken(dta[new_target==levels(new_target)[2],][[subcats[1]]]))
  result <- rbind(result, c('token length', one, two, one-two, thr, frr, thr-frr))

  ##### punctuation types #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_punct=FALSE), 'types')) -
    length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_punct=TRUE), 'types'))

  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_punct=FALSE), 'types')) -
    length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_punct=TRUE), 'types'))

  thr <- length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]], remove_punct=FALSE), 'types')) -
    length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]], remove_punct=TRUE), 'types'))

  frr <- length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]], remove_punct=FALSE), 'types')) -
    length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]], remove_punct=TRUE), 'types'))

  result <- rbind(result, c('punctuation types', one, two, one-two, thr, frr, thr-frr))

  ##### url text #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]]), 'types')) -
    length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_url=TRUE), 'types'))

  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]]), 'types')) -
    length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_url=TRUE), 'types'))

  thr <- length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]]), 'types')) -
    length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_url=TRUE), 'types'))

  frr <- length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]]), 'types')) -
    length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]], remove_url=TRUE), 'types'))

  result <- rbind(result, c('url text', one, two, one-two, thr, frr, thr-frr))

  ##### stopwords #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]]), 'types')) -
    length(attr(tokens_remove(tokens(dta[target==levels(target)[1],][[subcats[1]]]), stopwords('english')), 'types'))

  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]]), 'types')) -
    length(attr(tokens_remove(tokens(dta[target==levels(target)[2],][[subcats[1]]]), stopwords('english')), 'types'))

  one <- length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]]), 'types')) -
    length(attr(tokens_remove(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]]), stopwords('english')), 'types'))

  two <- length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]]), 'types')) -
    length(attr(tokens_remove(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]]), stopwords('english')), 'types'))

  result <- rbind(result, c('stopwords', one, two, one-two, thr, frr, thr-frr))

  ##### lexical diversity #####
  ld_df <- textstat_lexdiv(tokens(dta[[subcats[1]]]), measure=c('TTR', 'R', 'S'))[,-1]
  ld_df_means <- rbind(colMeans(ld_df[target==levels(target)[1],]),
                       colMeans(ld_df[target==levels(target)[2],]),
                       colMeans(ld_df[target==levels(target)[1],]) - colMeans(ld_df[target==levels(target)[2],]),
                       colMeans(ld_df[new_target==levels(new_target)[1],]),
                       colMeans(ld_df[new_target==levels(new_target)[2],]),
                       colMeans(ld_df[new_target==levels(new_target)[1],]) - colMeans(ld_df[new_target==levels(new_target)[2],])
                       )
  ld_df_means <- rbind(c('Type-to-Token Ratio', "Guiraud's Root TTR", "Summer's Index"), ld_df_means)
  colnames(ld_df_means) <- NULL
  result <- rbind(result, t(ld_df_means))

  ##### readability #####
  rd_df <- textstat_readability(dta[[subcats[1]]], measure=c('Flesch.Kincaid', 'FOG'))[,-1]
  rd_df_means <- rbind(colMeans(rd_df[target==levels(target)[1],]),
                       colMeans(rd_df[target==levels(target)[2],]),
                       colMeans(rd_df[target==levels(target)[1],]) - colMeans(rd_df[target==levels(target)[2],]),
                       colMeans(rd_df[new_target==levels(new_target)[1],]),
                       colMeans(rd_df[new_target==levels(new_target)[2],]),
                       colMeans(rd_df[new_target==levels(new_target)[1],]) - colMeans(rd_df[new_target==levels(new_target)[2],])
                       )
  rd_df_means <- rbind(c('Flesch-Kincaid', "Gunning's Fog Index"), rd_df_means)
  colnames(rd_df_means) <- NULL
  result <- rbind(result, t(rd_df_means))

  ##### sentiment #####
  require(quanteda.dictionaries)
  require(stringr)
  data(data_dictionary_geninqposneg)

  ## construct a dictionary object
  dict_sntmt <- dictionary(list(positive = data_dictionary_geninqposneg[['positive']],
                                negative = data_dictionary_geninqposneg[['negative']]))

  ## apply it to dfm which is normalised by stemming, removing stopwords/punctuation and weighting proportionally
  sntmt <- dfm_weight(dfm(dta[[subcats[1]]], dictionary = dict_sntmt, stem = TRUE, remove_punct = TRUE,
                          remove = stopwords('english')),
                      'prop')

  ## add it to dataframe
  dta$sntmt_score <- as.numeric(sntmt[,str_detect(colnames(sntmt), 'posit')]) -
                               as.numeric(sntmt[,str_detect(colnames(sntmt), 'negat')])

  result <- rbind(result, c('sentiment',
                            mean(dta[target==levels(target)[1],]$sntmt_score),
                            mean(dta[target==levels(target)[2],]$sntmt_score),
                            mean(dta[target==levels(target)[1],]$sntmt_score) -
                              mean(dta[target==levels(target)[2],]$sntmt_score),
                            mean(dta[new_target==levels(new_target)[1],]$sntmt_score),
                            mean(dta[new_target==levels(new_target)[2],]$sntmt_score),
                            mean(dta[new_target==levels(new_target)[1],]$sntmt_score) -
                              mean(dta[new_target==levels(new_target)[2],]$sntmt_score)
                            ))

  ##### moral values #####
  require(quanteda.dictionaries)
  require(stringr)
  data(data_dictionary_MFD)

  ## construct a dictionary object
  dict_moral <- dictionary(list(care.virtue = data_dictionary_MFD[['care.virtue']],
                                fair.virtue = data_dictionary_MFD[['fairness.virtue']],
                                loyal.virtue = data_dictionary_MFD[['loyalty.virtue']],
                                auth.virtue = data_dictionary_MFD[['authority.virtue']],
                                sanct.virtue = data_dictionary_MFD[['sanctity.virtue']],
                                care.vice = data_dictionary_MFD[['care.vice']],
                                fair.vice = data_dictionary_MFD[['fairness.vice']],
                                loyal.vice = data_dictionary_MFD[['loyalty.vice']],
                                auth.vice = data_dictionary_MFD[['authority.vice']],
                                sanct.vice = data_dictionary_MFD[['sanctity.vice']]))

  ## apply it to dfm which is normalised by stemming, removing stopwords/punctuation and weighting proportionally
  moral <- dfm_weight(dfm(dta[[subcats[1]]], dictionary = dict_moral, stem = TRUE, remove_punct = TRUE,
                          remove = stopwords('english')),
                      'prop')

  ## find lcd of columns and add to dataframe
  dta$moral_score <- rowSums(as.matrix(moral[,str_detect(colnames(moral), 'virt')])) - rowSums(as.matrix(moral[,str_detect(colnames(moral), 'vic')]))

  result <- rbind(result, c('moral values',
                            mean(dta[target==levels(target)[1],]$moral_score),
                            mean(dta[target==levels(target)[2],]$moral_score),
                            mean(dta[target==levels(target)[1],]$moral_score) -
                              mean(dta[target==levels(target)[2],]$moral_score),
                            mean(dta[new_target==levels(new_target)[1],]$moral_score),
                            mean(dta[new_target==levels(new_target)[2],]$moral_score),
                            mean(dta[new_target==levels(new_target)[1],]$moral_score) -
                              mean(dta[new_target==levels(new_target)[2],]$moral_score)
                            ))

  ##### distance #####
  ### target
  ## we normalise the dfm by stemming, removing stopwords/punctuation and weighting proportionally
  toks <- tokens(c(dta[target==levels(target)[1],][[subcats[1]]],
                   dta[target==levels(target)[2],][[subcats[1]]]))
  ## get rid of whitespace that messes up French and Linguistics
  toks <- tokens_remove(toks, "\\p{Z}", valuetype = "regex")
  tdfm <- dfm_weight(dfm(toks,
                         stem = TRUE, remove_punct = TRUE, remove = stopwords('english')),
                     'prop')

  ### new_target
  ## we normalise the dfm by stemming, removing stopwords/punctuation and weighting proportionally
  toks <- tokens(c(dta[new_target==levels(new_target)[1],][[subcats[1]]],
                   dta[new_target==levels(new_target)[2],][[subcats[1]]]))
  ## get rid of whitespace that messes up French and Linguistics
  toks <- tokens_remove(toks, "\\p{Z}", valuetype = "regex")
  ntdfm <- dfm_weight(dfm(toks,
                         stem = TRUE, remove_punct = TRUE, remove = stopwords('english')),
                     'prop')

  result <- rbind(result, c('euclidean distance',
                            NA, NA, mean(textstat_dist(tdfm, method='euclidean')),
                            NA, NA, mean(textstat_dist(ntdfm, method='euclidean'))
                            ))
  result <- rbind(result, c('cosine similarity',
                            NA, NA, mean(textstat_simil(tdfm, method='cosine')),
                            NA, NA, mean(textstat_simil(ntdfm, method='cosine'))
                            ))
  result <- rbind(result, c('jaccard similarity',
                            NA, NA, mean(textstat_simil(tdfm, method='jaccard')),
                            NA, NA, mean(textstat_simil(ntdfm, method='jaccard'))
                            ))


  ## name columns and collect results
  tib <- tibble(as.character(result[,1]),
                round(as.numeric(result[,2]), 3),
                round(as.numeric(result[,3]), 3),
                round(as.numeric(result[,4]), 3),
                round(as.numeric(result[,5]), 3),
                round(as.numeric(result[,6]), 3),
                round(as.numeric(result[,7]), 3))
  colnames(tib) <- c('metric',
                     levels(target)[1], levels(target)[2], 'difference',
                     levels(new_target)[1], levels(new_target)[2], 'difference')
  return(tib)
}
