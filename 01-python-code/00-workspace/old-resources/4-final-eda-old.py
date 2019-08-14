'''## describe viewcount per fora
for i in data_array:
    print("----- " + i + " -----")
    datasets[i].describe(['viewcount']).show()

## describe y_ravi
for i in data_array:
    print("----- " + i + " -----")
    datasets[i].describe(['y_ravi']).show

## describe score
for i in data_array:
    print("----- " + i + " -----")
    datasets[i].describe(['score']).show()

## highest viewed questions across fora
print('\n\033[1m finding highest viewed questions \033[0m\n')
for i in data_array:
    print("----- " + i + " -----")
    print(datasets[i].where(
        datasets[i].viewcount == datasets[i].select('viewcount').
        rdd.flatMap(lambda x: x).max()).collect())'''

#########################################################################
##### PLOTS #####
#########################################################################

import seaborn as sns
import matplotlib.pyplot as plt
    
#########################################################################

## violin plot of score

# collect data
plot_data = pd.DataFrame()
for i in data_array:
    temp = datasets[i].select('score').toPandas()
    temp['forum'] = i.title()
    plot_data = plot_data.append(temp)

# plot
fig, ax = plt.subplots(figsize=(7, 7))
sns.violinplot( x=plot_data['forum'], y=plot_data['score'] )

# axis labels
ax.set_xlabel('Score')
ax.set_ylabel('')

# save figure
plt.savefig('01-graphs/score-violin-plot.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## violin plot of viewcount

# collect data
plot_data = pd.DataFrame()
for i in data_array:
    temp = datasets[i].select('viewcount').toPandas()
    temp['forum'] = i.title()
    plot_data = plot_data.append(temp)

# plot
fig, ax = plt.subplots(figsize=(7, 7))
sns.violinplot( x=plot_data['forum'], y=plot_data['viewcount'] )

# axis labels
ax.set_xlabel('ViewCount')
ax.set_ylabel('')

# save figure
plt.savefig('01-graphs/viewcount-violin-plot.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## bar plot of post counts in descending order

# empty dictionary of df skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].count()

# plot
import operator
plot_list = sorted(plot_data.items(), key=operator.itemgetter(1), reverse=True)
x, y = zip(*plot_list) # unpack a list of pairs into two tuples
plt.bar(x, y, align='center', alpha=.8)
plt.xticks(range(len(plot_list)), list([i[0] for i in plot_list]), rotation=90)
plt.title('Total number of questions')
plt.savefig('01-graphs/post-counts-bar-graph.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## bar plot of average score per post in descending order

# collect data
for i in data_array:
    plot_data[i] = datasets[i].groupBy().avg('score').collect()[0][0]

# plot
import operator
plot_list = sorted(plot_data.items(), key=operator.itemgetter(1), reverse=True)
x, y = zip(*plot_list) # unpack a list of pairs into two tuples
plt.bar(x, y, align='center', alpha=.8)
plt.xticks(range(len(plot_list)), list([i[0] for i in plot_list]), rotation=90)
plt.title('Average Score per question')
plt.savefig('01-graphs/ave-score-bar-graph.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## bar plot of viewcount per post in descending order

# collect data
for i in data_array:
    plot_data[i] = datasets[i].groupBy().avg('viewcount').collect()[0][0]

# plot
import operator
plot_list = sorted(plot_data.items(), key=operator.itemgetter(1), reverse=True)
x, y = zip(*plot_list) # unpack a list of pairs into two tuples
plt.bar(x, y, align='center', alpha=.8)
plt.xticks(range(len(plot_list)), list([i[0] for i in plot_list]), rotation=90)
plt.title('Average ViewCount per post')
plt.savefig('01-graphs/ave-views-bar-graph.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## bar plot of y_ravi per post in descending order

'''# collect data
for i in data_array:
    plot_data[i] = datasets[i].groupBy().avg('y_ravi').collect()[0][0]

# plot
import operator
plot_list = sorted(plot_data.items(), key=operator.itemgetter(1), reverse=True)
x, y = zip(*plot_list) # unpack a list of pairs into two tuples
plt.bar(x, y, align='center', alpha=.8)
plt.xticks(range(len(plot_list)), list([i[0] for i in plot_list]), rotation=90)
plt.title('Average Score/ViewCount per post')
plt.savefig('01-graphs/ave-y_ravi-bar-graph.png', bbox_inches="tight")
plt.close('all')'''

#########################################################################

## plot cumulative distribution of viewcount across fora

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select("viewcount").rdd.flatMap(lambda x: x).collect()
    #plot_data[i] = [x for x in plot_data[i] if x is not None] don't need this just yet

# plot
n_bins = 500000
fig, ax = plt.subplots(figsize=(20, 8))
for i in data_array:
    n, bins, patches = ax.hist(plot_data[i], n_bins, density=True, histtype='step',
                               cumulative=True, label=i)
ax.grid(True)
ax.set_xscale('log')
ax.legend(loc='right')
ax.set_title('Cumulative ViewCount')
ax.set_xlabel('ViewCount')
ax.set_ylabel('Cumulative percentage of question posts')
plt.savefig('01-graphs/cumul-views.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## plot cumulative distribution of y_ravi score across fora

# collect data
'''for i in data_array:
    plot_data[i] = datasets[i].select("y_ravi").rdd.flatMap(lambda x: x).collect()
    #plot_data[i] = [x for x in plot_data[i] if x is not None] don't need this just yet

# plot
n_bins = 500000
fig, ax = plt.subplots(figsize=(20, 8))
for i in data_array:
    n, bins, patches = ax.hist(plot_data[i], n_bins, density=True, histtype='step',
                               cumulative=True, label=i)
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Cumulative Score/ViewCount')
ax.set_xlabel('Score/ViewCount')
ax.set_ylabel('Cumulative percentage of question posts')
plt.savefig('01-graphs/cumul-y_ravi.png', bbox_inches="tight")
plt.close('all')'''

#########################################################################

## plot cumulative distribution of score across fora

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('score').rdd.flatMap(lambda x: x).collect()
    #plot_data[i] = [x for x in plot_data[i] if x is not None] don't need this just yet

# plot
n_bins = 500000
fig, ax = plt.subplots(figsize=(20, 8))
for i in data_array:
    n, bins, patches = ax.hist(plot_data[i], n_bins, density=True, histtype='step',
                               cumulative=True, label=i)
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Cumulative Score')
ax.set_xlabel('Score')
ax.set_ylabel('Cumulative percentage of question posts')
plt.savefig('01-graphs/cumul-score.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## density plot for score

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('score').rdd.flatMap(lambda x: x).collect() 

# plot outliers and data from: https://matplotlib.org/examples/pylab_examples/broken_axis.html
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(20, 8))

# plot the same data on both axes
for i in data_array:
    sns.kdeplot(plot_data[i], ax=ax1, label=i)
    sns.kdeplot(plot_data[i], ax=ax2)

# these zoom-in limits are for SMALL datasets
ax1.set_xlim(-20, 40)  
ax2.set_xlim(100, 275) # outliers only

# set grids to true
ax1.grid(True)
ax2.grid(True)

# hide the spines between ax and ax2
ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
#ax1.xaxis.tick_top()
ax2.tick_params(labelleft='off')  # don't put tick labels at the left
ax2.yaxis.tick_right()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)        # top-right diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # bottom-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the next axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # top-left diagonal
ax2.plot((-d, +d), (-d, +d), **kwargs)  # bottom-left diagonal

# axis labels
ax2.set_xlabel('Score')
ax1.set_ylabel('Density')

# save figure
plt.savefig('01-graphs/score-density-plot.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## density plot viewcount

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('viewcount').rdd.flatMap(lambda x: x).collect() 

# plot outliers and data from: https://matplotlib.org/examples/pylab_examples/broken_axis.html
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(20, 8))

# plot the same data on both axes
for i in data_array:
    sns.kdeplot(plot_data[i], ax=ax1, label=i)
    sns.kdeplot(plot_data[i], ax=ax2)

# these zoom-in limits are for SMALL datasets
ax1.set_xlim(0, 30000)  
ax2.set_xlim(100000, 420000) # outliers only

# set grids to true
ax1.grid(True)
ax2.grid(True)

# hide the spines between ax and ax2
ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
#ax1.xaxis.tick_top()
ax2.tick_params(labelleft='off')  # don't put tick labels at the left
ax2.yaxis.tick_right()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)        # top-right diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # bottom-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the next axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # top-left diagonal
ax2.plot((-d, +d), (-d, +d), **kwargs)  # bottom-left diagonal

# axis labels
ax2.set_xlabel('ViewCount')
ax1.set_ylabel('Density')

# save figure
plt.savefig('01-graphs/views-density-plot.png', bbox_inches="tight")
plt.close('all')

#########################################################################

## density plot y_ravi

'''# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('y_ravi').rdd.flatMap(lambda x: x).collect() 

# plot outliers and data from: https://matplotlib.org/examples/pylab_examples/broken_axis.html
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(20, 8))

# plot the same data on both axes
for i in data_array:
    sns.kdeplot(plot_data[i], ax=ax1)
    sns.kdeplot(plot_data[i], ax=ax2, label=i)
    sns.kdeplot(plot_data[i], ax=ax3)

# these zoom-in limits are for SMALL datasets
ax1.set_xlim(-0.2, -0.1)
ax2.set_xlim(-0.025, 0.125)
ax3.set_xlim(0.2, 0.35)

# set grids to true
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)

# hide the spines between ax and ax2
ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax3.spines['left'].set_visible(False)
#ax1.xaxis.tick_top()
ax2.tick_params(labelleft='off')  # don't put tick labels at the left
ax2.tick_params(labelright='off')  # don't put tick labels at the right
ax3.tick_params(labelleft='off')  # don't put tick labels at the left
#ax2.yaxis.tick_right()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
ax1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)        # top-right diagonal
ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # bottom-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the next axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # top-left diagonal
ax2.plot((-d, +d), (-d, +d), **kwargs)  # bottom-left diagonal

ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)        # top-right diagonal
ax2.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # bottom-right diagonal

kwargs.update(transform=ax3.transAxes)  # switch to the next axes
ax3.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # top-left diagonal
ax3.plot((-d, +d), (-d, +d), **kwargs)  # bottom-left diagonal

# axis labels
ax2.set_xlabel('Score/ViewCount')
ax1.set_ylabel('Density')

# save figure
plt.savefig('01-graphs/y_ravi-density-plot.png', bbox_inches="tight")
plt.close('all')'''

#########################################################################

## content of "best" and "worst" questions based on target
best_worst_qs = {}

for i in data_array:
    best_worst_qs[i] = pd.concat(
        [
            datasets[i].where(datasets[i].score == datasets[i].select('score').
                           rdd.flatMap(lambda x: x).max()).toPandas(),
            datasets[i].where(datasets[i].score == datasets[i].select('score').
                           rdd.flatMap(lambda x: x).min()).toPandas()
        ]
        , axis=0)

## look at certain fora best and worst questions
pd.DataFrame.from_dict(best_worst_qs['fitness'][['title', 'viewcount', 'score', 'clean_body']])

## save results to csv
for i in data_array:
    best_worst_qs[i].to_csv(f'best_worst_qs/bwqs{i}.csv')

## pickle best/worst results
import pickle

with open('best_worst_qs/best_worst_qs.pickle', 'wb') as handle:
    pickle.dump(best_worst_qs, handle, protocol=pickle.HIGHEST_PROTOCOL)

## load pickle file to check
best_worst_qs = []
with (open("best_worst_qs/best_worst_qs.pickle", "rb")) as openfile:
    while True:
        try:
            best_worst_qs.append(pickle.load(openfile))
        except EOFError:
            break

## loading from pickle puts it in a list, so put it back in dictionary:
best_worst_qs = best_worst_qs[0]

## get latex output
# get rid of ellips'
pd.set_option('display.max_colwidth',1000)

for i in data_array:
    print(pd.DataFrame.from_dict(best_worst_qs[i][['score', 'viewcount', 'title']]).to_latex())

#########################################################################

## get score descriptives
# get header
desc = datasets['economics'].describe('score').select('summary').toPandas().T

# loop through for descriptives
for i in data_array:
    desc = desc.append(datasets[i].describe('score').select('score').toPandas().T, ignore_index=True)

# set column labels equal to first row
desc.columns = desc.iloc[0]

# drop first row and reindex
desc = desc.reindex(desc.index.drop(0))

# convert dataframe to numeric
desc = desc.apply(pd.to_numeric)

# round dataframe
desc = desc.round(2)

# print to latex
print(desc.to_latex())

#########################################################################

## get viewcount descriptives
# get header
desc = datasets['economics'].describe('viewcount').select('summary').toPandas().T

# loop through for descriptives
for i in data_array:
    desc = desc.append(datasets[i].describe('score').select('score').toPandas().T, ignore_index=True)

# set column labels equal to first row
desc.columns = desc.iloc[0]

# drop first row and reindex
desc = desc.reindex(desc.index.drop(0))

# convert dataframe to numeric
desc = desc.apply(pd.to_numeric)

# round dataframe
desc = desc.round(2)

# print to latex
print(desc.to_latex())






    
################################################################################################
################################################################################################
################################################################################################
## code to filter viewcount:
from pyspark.sql.functions import lit
plot_data[i] = datasets[i].filter(datasets[i]['viewcount'] < lit(500)).select('score').rdd.flatMap(lambda x: x).collect() 

## code to standardise:
# convert to np.array
plot_data[i] = np.array( datasets[i].select('score').rdd.flatMap(lambda x: x).collect() )
# standardise
plot_data[i] = ( plot_data[i] - np.mean(plot_data[i]) ) / np.std(plot_data[i])