# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 18:25:22 2016

@author: JosephNelson
"""

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

# remove goalies
data = data.ix[data.pos != 'G']

# raw inquisitivity
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

# Convert our TOI columns to number of 60 minutes intervals
data['TOI'] = data['TOI'].apply(convert_to_60)
data['TOI_5v5'] = data['TOI_5v5'].apply(convert_to_60)

# Create a new DataFrame for our stats per 60 mins of TOI
stats_60 = pd.DataFrame()

# Copy over the player information and their TOI info
for col in ['last','first','pos','num','GP','TOI','TOI_5v5']:
    stats_60[col] = combined[col]

# grab new cols
stat_5v5_cols = ['corsi_for_5v5','corsi_against_5v5','corsi_5v5',
                 'fenwick_for_5v5','fenwick_against_5v5','fenwick_5v5',
                 '5v5_block','g_block_5_5v5','b_block_5_5v5','g_block_10_5v5',
                 'b_block_10_5v5','g_block_5_ev','5v5_hits','g_hit_5_5v5',
                 'b_hit_5_5v5','g_hit_10_5v5','b_hit_10_5v5']


# Need to use TOI to produce all 5v5 stats relative to their /60min of play



    

blocks.head()

import matplotlib.pyplot as plt
import seaborn as sns

# display plots in the notebook
%matplotlib inline

# increase default figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

blocks['blocks'].plot(kind='hist', bins=3)
sns.distplot(blocks['blocks'])
plt.savefig('blocks.png')

type(blocks.g_block_10_ev)

shots.comb