#encoding:utf-8

"""
    从csv文件读取特征构成特征向量
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import argparse
import pickle

parser = argparse.ArgumentParser(description='Construct Vectors')
parser.add_argument('--contain_har', type=bool, default=False, help='train data source')
args = parser.parse_args()

# ['size', 'frame_flag', 'location_flag', 'a_nums', 'href_max_length',
# 'href_avg_length', 'avg_a_href', 'external_link_ratio', 'typo_flag',
# 'digit_flag', 'digit_ratio', 'res']

def load_data(filename):
    train_data = pd.read_csv(filename, low_memory=False, index_col='domain')

    one_hot_features = ['location_flag', 'typo_flag', 'digit_flag']
    range_features = ['size', 'a_nums', 'href_max_length', 'href_avg_length', 'avg_a_href',\
                      'external_link_ratio','digit_ratio', 'frame_nums']
    # href_avg_length, avg_a_href, external_link_ratio 中为 '\'的全部赋值为了0

    # View missing values
    # print (train_data.isnull().any())
    # print (train_data[train_data.isnull().values == True])

    train_data[range_features] = train_data[range_features].astype('float64')

    # One-hot 
    enc = OneHotEncoder()
    for feature in one_hot_features:

        enc.fit(train_data[feature].values.reshape(-1, 1))
        train_a = enc.transform(train_data[feature].values.reshape(-1, 1))
        train_a = train_a.toarray()

        train_b = pd.DataFrame(train_a, index=train_data.index)
        train_b.columns = [list(map(lambda x: feature + '_' + str(x), range(train_a.shape[1])))]
        train_data  = pd.concat([train_data, train_b], axis=1)
        train_data = train_data.drop([feature], axis=1)

    train_target = train_data['res']
    train_data = train_data.drop(['res'], axis=1)
    return train_data, train_target


if __name__ == '__main__':
    train_data, train_target = load_data("./final_features.csv")