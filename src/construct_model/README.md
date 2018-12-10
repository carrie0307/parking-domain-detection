## 代码说明

* construct_vec.py  读取CSV文件对特征进行处理和构建

* detect.py   对原始域名数据进行统计和特征发现

* data.py  根据已标注数据数量对final_features.csv数据进行分组

* get_features.py   从域名相关数据中提取特征，生成CSV文件

* get_html_features.py  从HTML源码提取特征相关函数

* get_resp_info.py    通过urllib获取源码

* html_feature_explore.py  对HTML特征的统计和分析

* qwerty.map   typo域名判断的辅助字典

* train.py  模型训练与特征项评估

* typo_checker.py   检测域名是否是typo域名

## 模型训练：运行 train.py 

在PPT讲解中会提到，聚类是对已分组的数据进行的。

由于数据量较大，上交时只提交了对final_features.csv分组后的两个样例文件，位于./split_vector/。运行train.py即可在./split_vector_res/得到对这两组数据域名聚类结果