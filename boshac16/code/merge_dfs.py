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
