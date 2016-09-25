# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 18:25:22 2016

@author: JosephNelson
"""

# loading data
blocks = pd.read_csv('./assets/data/20152016_02_total_blocks.csv')
blocks.head()
blocks.describe()

cf = pd.read_csv('./assets/data/20152016_02_total_cf.csv')

faceoffs = pd.read_csv('./assets/data/20152016_02_total_faceoff.csv')

giveaways = pd.read_csv('./assets/data/20152016_02_total_giveaways.csv')

goals = pd.read_csv('./assets/data/20152016_02_total_goals.csv')

hits = pd.read_csv('./assets/data/20152016_02_total_hits.csv')

miss = pd.read_csv('./assets/data/20152016_02_total_miss.csv')

pen_type = pd.read_csv('./assets/data/20152016_02_total_pen_type.csv')

'./assets/data/20152016_02_total_pen.csv'
'./assets/data/20152016_02_total_shot.csv'
'./assets/data/20152016_02_total_take.csv'

