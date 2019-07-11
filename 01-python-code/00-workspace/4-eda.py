## find average views
for i in datasets:
    print("----- " + i + " -----")
    datasets[i].select("viewcount").describe().show() # have to use `select` here

## highest viewed questions across fora
print('\n\033[1m finding highest viewed questions \033[0m\n')
for i in data_array:
    print("----- " + i + " -----")
    print(datasets[i].where(
        datasets[i].viewcount == datasets[i].select('viewcount').
        rdd.flatMap(lambda x: x).max()).collect())

import seaborn as sns
import matplotlib.pyplot as plt
    
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
plt.title('The total number of questions')
plt.savefig('01-graphs/post-counts-bar-graph.png', bbox_inches="tight")
    
## bar plot of average score per post in descending order

# empty dictionary of df skeleton
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
plt.title('Average score per question')
plt.savefig('01-graphs/ave-score-bar-graph.png', bbox_inches="tight")

## bar plot of viewcount per post in descending order

# empty dictionary of df skeleton
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
plt.title('Average viewcount per post')
plt.savefig('01-graphs/ave-views-bar-graph.png', bbox_inches="tight")

## plot cumulative distribution of viewcount across fora

# empty dictionary of df skeleton
plot_data = {}

# collect data
for i in data_array:
    plot_data[i] = datasets[i].select("viewcount").rdd.flatMap(lambda x: x).collect()
    #plot_data[i] = [x for x in plot_data[i] if x is not None] don't need this just yet

# plot
n_bins = 500000
fig, ax = plt.subplots(figsize=(16, 8))
for i in data_array:
    n, bins, patches = ax.hist(plot_data[i], n_bins, density=True, histtype='step',
                               cumulative=True, label=i)
ax.grid(True)
ax.set_xscale('log')
ax.legend(loc='right')
ax.set_title('Cumulative step histograms')
ax.set_xlabel('ViewCount')
ax.set_ylabel('Cumulative percentage of question posts')
plt.savefig('01-graphs/cumul-viewcount.png', bbox_inches="tight")