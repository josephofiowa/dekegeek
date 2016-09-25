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

# EDA
dfs = [blocks, cf, faceoffs, giveaways, goals, hits, miss, pen_type, pen, shots, takeaways, toi]
for x in dfs:
    print x.shape

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