import pandas as pd

# Read in the CSV files
toi = pd.read_csv('https://raw.githubusercontent.com/josephnelson93/dekegeek/master/boshac16/assets/data/20152016_02_total_gp_toi.csv')
cf = pd.read_csv('https://raw.githubusercontent.com/josephnelson93/dekegeek/master/boshac16/assets/data/20152016_02_total_cf.csv')
blocks = pd.read_csv('https://raw.githubusercontent.com/josephnelson93/dekegeek/master/boshac16/assets/data/20152016_02_total_blocks.csv')
hits = pd.read_csv('https://raw.githubusercontent.com/josephnelson93/dekegeek/master/boshac16/assets/data/20152016_02_total_hits.csv')

# Select the columns we want
cf = cf[['comb','corsi_for_5v5','corsi_against_5v5','corsi_5v5','corsi_for',
         'corsi_against','corsi','fenwick_for_5v5','fenwick_against_5v5',
         'fenwick_5v5','fenwick_for','fenwick_against','fenwick']]

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

# Merge our DataFrames
combined = toi.merge(cf,on='comb',how='outer')
combined = combined.merge(blocks,on='comb',how='outer')
combined = combined.merge(hits,on='comb',how='outer')
# Save the combined DataFrame to CSV
combined.to_csv('/Users/Brian/dekegeek/boshac16/assets/data/20152016_02_total_merged.csv',index=False)

combined
combined = combined.ix[combined.pos != 'G']

def convert_to_60(time):
    mins = int(time.split(':')[0])
    secs = int(time.split(':')[1])
    secs = secs/60.0
    converted_mins = mins + secs
    return converted_mins/60.0

# Convert our TOI columns to number of 60 minutes intervals
combined['TOI'] = combined['TOI'].apply(convert_to_60)
combined['TOI_5v5'] = combined['TOI_5v5'].apply(convert_to_60)

# Create a new DataFrame for our stats per 60 mins of TOI
stats_60 = pd.DataFrame()
# Copy over the player information and their TOI info
for col in ['last','first','pos','num','GP','TOI','TOI_5v5']:
    stats_60[col] = combined[col]

stat_5v5_cols = ['corsi_for_5v5','corsi_against_5v5','corsi_5v5',
                 'fenwick_for_5v5','fenwick_against_5v5','fenwick_5v5',
                 '5v5_block','g_block_5_5v5','b_block_5_5v5','g_block_10_5v5',
                 'b_block_10_5v5','g_block_5_ev','5v5_hits','g_hit_5_5v5',
                 'b_hit_5_5v5','g_hit_10_5v5','b_hit_10_5v5']
for col in stat_5v5_cols:
    stats_60[col+'/60'] = combined[col]/stats_60['TOI_5v5']

stat_all_cols = ['corsi_for','corsi_against','corsi','fenwick_for',
                 'fenwick_against','fenwick','blocks','hits','5v5_hits']
for col in stat_all_cols:
    stats_60[col+'/60'] = combined[col]/stats_60['TOI']

g_block_5_all = combined['g_block_5_ev'] + combined['g_block_5_pp'] + combined['g_block_5_sh']
b_block_5_all = combined['b_block_5_ev'] + combined['b_block_5_pp'] + combined['b_block_5_sh']
g_block_10_all = combined['g_block_10_ev'] + combined['g_block_10_pp'] + combined['g_block_10_sh']
b_block_10_all = combined['b_block_10_ev'] + combined['b_block_10_pp'] + combined['b_block_10_sh']
g_hit_5_all = combined['g_hit_5_ev'] + combined['g_hit_5_pp'] + combined['g_hit_5_sh']
b_hit_5_all = combined['g_hit_5_ev'] + combined['g_hit_5_pp'] + combined['g_hit_5_sh']
g_hit_10_all = combined['g_hit_10_ev'] + combined['g_hit_10_pp'] + combined['g_hit_10_sh']
b_hit_10_all = combined['g_hit_10_ev'] + combined['g_hit_10_pp'] + combined['g_hit_10_sh']

# Create a temporary DataFrame to calculate the good/bad hits and blocks for
# all situations
calc_df = pd.DataFrame()
cols = [g_block_5_all,b_block_5_all,g_block_10_all,b_block_10_all,g_hit_5_all,b_hit_5_all,g_hit_10_all,b_hit_10_all]
col_names = ['g_block_5_all','b_block_5_all','g_block_10_all','b_block_10_all','g_hit_5_all','b_hit_5_all','g_hit_10_all','b_hit_10_all']
for col_name,col in zip(col_names,cols):
    calc_df[col_name] = col
    
# Calculate the stat/60 for each of these
calc_df['TOI'] = combined['TOI']
for col in col_names:
    calc_df[col+'/60'] = calc_df[col]/calc_df['TOI']
# Add only the stat/60 columns to our stats_60 DataFrame
for col in col_names:
    stats_60[col+'/60'] = calc_df[col+'/60']
