# -*- coding: utf-8 -*-       
import os  
    
def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        for i in range(len(files)):
            files[i] = os.path.splitext(files[i])[0]
        # print(files)
        return files

domain_file = 'new_domain_now.txt'
domain_dir = 'saved_source'
filter_file = 'filter_domain.txt'

# 读取所有域名
domain_list_all = list()
with open(domain_file, mode="r") as f:
    for line in f:
        line = line.strip()
        domain_list_all.append(line)

# 读取已爬到域名
domain_list_now = file_name(domain_dir)

# 取差集
set_all = set(domain_list_all)
set_now = set(domain_list_now)
set_filter = set_all - set_now
# set_filter = set_now - set_all
list_filter = [i for i in set_filter]
# print(list_filter)

# 写入文件
with open(filter_file, mode="w") as f:
    for line in list_filter:
        f.write(line+'\n')