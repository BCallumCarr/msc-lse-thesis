# create timing arrary
times = []

for npart in range(25,0,-1):
    # total number of posts of dataframes
    plot_data = {}
    for i in data_array:
        posts_dfs[i] = posts_dfs[i].repartition(npart)
        print("Number of partitions: {}".format(posts_dfs[i].getNumPartitions()))
        t0 = time.time()
        plot_data[i] = posts_dfs[i].count()
        T = time.time() - t0;
        print("time: ",T)
        times = times + [T]



import pickle

## function to save objects
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

# sample usage
save_object(company1, 'company1.pkl')

## display architecture (must find workers as well)
import multiprocessing
multiprocessing.cpu_count()


## package to work with graphframes, must include in creation of cluster
spark:spark.jars.packages=graphframes:graphframes:0.5.0-spark2.1-s_2.11,



## function to save objects
import pickle
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

## save list of dataframes usage
save_object(posts_dfs, 'posts_dfs.pkl')

## load object
#filehandler = open(filename, 'r')
#object = pickle.load(filehandler)

#import pickle
#file_pi2 = open('filename_pi.obj', 'r')
#object_pi2 = pickle.load(file_pi2)

## 1D plot of expat viewcount
val = 0.
ar = plot_data['expatriates']
plt.plot(ar, np.zeros_like(ar) + val, 'x')
plt.show()

## plot multiple at once
fig, axs = plt.subplots(1,2)

df['korisnika'].plot(ax=axs[0])
df['osiguranika'].plot(ax=axs[1])

### ! Problem plotting length of questions !
plot_data = {}
for i in data_array:
    plot_data[i] = posts_dfs[i].groupBy().length('_Body').collect()[0][0]

# bar plot
import operator
plot_list = sorted(plot_data.items(), key=operator.itemgetter(1), reverse=True)
x, y = zip(*plot_list) # unpack a list of pairs into two tuples
plt.bar(x, y, align='center', alpha=.8)
plt.xticks(range(len(plot_list)), list([i[0] for i in plot_list]), rotation=90)
plt.title('Viewcount per post')
plt.show()

## average length of post across fora
posts_dfs["expatriates"].select('_Body').rdd.flatMap(lambda x: x).flatMap(lambda x: x).collect()
len(posts_dfs['expatriates'].select('_Body').take(1)[0][0])
len(posts_dfs['expatriates'].select('_Body').take(2)[1][0])
posts_dfs['expatriates'].select('_Body').take(1)[0][0]
posts_dfs['expatriates'].select('_Body').take(2)[1][0]
spark.createDataFrame([('ABC ',)], ['a']).select(length('a').alias('length')).collect()
