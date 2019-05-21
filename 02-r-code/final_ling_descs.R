final_ling_descs <- function(dta, 
                             target=dta$y, 
                             new_target=dta$new_y, 
                             subcats="Body", 
                             reverse_levels=TRUE
                             ) {
  ### Brad Carruthers ###
  
  require(quanteda, quietly=TRUE)
  
  # reverse level fix
  if (reverse_levels==TRUE) {
    target <- relevel(target, levels(target)[2])
    new_target <- relevel(new_target, levels(new_target)[2])
  }
  
  # print out starting information
  message("Beginning linguistics analysis")
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
  result <- rbind(result, c("N", one, two, one-two, NA, NA, thr, frr, thr-frr, NA, NA))
  result <- rbind(result, c("N%",
                            one/nrow(dta)*100,
                            two/nrow(dta)*100,
                            (one-two)/nrow(dta)*100, NA, NA,
                            thr/nrow(dta)*100,
                            frr/nrow(dta)*100,
                            (thr-frr)/nrow(dta)*100, NA, NA))
  message("Done counts")
  
  ##### punctuation types #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_punct=FALSE), "types")) -
    length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_punct=TRUE), "types"))
  
  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_punct=FALSE), "types")) -
    length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_punct=TRUE), "types"))
  
  thr <- length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]], remove_punct=FALSE), "types")) -
    length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]], remove_punct=TRUE), "types"))
  
  frr <- length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]], remove_punct=FALSE), "types")) -
    length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]], remove_punct=TRUE), "types"))
  
  result <- rbind(result, c("Punctuation Types", one, two, one-two, NA, NA, thr, frr, thr-frr, NA, NA))
  message("Done punct types")
  
  ##### url text #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]]), "types")) -
    length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]], remove_url=TRUE), "types"))
  
  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]]), "types")) -
    length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]], remove_url=TRUE), "types"))
  
  thr <- length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]]), "types")) -
    length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]], remove_url=TRUE), "types"))
  
  frr <- length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]]), "types")) -
    length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]], remove_url=TRUE), "types"))
  
  result <- rbind(result, c("Url-Text Types", one, two, one-two, NA, NA, thr, frr, thr-frr, NA, NA))
  message("Done url text")
  
  ##### stopwords #####
  one <- length(attr(tokens(dta[target==levels(target)[1],][[subcats[1]]]), "types")) -
    length(attr(tokens_remove(tokens(dta[target==levels(target)[1],][[subcats[1]]]), stopwords("english")), "types"))
  
  two <- length(attr(tokens(dta[target==levels(target)[2],][[subcats[1]]]), "types")) -
    length(attr(tokens_remove(tokens(dta[target==levels(target)[2],][[subcats[1]]]), stopwords("english")), "types"))
  
  thr <- length(attr(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]]), "types")) -
    length(attr(tokens_remove(tokens(dta[new_target==levels(new_target)[1],][[subcats[1]]]), stopwords("english")), "types"))
  
  frr <- length(attr(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]]), "types")) -
    length(attr(tokens_remove(tokens(dta[new_target==levels(new_target)[2],][[subcats[1]]]), stopwords("english")), "types"))
  
  result <- rbind(result, c("Stopword Types", one, two, one-two, NA, NA, thr, frr, thr-frr, NA, NA))
  message("Done stopwords")
  
  ##### character length #####
  one <- nchar(dta[target==levels(target)[1],][[subcats[1]]])
  two <- nchar(dta[target==levels(target)[2],][[subcats[1]]])
  thr <- nchar(dta[new_target==levels(new_target)[1],][[subcats[1]]])
  frr <- nchar(dta[new_target==levels(new_target)[2],][[subcats[1]]])
  result <- rbind(result, c("Character Length", mean(one), mean(two), mean(one)-mean(two), 
                            wilcox.test(one, two)$p.value, t.test(one, two)$p.value,
                            mean(thr), mean(frr), mean(thr)-mean(frr), 
                            wilcox.test(thr, frr)$p.value, t.test(thr, frr)$p.value))
  message("Done char length")
  
  ##### token length #####
  one <- ntoken(dta[target==levels(target)[1],][[subcats[1]]])
  two <- ntoken(dta[target==levels(target)[2],][[subcats[1]]])
  thr <- ntoken(dta[new_target==levels(new_target)[1],][[subcats[1]]])
  frr <- ntoken(dta[new_target==levels(new_target)[2],][[subcats[1]]])
  result <- rbind(result, c("Token Length", mean(one), mean(two), mean(one)-mean(two), 
                            wilcox.test(one, two)$p.value, t.test(one, two)$p.value,
                            mean(thr), mean(frr), mean(thr)-mean(frr), 
                            wilcox.test(thr, frr)$p.value, t.test(thr, frr)$p.value))
  message("Done token length")
  
  ##### lexical diversity #####
  ld_df <- textstat_lexdiv(tokens(dta[[subcats[1]]]), measure=c("R", "K"))[,-1]
  ld_df_means <- rbind(colMeans(ld_df[target==levels(target)[1],]),
                       colMeans(ld_df[target==levels(target)[2],]),
                       colMeans(ld_df[target==levels(target)[1],]) - colMeans(ld_df[target==levels(target)[2],]),
                       c(wilcox.test(ld_df[target==levels(target)[1],]$R, ld_df[target==levels(target)[2],]$R)$p.value, 
                         wilcox.test(ld_df[target==levels(target)[1],]$K, ld_df[target==levels(target)[2],]$K)$p.value), 
                       c(t.test(ld_df[target==levels(target)[1],]$R, ld_df[target==levels(target)[2],]$R)$p.value,
                         t.test(ld_df[target==levels(target)[1],]$K, ld_df[target==levels(target)[2],]$K)$p.value),
                       colMeans(ld_df[new_target==levels(new_target)[1],]),
                       colMeans(ld_df[new_target==levels(new_target)[2],]),
                       colMeans(ld_df[new_target==levels(new_target)[1],]) - colMeans(ld_df[new_target==levels(new_target)[2],]),
                       c(wilcox.test(ld_df[new_target==levels(new_target)[1],]$R, ld_df[new_target==levels(new_target)[2],]$R)$p.value, 
                         wilcox.test(ld_df[new_target==levels(new_target)[1],]$K, ld_df[new_target==levels(new_target)[2],]$K)$p.value), 
                       c(t.test(ld_df[new_target==levels(new_target)[1],]$R, ld_df[new_target==levels(new_target)[2],]$R)$p.value,
                         t.test(ld_df[new_target==levels(new_target)[1],]$K, ld_df[new_target==levels(new_target)[2],]$K)$p.value)
                       )
  ld_df_means <- rbind(c("Guiraud's Root TTR", "Yule's K"), ld_df_means)
  colnames(ld_df_means) <- NULL
  result <- rbind(result, t(ld_df_means))
  message("Done lex div'y")
  
  ##### readability #####
  rd_df <- textstat_readability(dta[[subcats[1]]], measure=c("Flesch.Kincaid", "FOG"))[,-1]
  rd_df_means <- rbind(colMeans(rd_df[target==levels(target)[1],]),
                       colMeans(rd_df[target==levels(target)[2],]),
                       colMeans(rd_df[target==levels(target)[1],]) - colMeans(rd_df[target==levels(target)[2],]),
              c(wilcox.test(rd_df[target==levels(target)[1],]$Flesch.Kincaid, rd_df[target==levels(target)[2],]$Flesch.Kincaid)$p.value, 
                wilcox.test(rd_df[target==levels(target)[1],]$FOG, rd_df[target==levels(target)[2],]$FOG)$p.value), 
              c(t.test(rd_df[target==levels(target)[1],]$Flesch.Kincaid, rd_df[target==levels(target)[2],]$Flesch.Kincaid)$p.value,
                t.test(rd_df[target==levels(target)[1],]$FOG, rd_df[target==levels(target)[2],]$FOG)$p.value),
                       colMeans(rd_df[new_target==levels(new_target)[1],]),
                       colMeans(rd_df[new_target==levels(new_target)[2],]),
                       colMeans(rd_df[new_target==levels(new_target)[1],]) - colMeans(rd_df[new_target==levels(new_target)[2],]),
c(wilcox.test(rd_df[new_target==levels(new_target)[1],]$Flesch.Kincaid, rd_df[new_target==levels(new_target)[2],]$Flesch.Kincaid)$p.value,
  wilcox.test(rd_df[new_target==levels(new_target)[1],]$FOG, rd_df[new_target==levels(new_target)[2],]$FOG)$p.value), 
c(t.test(rd_df[new_target==levels(new_target)[1],]$Flesch.Kincaid, rd_df[new_target==levels(new_target)[2],]$Flesch.Kincaid)$p.value,
  t.test(rd_df[new_target==levels(new_target)[1],]$FOG, rd_df[new_target==levels(new_target)[2],]$FOG)$p.value)
                       )
  rd_df_means <- rbind(c("Flesch-Kincaid", "Gunning's Fog Index"), rd_df_means)
  colnames(rd_df_means) <- NULL
  result <- rbind(result, t(rd_df_means))
  message("Done readability")
  
  ##### sentiment #####
  require(quanteda.dictionaries, quietly=TRUE)
  require(stringr, quietly=TRUE)
  data(data_dictionary_geninqposneg)
  
  ## construct a dictionary object
  dict_sntmt <- dictionary(list(positive = data_dictionary_geninqposneg[["positive"]],
                                negative = data_dictionary_geninqposneg[["negative"]]))
  
  ## apply it to dfm which is normalised by stemming, removing stopwords/punctuation and weighting proportionally
  sntmt <- dfm_weight(dfm(dta[[subcats[1]]], dictionary = dict_sntmt, stem = TRUE, remove_punct = TRUE,
                          remove = stopwords("english")),
                      "prop")
    ## add it to dataframe
  dta$sntmt_score <- as.numeric(sntmt[,str_detect(colnames(sntmt), "posit")]) -
    as.numeric(sntmt[,str_detect(colnames(sntmt), "negat")])
  
  result <- rbind(result, c("Sentiment",
                            mean(dta[target==levels(target)[1],]$sntmt_score),
                            mean(dta[target==levels(target)[2],]$sntmt_score),
                            mean(dta[target==levels(target)[1],]$sntmt_score) -
                              mean(dta[target==levels(target)[2],]$sntmt_score),
                            wilcox.test(dta[target==levels(target)[1],]$sntmt_score, 
                                        dta[target==levels(target)[2],]$sntmt_score)$p.value,
                            t.test(dta[target==levels(target)[1],]$sntmt_score, 
                                   dta[target==levels(target)[2],]$sntmt_score)$p.value,
                            mean(dta[new_target==levels(new_target)[1],]$sntmt_score),
                            mean(dta[new_target==levels(new_target)[2],]$sntmt_score),
                            mean(dta[new_target==levels(new_target)[1],]$sntmt_score) -
                              mean(dta[new_target==levels(new_target)[2],]$sntmt_score),
                            wilcox.test(dta[new_target==levels(new_target)[1],]$sntmt_score, 
                                        dta[new_target==levels(new_target)[2],]$sntmt_score)$p.value,
                            t.test(dta[new_target==levels(new_target)[1],]$sntmt_score, 
                                   dta[new_target==levels(new_target)[2],]$sntmt_score)$p.value
                            ))
  message("Done sentiment")
  
  
  ##### moral values #####
  require(quanteda.dictionaries, quietly=TRUE)
  require(stringr, quietly=TRUE, warn.conflicts = )
  data(data_dictionary_MFD)
  
  ## construct a dictionary object
  dict_moral <- dictionary(list(care.virtue = data_dictionary_MFD[["care.virtue"]],
                                fair.virtue = data_dictionary_MFD[["fairness.virtue"]],
                                loyal.virtue = data_dictionary_MFD[["loyalty.virtue"]],
                                auth.virtue = data_dictionary_MFD[["authority.virtue"]],
                                sanct.virtue = data_dictionary_MFD[["sanctity.virtue"]],
                                care.vice = data_dictionary_MFD[["care.vice"]],
                                fair.vice = data_dictionary_MFD[["fairness.vice"]],
                                loyal.vice = data_dictionary_MFD[["loyalty.vice"]],
                                auth.vice = data_dictionary_MFD[["authority.vice"]],
                                sanct.vice = data_dictionary_MFD[["sanctity.vice"]]))
  
  ## apply it to dfm which is normalised by stemming, removing stopwords/punctuation and weighting proportionally
  moral <- dfm_weight(dfm(dta[[subcats[1]]], dictionary = dict_moral, stem = TRUE, remove_punct = TRUE,
                          remove = stopwords("english")),
                      "prop")
  
  ## find lcd of columns and add to dataframe
  dta$moral_score <- rowSums(as.matrix(moral[,str_detect(colnames(moral), "virt")])) - rowSums(as.matrix(moral[,str_detect(colnames(moral), "vic")]))
  
  result <- rbind(result, c("Moral Values",
                            mean(dta[target==levels(target)[1],]$moral_score),
                            mean(dta[target==levels(target)[2],]$moral_score),
                            mean(dta[target==levels(target)[1],]$moral_score) -
                              mean(dta[target==levels(target)[2],]$moral_score),
                            wilcox.test(dta[target==levels(target)[1],]$moral_score, 
                                        dta[target==levels(target)[2],]$moral_score)$p.value,
                            t.test(dta[target==levels(target)[1],]$moral_score, 
                                   dta[target==levels(target)[2],]$moral_score)$p.value,
                            mean(dta[new_target==levels(new_target)[1],]$moral_score),
                            mean(dta[new_target==levels(new_target)[2],]$moral_score),
                            mean(dta[new_target==levels(new_target)[1],]$moral_score) -
                              mean(dta[new_target==levels(new_target)[2],]$moral_score),
                            wilcox.test(dta[new_target==levels(new_target)[1],]$moral_score, 
                                        dta[new_target==levels(new_target)[2],]$moral_score)$p.value,
                            t.test(dta[new_target==levels(new_target)[1],]$moral_score, 
                                   dta[new_target==levels(new_target)[2],]$moral_score)$p.value
                            ))
  message("Done moral values")
  
  ##### name columns and collect results #####
  tib <- tibble(as.character(result[,1]),
                round(as.numeric(result[,2]), 2),
                round(as.numeric(result[,3]), 2),
                round(as.numeric(result[,4]), 2),
                round(as.numeric(result[,5]), 3),
                round(as.numeric(result[,6]), 3),
                round(as.numeric(result[,7]), 2),
                round(as.numeric(result[,8]), 2),
                round(as.numeric(result[,9]), 2),
                round(as.numeric(result[,10]), 2),
                round(as.numeric(result[,11]), 2)
                )
  
  simple_cap <- function(x) {
    s <- strsplit(x, " ")[[1]]
    paste(toupper(substring(s, 1, 1)), substring(s, 2),
          sep = "", collapse = " ")
  }
  
  colnames(tib) <- c("Metric",
                     simple_cap(levels(target)[1]), simple_cap(levels(target)[2]), "Difference", "wilcox.p", "t.p",
                     simple_cap(levels(new_target)[1]), simple_cap(levels(new_target)[2]), "Difference", "wilcox.p", "t.p")
  return(tib)
  
}
