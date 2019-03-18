setwd('/Users/brad/Downloads/beer.stackexchange.com')
list.files()
require(XML)

temp <- xmlParse("PostHistory.xml")
posth <- xmlToList(temp)

temp <- xmlParse("Posts.xml")
posts <- xmlToList(temp)

head(posts, 1)





