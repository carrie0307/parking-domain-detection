# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from construct_vec import load_data
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.model_selection import train_test_split
import os
import warnings
warnings.filterwarnings('ignore')

# train_data, train_target = load_data('./split_vectors/new_df_4000.csv')
# X_train,X_valid, y_train, y_valid = train_test_split(train_data,train_target,test_size=0.2, random_state=1023)
# feature_names = X_train.columns
from sklearn.model_selection import train_test_split
# 聚类https://www.cnblogs.com/pinard/p/6169370.html


def randomforest_Classifier():
    
    """
    RandomForest对标注数据进行测试
    从全局遍历获取数据
    """
    # clf = RandomForestClassifier(n_estimators= 50, max_depth=10,criterion='gini', min_samples_split=5, max_features='auto',
    #                              bootstrap=True, random_state=2018, verbose=2, n_jobs=-1,min_samples_leaf=4)
    clf = RandomForestClassifier()
    print ("fitting ...")
    clf.fit(X_train, y_train.values.ravel())
    # get dummy 87, oneencoder 89
    X_val_pred = clf.predict(X_valid)
    print (f1_score(y_valid, X_val_pred,average='weighted'))

def feature_evaluation_RanForest():
    
    """
    RandomForest评估特征
    从全局变量获取数据
    """
    # clf = RandomForestClassifier(n_estimators= 50, max_depth=10,criterion='gini', min_samples_split=5, max_features='auto',
    #                              bootstrap=True, random_state=2018, verbose=2, n_jobs=-1,min_samples_leaf=4)
    clf = RandomForestClassifier()
    print ("fitting ...")
    clf.fit(X_train, y_train.values.ravel())
    feature_evaluation = sorted(zip(map(lambda x: round(x, 4), clf.feature_importances_), feature_names), reverse=True)
    for feature in feature_evaluation:
        print (feature)


def kmeans_train(cluster_numbers, X, y):
    """
    Kemans训练
    :return:
    """

    model = KMeans(n_clusters=cluster_numbers, random_state=9)
    model.fit(X)
    # model.labels, model.cluster_centers_
    cluster_df = pd.DataFrame(model.labels_, index=X.index, columns = ['kmeans_res'])
    cluster_df['target'] = y
    # 根据聚类结果划分
    for kmeans_res in list(set(model.labels_)):
        # print (len(cluster_df.loc[cluster_df['kmeans_res'] == kmeans_res]))
        reference = cluster_df.loc[cluster_df['kmeans_res'] == kmeans_res]['target'].value_counts()
        # 如果这个类簇里面恶意的数量多余良性的数量，则认为该簇内所有类型未知的域名是恶意的
        try:
            if reference.loc[-1] > reference.loc[1]:
                # print (reference.loc[-1], reference.loc[1], reference.loc[0])
                cluster_df.loc[(cluster_df['kmeans_res'] == kmeans_res) & (cluster_df['target'] == 0), 'pred_res'] = -1
        except:
            # 有的类簇里可能不存在reference.loc[-1] , reference.loc[1]
            pass
   

    return list(cluster_df.loc[cluster_df['pred_res'] == -1].index), len(list(cluster_df.loc[cluster_df['pred_res'] == -1].index))


def kmeans_test(cluster_numbers, X, y):
    """
    单一文件 KMeans 测试
    """

    model = KMeans(n_clusters=cluster_numbers, random_state=9)
    model.fit(X)
    print (list(set(model.labels_)))
    # model.labels, model.cluster_centers_
    cluster_df = pd.DataFrame(model.labels_, index=X.index, columns = ['kmeans_res'])
    cluster_df['target'] = y
    # 根据聚类结果划分
    for kmeans_res in list(set(model.labels_)):
        # 聚类结果为kmeans_res类簇内域名的结果，是该类簇内target中出现最多的那一种
        cluster_df.loc[cluster_df['kmeans_res'] == kmeans_res, 'pred_res'] = \
        cluster_df.loc[cluster_df['kmeans_res'] == kmeans_res]['target'].value_counts().index[0]
        # print ("kmeans_res = {}".format(kmeans_res)) 
        # print(cluster_df.loc[cluster_df['kmeans_res'] == kmeans_res]['target'].value_counts(), '\n')
    # print (cluster_df.loc[cluster_df['kmeans_res'] == 0, 'res'],cluster_df.loc[cluster_df['kmeans_res'] == 1, 'res'],cluster_df.loc[cluster_df['kmeans_res'] == 2, 'res'])
    f1 = f1_score(cluster_df['target'], cluster_df['pred_res'], average='weighted')
    # evaluate = metrics.calinski_harabaz_score(X_train, model.labels_)
    return f1

if __name__ == '__main__':
    
    # Kmeans 实际训练 分别读取D:/Domain Homework/src/split_vectors2/下分组好的每个数据文件
    filenames = os.listdir("./split_vectors2/")
    for filename in filenames:
        print (filename)
        train_data, train_target = load_data('./split_vectors2/{}'.format(filename))
        domains, num = kmeans_train(50, train_data, train_target)
        # 将提取到的可疑域名写入文件
        if domains:
            domains = '\n'.join(domains)
            with open('./split_vectors2_res/{}.txt'.format(filename[:filename.find('.csv')]), 'w') as f:
                f.write(domains)

    # Kmeans 测试
    # train_data, train_target = load_data('./res_df.csv')
    # f1 = kmeans_test(2, train_data, train_target)
    # print (f1)
    
    # all data
    # train_data, train_target = load_data('./final_features.csv')
    # Single Train
    # train_data, train_target = load_data('./split_vectors2/new_df_4000.csv')
    # k=50
    # domains = kmeans_train(50, train_data, train_target)
    
    # feature_evaluation_RanForest()
    # randomforest_Classifier()