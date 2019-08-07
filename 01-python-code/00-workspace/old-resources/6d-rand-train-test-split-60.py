## create train and test dictionaries
train = {}
test = {}

############################################################
### Random split
############################################################

for i in data_array:
    train[i], test[i] = datasets[i].randomSplit([0.6, 0.4], 1234)