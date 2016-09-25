# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 18:25:22 2016

@author: JosephNelson
"""

blocks = pd.read_csv('./20152016_02_total_blocks.csv')
blocks.head()
blocks.describe()

cf = pd.read_csv('./20152016_02_total_cf.csv')

faceoffs = pd.read_csv('./20152016_02_total_faceoff.csv')

giveaways = pr.read_csv('./20152016_02_total_giveaways.csv')