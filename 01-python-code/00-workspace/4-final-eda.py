#########################
########## EDA ##########
#########################

## choose variables to describe
desc_array = ['viewcount', 'score', 'viewcount_log', 'score_shift_log']

##################################
########## Descriptives ##########
##################################

## correlations between score and viewcount

print('\n\033[1mCorrelations between score and viewcount\033[0m\n')
for i in data_array:
    s = i + ' & ' + str(round( datasets[i].stat.corr("score", "viewcount"), 2 )) + ' \\\\'
    print(s)

## descriptive statistic tables

for k in desc_array:
    print(f'\n\033[1m{k.title()}\033[0m descriptives\n')
    # get header
    desc = datasets[data_array[0]].describe(k).select('summary').toPandas().T

    # loop through for descriptives
    for i in data_array:
        desc = desc.append(datasets[i].describe(k).select(k).toPandas().T, ignore_index=True)

    # set column labels equal to first row
    desc.columns = desc.iloc[0]

    # drop first row and reindex
    desc = desc.reindex(desc.index.drop(0))

    # convert dataframe to numeric
    desc = desc.apply(pd.to_numeric)

    # round dataframe
    if (k=='viewcount'):
        desc = desc.round(0)

    else:
        desc = desc.round(1)

    # assign fora names as index
    desc.index = data_array

    # print to latex
    print(desc.to_latex())

#########################################################################

'''## largest variable values across fora  
print('\n\033[1m finding highest viewed questions \033[0m\n')
for i in data_array:
    for k in desc_array:
        print("----- " + i + " -----")
        print(datasets[i].where(
            datasets[i][k] == datasets[i].select(k).
            rdd.flatMap(lambda x: x).max()).collect())'''


###########################
########## Plots ##########
###########################

# import plotting libraries
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# choose graph font size
font_size = 14

# choose graph fig size
fig_size = (14, 7)

#########################################################################
### Bar plot post counts descending order
#########################################################################

# re-establish empty dictionary of plotting data skeleton
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
plt.savefig('01-eda/01-graphs/post-counts-bar-graph.png', bbox_inches="tight")
plt.close('all')

#########################################################################
### Bar plot score descending order
#########################################################################

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].groupBy().avg('score').collect()[0][0]

# plot
import operator
plot_list = sorted(plot_data.items(), key=operator.itemgetter(1), reverse=True)
x, y = zip(*plot_list) # unpack a list of pairs into two tuples
plt.bar(x, y, align='center', alpha=.8)
plt.xticks(range(len(plot_list)), list([i[0] for i in plot_list]), rotation=90)
plt.title('Average Score per post')
plt.savefig('01-eda/01-graphs/ave-score-bar-graph.png', bbox_inches="tight")
plt.close('all')

#########################################################################
### Bar plot viewcount descending order
#########################################################################

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

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
plt.savefig('01-eda/01-graphs/ave-viewcount-bar-graph.png', bbox_inches="tight")
plt.close('all')


#########################################################################
### Bar plot y_ravi descending order
#########################################################################

# re-establish empty dictionary of plotting data skeleton
'''plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].groupBy().avg('y_ravi').collect()[0][0]

# plot
import operator
plot_list = sorted(plot_data.items(), key=operator.itemgetter(1), reverse=True)
x, y = zip(*plot_list) # unpack a list of pairs into two tuples
plt.bar(x, y, align='center', alpha=.8)
plt.xticks(range(len(plot_list)), list([i[0] for i in plot_list]), rotation=90)
plt.title('Average Score/ViewCount per post')
plt.savefig('01-eda/01-graphs/ave-y_ravi-bar-graph.png', bbox_inches="tight")
plt.close('all')'''


#########################################################################
### Violin plots
#########################################################################

matplotlib.rcParams.update({'font.size': font_size})

for k in desc_array:
    print(f'\033[1m{k.title()}\033[0m violin plot\n')
    
    # collect data
    plot_data = pd.DataFrame()
    for i in data_array:
        temp = datasets[i].select(k).toPandas()
        temp['dataset'] = i
        plot_data = plot_data.append(temp)

    # plot
    fig, ax = plt.subplots(figsize=fig_size)
    sns.violinplot( y=plot_data['dataset'], x=plot_data[k], color="darkorange" )

    # axis labels
    # get nice log(Var) x-axis label
    if (k == 'viewcount_log'):
        ax.set_xlabel('log(ViewCount)')
    elif (k == 'score_shift_log'):
        ax.set_xlabel('log(Score)')
    else:
        ax.set_xlabel(k.title())
    ax.set_ylabel('')

    # set y-axis to log
    #ax.set_yscale('log')

    # save figure
    plt.savefig(f'01-eda/01-graphs/{k}-violin-plot.png', bbox_inches="tight")
    plt.close('all')

#########################################################################
### Boxplots
#########################################################################

matplotlib.rcParams.update({'font.size': font_size})

for k in desc_array:
    print(f'\033[1m{k.title()}\033[0m boxplot plot\n')
    
    # collect data
    plot_data = pd.DataFrame()
    for i in data_array:
        temp = datasets[i].select(k).toPandas()
        temp['dataset'] = i
        plot_data = plot_data.append(temp)

    # log of variable
    #plot_data[k] = np.log(plot_data[k])
    
    # plot
    fig, ax = plt.subplots(figsize=fig_size)
    sns.boxplot( y=plot_data['dataset'], x=plot_data[k], color="darkorange" )

    # axis labels
    # get nice log(Var) x-axis label
    if (k == 'viewcount_log'):
        ax.set_xlabel('log(ViewCount)')
    elif (k == 'score_shift_log'):
        ax.set_xlabel('log(Score)')
    else:
        ax.set_xlabel(k.title())
    ax.set_ylabel('')

    # set y-axis to log
    #ax.set_yscale('log')
    
    # save figure
    plt.savefig(f'01-eda/01-graphs/{k}-box-plot.png', bbox_inches="tight")
    plt.close('all')

#########################################################################
### Plot cumulative score distribution
#########################################################################

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('score').rdd.flatMap(lambda x: x).collect()
    #plot_data[i] = [x for x in plot_data[i] if x is not None] don't need this just yet

# set colour palette
seq_col_brew = sns.color_palette("YlOrRd_r", 8)
sns.set_palette(seq_col_brew)

# plot
n_bins = 500000
fig, ax = plt.subplots(figsize=fig_size)
for i in data_array:
    n, bins, patches = ax.hist(plot_data[i], n_bins, density=True, histtype='step',
                               cumulative=True, label=i)
ax.grid(True)
ax.legend(loc='right')
ax.set_title('Cumulative Score')
ax.set_xlabel('Score')
ax.set_ylabel('Cumulative percentage of question posts')
plt.savefig('01-eda/01-graphs/cumul-score.png', bbox_inches="tight")
plt.close('all')

#########################################################################
### Single density plot viewcount
#########################################################################

matplotlib.rcParams.update({'font.size': font_size})

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('viewcount').rdd.flatMap(lambda x: x).collect() 

# set colour palette
seq_col_brew = sns.color_palette("YlOrRd_r", 8)
sns.set_palette(seq_col_brew)

# plot
fig, ax = plt.subplots(figsize=fig_size)
for i in data_array:
    sns.kdeplot(plot_data[i], label=i, shade=True)

# set x-axis to log
ax.set_xscale('log')

# set grids to true
ax.grid(True)

# axis labels
ax.set_xlabel('ViewCount')
ax.set_ylabel('Density')

# save figure
plt.savefig('01-eda/01-graphs/viewcount-sgl-density-plot.png', bbox_inches="tight")
plt.close('all')

#########################################################################
### Single density plot viewcount_log
#########################################################################

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('viewcount_log').rdd.flatMap(lambda x: x).collect() 

# set colour palette
seq_col_brew = sns.color_palette("YlOrRd_r", 8)
sns.set_palette(seq_col_brew)

# plot
fig, ax = plt.subplots(figsize=fig_size)
for i in data_array:
    sns.kdeplot(plot_data[i], label=i, shade=True)

# set x-axis to log
ax.set_xscale('log')

# set grids to true
ax.grid(True)

# axis labels
ax.set_xlabel('log(ViewCount)')
ax.set_ylabel('Density')

# save figure
plt.savefig('01-eda/01-graphs/viewcount_log-sgl-density-plot.png', bbox_inches="tight")
plt.close('all')


#########################################################################
### Dual density plot viewcount
#########################################################################

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('viewcount').rdd.flatMap(lambda x: x).collect() 

# find maximum for outlier plotting
maxp = 100
for i in data_array:
    if (max(plot_data[i]) > maxp):
        maxp = max(plot_data[i])

# set colour palette
seq_col_brew = sns.color_palette("YlOrRd_r", 8)
sns.set_palette(seq_col_brew)

# plot outliers and data from: https://matplotlib.org/examples/pylab_examples/broken_axis.html
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=fig_size)

# plot the same data on both axes
for i in data_array:
    sns.kdeplot(plot_data[i], ax=ax1, label=i, shade=True)
    sns.kdeplot(plot_data[i], ax=ax2, shade=True)

# these zoom-in limits are for SMALL datasets
ax1.set_xlim(0, 400000)  
ax2.set_xlim(5400000, maxp-10) # outliers only

# set x-axis to log
#ax1.set_xscale('log')
#ax2.set_xscale('log')

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
plt.savefig('01-eda/01-graphs/viewcount-dbl-density-plot.png', bbox_inches="tight")
plt.close('all')


#########################################################################
### Single density plot score
#########################################################################

matplotlib.rcParams.update({'font.size': font_size})

from pyspark.sql.functions import lit, expr

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('score').rdd.flatMap(lambda x: x).collect() 

# set colour palette
seq_col_brew = sns.color_palette("YlOrRd_r", 8)
sns.set_palette(seq_col_brew)

# plot
fig, ax = plt.subplots(figsize=fig_size)
for i in data_array:
    sns.kdeplot(plot_data[i], label=i, shade=True)

# set grids to true
ax.grid(True)

# set x-axis to log
ax.set_xscale('log')

# axis labels
ax.set_xlabel('Score')
ax.set_ylabel('Density')

# save figure
plt.savefig('01-eda/01-graphs/score-sgl-density-plot.png', bbox_inches="tight")
plt.close('all')

#########################################################################
### Single density plot score_shift_log
#########################################################################

from pyspark.sql.functions import lit, expr

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('score_shift_log').rdd.flatMap(lambda x: x).collect() 

# set colour palette
seq_col_brew = sns.color_palette("YlOrRd_r", 8)
sns.set_palette(seq_col_brew)

# plot
fig, ax = plt.subplots(figsize=fig_size)
for i in data_array:
    sns.kdeplot(plot_data[i], label=i, shade=True)

# set grids to true
ax.grid(True)

# set x-axis to log
#ax.set_xscale('log')

# axis labels
ax.set_xlabel('log(Score)')
ax.set_ylabel('Density')

# save figure
plt.savefig('01-eda/01-graphs/score_shift_log-sgl-density-plot.png', bbox_inches="tight")
plt.close('all')


#########################################################################
### Double density plot for score
#########################################################################

# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select('score').rdd.flatMap(lambda x: x).collect() 

# find minimum and maximum for outlier plotting
minp = 100
for i in data_array:
    if (min(plot_data[i]) < minp):
        minp = min(plot_data[i])

maxp = 100
for i in data_array:
    if (max(plot_data[i]) > maxp):
        maxp = max(plot_data[i])

# set colour palette
seq_col_brew = sns.color_palette("YlOrRd_r", 8)
sns.set_palette(seq_col_brew)

# plot outliers and data from: https://matplotlib.org/examples/pylab_examples/broken_axis.html
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=fig_size)

# plot the same data on both axes
for i in data_array:
    sns.kdeplot(plot_data[i], ax=ax1, label=i, shade=True)
    sns.kdeplot(plot_data[i], ax=ax2, shade=True)

# these zoom-in limits are for SMALL datasets
ax1.set_xlim(minp-10, 500)  
ax2.set_xlim(4000, maxp+10) # outliers only

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
plt.savefig('01-eda/01-graphs/score-dbl-density-plot.png', bbox_inches="tight")
plt.close('all')

#########################################################################
### Density plot for y_ravi
#########################################################################

'''# re-establish empty dictionary of plotting data skeleton
plot_data = {}

# collect data
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
plt.savefig('01-eda/01-graphs/y_ravi-density-plot.png', bbox_inches="tight")
plt.close('all')'''

#########################################################################
### Content of "best" and "worst" questions based on target
#########################################################################

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
pd.DataFrame.from_dict(best_worst_qs[data_array[0]][['title', 'viewcount', 'score', 'clean_body']])

## save results to csv
for i in data_array:
    best_worst_qs[i].to_csv(f'01-eda/best_worst_qs/bwqs{i}.csv')

## pickle best/worst results
import pickle

with open('01-eda/best_worst_qs/best_worst_qs.pickle', 'wb') as handle:
    pickle.dump(best_worst_qs, handle, protocol=pickle.HIGHEST_PROTOCOL)

## load pickle file to check
best_worst_qs = []
with (open("01-eda/best_worst_qs/best_worst_qs.pickle", "rb")) as openfile:
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