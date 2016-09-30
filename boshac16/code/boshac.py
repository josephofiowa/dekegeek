# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 18:25:22 2016

@author: JosephNelson
"""
import pandas as pd

# loading data
blocks = pd.read_csv('./assets/data/20152016_02_total_blocks.csv')
cf = pd.read_csv('./assets/data/20152016_02_total_cf.csv')
faceoffs = pd.read_csv('./assets/data/20152016_02_total_faceoff.csv')
giveaways = pd.read_csv('./assets/data/20152016_02_total_giveaways.csv')
goals = pd.read_csv('./assets/data/20152016_02_total_goals.csv')
hits = pd.read_csv('./assets/data/20152016_02_total_hits.csv')
miss = pd.read_csv('./assets/data/20152016_02_total_miss.csv')
pen_type = pd.read_csv('./assets/data/20152016_02_total_pen_type.csv')
pen = pd.read_csv('./assets/data/20152016_02_total_pen.csv')
shots = pd.read_csv('./assets/data/20152016_02_total_shot.csv')
takeaways = pd.read_csv('./assets/data/20152016_02_total_take.csv')
toi = pd.read_csv('./assets/data/20152016_02_total_gp_toi.csv')

# EDA - check shapes
all_dfs = [blocks, cf, faceoffs, giveaways, goals, hits, miss, pen_type, pen, shots, takeaways, toi]
for x in all_dfs:
    print x.shape

# check columns of relevant dfs
dfs = [blocks, cf, giveaways, goals, hits, shots, takeaways]
for x in dfs:
    print x.columns

# select relevant columns
blocks = blocks[['comb','blocks','5v5_block','g_block_5_5v5','b_block_5_5v5',
                 'g_block_10_5v5','b_block_10_5v5','g_block_5_ev',
                 'b_block_5_ev','g_block_10_ev','b_block_10_ev',
                 'g_block_5_pp','b_block_5_pp','g_block_10_pp',
                 'b_block_10_pp','g_block_5_sh','b_block_5_sh',
                 'g_block_10_sh','b_block_10_sh']]

hits = hits[['comb','hits','5v5_hits','g_hit_5_5v5','b_hit_5_5v5',
             'g_hit_10_5v5','b_hit_10_5v5','g_hit_5_ev','b_hit_5_ev',
             'g_hit_10_ev','b_hit_10_ev','g_hit_5_pp','b_hit_5_pp',
             'g_hit_10_pp','b_hit_10_pp','g_hit_5_sh','b_hit_5_sh',
             'g_hit_10_sh','b_hit_10_sh']]

cf = cf[['comb','corsi_for_5v5','corsi_against_5v5','corsi_5v5','corsi_for',
         'corsi_against','corsi','fenwick_for_5v5','fenwick_against_5v5',
         'fenwick_5v5','fenwick_for','fenwick_against','fenwick']]

giveaways = giveaways[['comb', 'giveaways', '5v5_give', 'ev_give']]

goals = goals[['comb', 'goals', 'assists', '5v5_goal', 'ev_goal']]

shots = shots[['comb', 'shots', '5v5_shot', 'ev_shot']]

takeaways = takeaways[['comb','takeaways', '5v5_take', 'ev_take']]

# combine into a single dataset
data = toi.merge(cf,on='comb',how='outer')
data = data.merge(blocks, on='comb', how='outer')
data = data.merge(hits, on='comb', how='outer')
data = data.merge(giveaways, on='comb', how='outer')
data = data.merge(goals, on='comb', how='outer')
data = data.merge(shots, on='comb', how='outer')
data = data.merge(takeaways, on='comb', how='outer')

# check it
data.shape

# save dat ish
data.to_csv('./assets/data/20152016_02_merged.csv',index=False)


# raw inquisitivity
import seaborn as sns

sns.pairplot(data, x_vars=['giveaways', 'takeaways'], y_vars='hits')
sns.pairplot(data, x_vars=['giveaways', 'takeaways', 'hits', 'blocks'], y_vars='corsi')

# at this stage, our stats are not scaled per 60 mins
# I'll build a df that has our relevant /60 stats

# but first, get the appropriate TOI
def convert_to_60(time):
    mins = int(time.split(':')[0])
    secs = int(time.split(':')[1])
    secs = secs/60.0
    converted_mins = mins + secs
    return converted_mins/60.0
    
# remove goalies
data = data.ix[data.pos != 'G']

# Convert our TOI columns to number of 60 minutes intervals
data.ix[:,'TOI'] = data['TOI'].apply(convert_to_60)
data.ix[:,'TOI_5v5'] = data['TOI_5v5'].apply(convert_to_60)

# Create a new DataFrame for our stats per 60 mins of TOI
stats_60 = pd.DataFrame()

# Copy over the player information and their TOI info
for col in ['last','first','pos','num','GP','TOI','TOI_5v5']:
    stats_60[col] = data[col]

# grab new cols
stat_5v5_cols = ['corsi_for_5v5','corsi_against_5v5','corsi_5v5',
                 'fenwick_for_5v5','fenwick_against_5v5','fenwick_5v5',
                 '5v5_block','g_block_5_5v5','b_block_5_5v5','g_block_10_5v5',
                 'b_block_10_5v5','g_block_5_ev','5v5_hits','g_hit_5_5v5',
                 'b_hit_5_5v5','g_hit_10_5v5','b_hit_10_5v5', '5v5_goal',
                 '5v5_shot', '5v5_give', '5v5_take']

# Need to use TOI to produce all 5v5 stats relative to their /60min of play
for col in stat_5v5_cols:
    stats_60[col+'/60'] = data[col]/stats_60['TOI_5v5']

# save the /60 dataset by itself
stats_60.to_csv('./assets/data/20152016_02_stats60.csv')

# filter to only 20 games played individuals
stats_60.GP
stats_60[stats_60.GP >= 20].head()
stats_60[stats_60.GP >= 20].shape          # 898 players

# only defensemen
stats_60[(stats_60.GP >= 20) & (stats_60.pos == 'D')].shape
dmen = stats_60[(stats_60.GP >= 20) & (stats_60.pos == 'D')] # new df

dmen.head()
dmen['b_hit_shot_5_5v5/60']= dmen['b_hit_5_5v5/60'] + dmen['b_block_5_5v5/60']

# scale this data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(dmen['b_hit_shot_5_5v5/60'])
bad_scaled = scaler.transform(dmen['b_hit_shot_5_5v5/60'])

dmen['5v5_give/60']
scaler.fit(dmen['5v5_give/60'])
give_scaled = scaler.transform(dmen['5v5_give/60'])

import matplotlib.pyplot as plt
# display plots in the notebook
%matplotlib inline

# increase default figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

# plot this
plt.scatter(bad_scaled, give_scaled)

# put back into the df to plot with Tableau
dmen.ix[:,'b_hit_shot_5_5v5/60_scaled'] = bad_scaled
dmen.ix[:,'5v5_give/60_scaled'] = give_scaled

# export
dmen.to_csv('./assets/data/20152016_02_stats60_dmen.csv')

#  compute recovery: the number of times a player 
data['recovery'] = ((data['b_block_5_5v5']+data['b_hit_5_5v5'])/data['5v5_give'])
data.recovery.plot(kind='hist', bins=30)

# top recovery leaders
data[(data.pos == 'D') & (data.GP >= 60)].sort('recovery', ascending=False).head(15)

# check for more b bl or b hit within giveaways

# reset index on data
data.reset_index(inplace=True, drop=True)

# check for cases where there are more bad blocked shots than giveaways
for i in data.ix[:,'b_hit_5_5v5']:
    if i > data.ix[i,'5v5_give']:
        print i
data['5v5_give'][1]

    
# EDA
sns.distplot(dmen['b_block_5_5v5/60'])
sns.distplot(dmen['5v5_give/60'])


# pairplots
sns.lmplot(x='b_block_5_5v5/60', y='corsi_5v5/60', data=dmen, aspect=1.5, scatter_kws={'alpha':0.2})

# linreg with sklearn
from sklearn.linear_model import LinearRegression

# tts
from sklearn.cross_validation import train_test_split
import numpy as np
def linreg(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    y_pred = linreg.predict(X_test)
    
    plt.scatter(X_test, y_test,  color='black')
    plt.plot(X_test, linreg.predict(X_test), color='blue',
             linewidth=3)
    print("Coefficients: ", linreg.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"%np.mean((linreg.predict(X_test) - y_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('R-squared score: %.2f' % linreg.score(X_test, y_test))
    
# baseline
X = dmen[['5v5_hits/60']]
y = dmen['fenwick_5v5/60']
linreg(X,y)

# try polyfit on fenwick
degree=5
X = dmen['5v5_hits/60']                     # fit on array
poly = np.polyfit(X.tolist(),y,deg=degree)
p = np.poly1d(poly)

# plot
xp = np.linspace(-2, 20, 100)
plt.plot(X, y, '.', xp, p(xp), '-', xp, p(xp), '--')
plt.xlabel('5v5 Hits per 60')
plt.ylabel('Fenwick 5v5')
plt.title("Defenseman's Paradox")
plt.savefig('./assets/images/Hits_vs_Fenwick.png')

# dropping Mark Borowiecki (outlier) and double checking
dmen[dmen['5v5_hits/60']>18]
X = dmen[dmen['5v5_hits/60']<18]['5v5_hits/60']
y = dmen[dmen['5v5_hits/60']<18]['fenwick_5v5/60']

poly = np.polyfit(X.tolist(),y,deg=degree)
p = np.poly1d(poly)
# plot
xp = np.linspace(-2, 20, 100)
plt.plot(X, y, '.', xp, p(xp), '-', xp, p(xp), '--')
plt.xlim(min(X), max(X))


# baseline for blocks
X = dmen['5v5_block/60']
y = dmen['fenwick_5v5/60']
poly = np.polyfit(X.tolist(),y,deg=3)
p = np.poly1d(poly)

# plot
xp = np.linspace(-2, 20, 100)
plt.plot(X, y, '.', xp, p(xp), '-', xp, p(xp), '--')
plt.xlabel('5v5 Blocked Shots per 60')
plt.ylabel('Fenwick 5v5')
plt.title("Defenseman's Paradox")
plt.xlim(min(X), max(X))
plt.ylim(min(y), max(y))
plt.savefig('./assets/images/Blocks_vs_Fenwick.png')

# bad blocked shots
X = dmen[['b_block_5_5v5/60']]
y = dmen['corsi_5v5/60']
linreg(X,y)

# polyfit
degree=2
X = dmen['b_block_5_5v5/60']                     # fit on array
y = dmen['fenwick_5v5/60']
poly = np.polyfit(X.tolist(),y,deg=degree)
p = np.poly1d(poly)

# plot
xp = np.linspace(-2, 20, 100)
plt.plot(X, y, '.', xp, p(xp), '-', xp, p(xp), '--')
plt.xlim(-.1, .35)
plt.ylim(min(y-1), max(y+1))


# good blocked shots only in presence of giveaway
X = dmen[['b_block_5_5v5/60']]
y = dmen['5v5_give/60']
linreg(X,y)


# statsmodels
import statsmodels.api as sm

X = dmen[['5v5_hits/60']]*dmen[['5v5_hits/60']]
y = dmen['corsi_5v5/60']

results = sm.OLS(y,sm.add_constant(X)).fit()

print results.summary()

brian = pd.read_csv('final_20152016.csv')

# scale this data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(brian['b_bh_5_5v5/60'])
bad_scaled = scaler.transform(brian['b_bh_5_5v5/60'])


scaler.fit(brian['5v5_give/60'])
give_scaled = scaler.transform(brian['5v5_give/60'])

brian['b_bh_5_5v5/60_scaled'] = bad_scaled
brian['5v5_give/60'] = give_scaled
brian.to_csv('brian.csv')