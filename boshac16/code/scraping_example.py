import pandas as pd
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parse
import requests
import re

'''
This script is temporary until we start to scrape TOI from NHL gamesheets.
Currently scraping from stats.hockeyanalysis.com.
'''

def scrape_url(url):
    # Get the html of the page
    html = requests.get(url).text
    # Convert to BeautifulSoup object
    soup = BeautifulSoup(html,'html.parser')
    # Find the table containing the statistics
    table = soup.find('table',{'border':'1','bgcolor':'#aaaaaa'})
    # Convert to two-dimensional table to make parsing easier
    twodim_table = parse.make2d(table)
    df = pd.DataFrame(twodim_table)
    # Set the column names and get rid of reprinted header rows throughout table
    df.columns = df.ix[0,:]
    df = df[df['#'] != '#']
    # Select only the players name, games played, and time on ice
    df = df[['Player Name','GP','TOI']]
    return df

# Scrape the GP/TOI data for all situations
url_all = 'http://stats.hockeyanalysis.com/ratings.php?db=201516&sit=all&type=individual&teamid=0&pos=skaters&minutes=1&disp=1&sort=PCT&sortdir=DESC'
df_all = scrape_url(url_all)

# Scrape the GP/TOI data for 5v5
url_5v5 = 'http://stats.hockeyanalysis.com/ratings.php?db=201516&sit=5v5&type=individual&teamid=0&pos=skaters&minutes=1&disp=1&sort=PCT&sortdir=DESC'
df_5v5 = scrape_url(url_5v5)
# Get rid of GP column so it isn't duplicated when we merge
del df_5v5['GP']
# Select only the players name and 5v5 time on ice
df_5v5.columns = ['Player Name','TOI_5v5']

# Merge our two DataFrames
combined = df_all.merge(df_5v5,on='Player Name',how='outer')
# Create new columns for players first and last names (to match NHL gamesheets)
combined['first'] = combined['Player Name'].apply(lambda s: s.split(', ')[1])
combined['last'] = combined['Player Name'].apply(lambda s: s.split(', ')[0])
combined['last'] = combined['last'].apply(lambda s: re.sub('_',' ',s))
# Re-order the columns and save to CSV
combined = combined[['last','first','GP','TOI','TOI_5v5']]
combined.to_csv('/Users/Brian/NHL_Webscraper/Season_Totals/20152016_02/20152016_02_total_gp_toi.csv',index=False)
