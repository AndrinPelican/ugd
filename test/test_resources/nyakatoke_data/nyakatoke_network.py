import pandas as pd
import numpy as np


# The Data
try:
    Nyakatoke_ind = pd.read_stata("test/test_resources/nyakatoke_data/Nyakatoke individual.dta")
    Nyakatoke_dyad = pd.read_stata("test/test_resources/nyakatoke_data/Nyakatoke dyadic.dta")
    Nyakatoke_hh = pd.read_stata("test/test_resources/nyakatoke_data/Nyakatoke household.dta")
    Nyakatoke_dir = pd.read_stata("test/test_resources/nyakatoke_data/Nyakatoke directed.dta")
except:
    Nyakatoke_ind = pd.read_stata("test_resources/nyakatoke_data/Nyakatoke individual.dta")
    Nyakatoke_dyad = pd.read_stata("test_resources/nyakatoke_data/Nyakatoke dyadic.dta")
    Nyakatoke_hh = pd.read_stata("test_resources/nyakatoke_data/Nyakatoke household.dta")
    Nyakatoke_dir = pd.read_stata("test_resources/nyakatoke_data/Nyakatoke directed.dta")



'''
Data Preperation:
'''

Nyakatoke_ind['hh1']=Nyakatoke_ind['hhind'].apply(str).str[2:5]      # Create household ID number
Nyakatoke_ind['iid']=Nyakatoke_ind['hhind'].apply(str).str[5:7]      # Create individual ID number

# Find age of household head
Nyakatoke_ind['head_age'] = None
Nyakatoke_ind.loc[Nyakatoke_ind['iid']=='01', 'head_age'] = Nyakatoke_ind['age']

# Find sex of household head
Nyakatoke_ind['head_sex'] = None
Nyakatoke_ind.loc[Nyakatoke_ind['iid']=='01', 'head_sex'] = Nyakatoke_ind['sex']


# Now work with the dyadic dataframe
# Convert hh1 to string and add leading zeros (to matched with hh dataframe created above)
Nyakatoke_dyad.loc[:,'hh1'] = Nyakatoke_dyad['hh1'].apply(str).str.zfill(5)

# remove decimal and digits to its right
Nyakatoke_dyad.loc[:,'hh1'] = Nyakatoke_dyad['hh1'].apply(str).str[0:3]

# Repeat conversions for hh2
Nyakatoke_dyad.loc[:,'hh2'] = Nyakatoke_dyad['hh2'].apply(str).str.zfill(5)
Nyakatoke_dyad.loc[:,'hh2'] = Nyakatoke_dyad['hh2'].apply(str).str[0:3]


# NOTE: Last merge creates two instances of hh1 due to how the merge above was done. Drop the second instance and
#       rename the first
# Nyakatoke_dyad.drop('hh1_y', axis=1, inplace=True)
Nyakatoke_dyad.rename(columns={'hh1_x' : 'hh1'}, inplace=True)

Nyakatoke_dyad.rename(columns={'head_age' : 'head_age2', 'head_sex' : 'head_sex2', 'education' : 'education2'}, inplace=True)

'''
add wealth
'''

# Comola and Fafchamps (2014) wealth formula# Comol
Nyakatoke_dyad['wealth1'] = (300000*Nyakatoke_dyad['land1'] + Nyakatoke_dyad['livestock1'])/100000
Nyakatoke_dyad['wealth2'] = (300000*Nyakatoke_dyad['land2'] + Nyakatoke_dyad['livestock2'])/100000
# Group households by wealth
# Very Poor
set1 = set([row['hh1'] for index, row in Nyakatoke_dyad.iterrows() if (row['wealth1'] < 1.5)])
very_poor = list(set1 )

# Poor
set1 = set([row['hh1'] for index, row in Nyakatoke_dyad.iterrows() if (row['wealth1'] >= 1.5) & (row['wealth1'] < 3)])
poor = list(set1 )

# Middle
set1 = set([row['hh1'] for index, row in Nyakatoke_dyad.iterrows() if (row['wealth1'] >= 3) & (row['wealth1'] < 6)])
middle = list(set1 )

# Rich
set1 = set([row['hh1'] for index, row in Nyakatoke_dyad.iterrows() if (row['wealth1'] >= 6)])
rich = list(set1 )






'''
Create adj _m and variable_dict
'''
var_dict = {}
id_to_ind_dict = {}
for i, id in enumerate(Nyakatoke_dyad['hh1'].unique()):
    id_to_ind_dict[id] = i
    var_dict[i] = {} # initialize vardict


# adjancy matrix:
adj_m = np.zeros(shape=(id_to_ind_dict.__len__(),id_to_ind_dict.__len__()))
for key, row in Nyakatoke_dyad.iterrows():
    if row['links']=='reciprocal link' or row['links']=='unilateral link' :
        if row['hh1'] == '122' or row['hh2'] == '122':
            continue
        from_int = id_to_ind_dict[row['hh1']]
        to_int = id_to_ind_dict[row['hh2']]
        adj_m[from_int,to_int] = 1
        adj_m[to_int,from_int] = 1

# adjancy matrix:
di_adj_m = np.zeros(shape=(id_to_ind_dict.__len__(), id_to_ind_dict.__len__()))
for key, row in Nyakatoke_dyad.iterrows():
    if row['links'] == 'reciprocal link' or row['links'] == 'unilateral link':
        if row['hh1'] == '122' or row['hh2'] == '122':
            continue
        from_int = id_to_ind_dict[row['hh1']]
        to_int = id_to_ind_dict[row['hh2']]
        di_adj_m[from_int, to_int] = 1



# var_dict
for key, row in Nyakatoke_dyad.iterrows():
    index_int = id_to_ind_dict[row['hh1']]
    var_dict[index_int]['clan'] = row['clan1']
    # var_dict[index_int]['education'] = row['education1']
    var_dict[index_int]['religion'] = row['religion1']
    if row['land1']>0.5:
        var_dict[index_int]['land']  = 'has_land'
    else:
        var_dict[index_int]['land'] = 'no_land'
    if row['livestock1']>10000:
        var_dict[index_int]['animals'] = 'many'
    else:
        var_dict[index_int]['animals'] = 'few'


for key in very_poor:
    index_int = id_to_ind_dict[key]
    var_dict[index_int]['wealth_granular'] = 'very_poor'
    var_dict[index_int]['wealth'] = 'poor'

for key in poor:
    index_int = id_to_ind_dict[key]
    var_dict[index_int]['wealth_granular'] = 'poor'
    var_dict[index_int]['wealth'] = 'poor'

for key in middle:
    index_int = id_to_ind_dict[key]
    var_dict[index_int]['wealth_granular'] = 'middle'
    var_dict[index_int]['wealth'] = 'rich'

for key in rich:
    index_int = id_to_ind_dict[key]
    var_dict[index_int]['wealth_granular'] = 'rich'
    var_dict[index_int]['wealth'] = 'rich'


