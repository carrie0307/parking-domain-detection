#encoding:utf-8

import pandas as pd
from typo_checker import TypoChecker
import os

all_domain_df = pd.read_csv('final_features.csv', index_col = 0)
res1_dm = all_domain_df.loc[all_domain_df['res'] == 1]
print (len(res1_dm))
res_n1_dm = all_domain_df.loc[all_domain_df['res'] == -1]
res_dm = res1_dm.append(res_n1_dm) # 3562
res_df = pd.DataFrame(res1_dm.append(res_n1_dm), index=res1_dm.index.append(res_n1_dm.index), columns = res_n1_dm.columns)
print (res_df.index)
print (res_df.columns)
res_df.to_csv('./res_df.csv')
res0_dm = all_domain_df.loc[all_domain_df['res'] == 0] # 560162, 560162 / 3562 = 157.26 
res0_dm_length = len(res0_dm)
i = 0
while i + 4000 < res0_dm_length:
    print ("{} // {}".format(str(i), str(res0_dm_length)))
    curr_dm = res0_dm.iloc[i:i+4000]
    new_df = pd.DataFrame(curr_dm.append(res_dm), index=curr_dm.index.append(res_dm.index), columns = all_domain_df.columns)
    i = i + 4000
    new_df.to_csv('./split_vectors/new_df_{}.csv'.format(i))

# curr_dm = res0_dm.iloc[i:res0_dm_length]
# new_df.to_csv('./split_vectors/new_df_{}.csv'.format(i))
# pd.DataFrame(model.labels_, index=X_train.index, columns = ['kmeans_res'])
# curr_dm = res0_dm.iloc[0:4000]
# new_df = pd.DataFrame(curr_dm.append(res_dm), index=curr_dm.index.append(res_dm), columns = ['kmeans_res'])



# print (len(all_domain_df[all_domain_df['res'] == 1]),len(set(list(all_domain_df[all_domain_df['res'] == 1].index))))
# print (len(all_domain_df[all_domain_df['res'] == -1]),len(set(list(all_domain_df[all_domain_df['res'] == -1].index))))
# print (len(all_domain_df[all_domain_df['res'] == 0]),len(set(list(all_domain_df[all_domain_df['res'] == 0].index))))
# print (len(all_domain_df))
# print (len(set(list(all_domain_df.index))))
