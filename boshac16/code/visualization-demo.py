# -*- coding: utf-8 -*-
"""
Updated on Sat Oct  1 15:00:58 2016
@author: JosephNelson
"""

# import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# display plots in the notebook
%matplotlib inline

# increase default figure and font sizes for easier viewing
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

# grab out data
data = pd.read_csv('https://raw.githubusercontent.com/josephofiowa/dekegeek/master/boshac16/assets/data/20152016_02_merged.csv')

# check out our data
data.head()
data.columns

# make initial plot
data['goals'].plot(kind='hist', bins=20)
data[data['GP']>20]['goals'].plot(kind='hist', bins=20)
data[data['GP']>20]['5v5_goal'].plot(kind='hist', bins=20)

# add labels
data[data['GP']>20]['5v5_goal'].plot(kind='hist', bins=20)
plt.xlabel('Goals')
plt.ylabel('Frequency')

# list available plot styles
plt.style.available

# change to a different style
plt.style.use('fivethirtyeight')

# use seaborn to make a distribution plot
sns.distplot(data[data['GP']>20]['5v5_goal'])

# scatter plot
data[data['GP']>20].plot(kind='scatter', x=['fenwick_5v5'], y=['5v5_goal'], alpha=0.3)

# multiple scatter
sns.pairplot(data[(data['GP']>20) & (data['pos']=='C')], x_vars=['giveaways', 'takeaways'], y_vars='hits')


# eliminate goalies
data[(data['GP']>20) & (data['pos'] == 'C')].head()

#regression and plot -- called lmplot()
sns.lmplot(data=data[(data['GP']>20) & (data['pos']=='C')], x='fenwick_5v5', y='5v5_goal')

# optional save
sns.lmplot(data=data[(data['GP']>20) & (data['pos']=='C')], x='fenwick_5v5', y='5v5_goal')
plt.savefig('fenwick_vs_goals.png')