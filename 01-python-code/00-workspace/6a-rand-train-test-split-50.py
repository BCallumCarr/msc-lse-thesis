## create train and test dictionaries
train = {}
test = {}

############################################################
### Random split
############################################################

# 50/50
for i in data_array:
    train[i], test[i] = datasets[i].randomSplit([0.5, 0.5], 1777)