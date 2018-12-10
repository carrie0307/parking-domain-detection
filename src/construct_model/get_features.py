#encoding:utf-8
import get_html_features
from typo_checker import TypoChecker
import tldextract
import pandas as pd
import re
import os
import logging

"""
提取特征
features:
1. 文件大小
2. frame与iframe数量之和
3. location_flag:是否具有window.location
4. a_nums a标签数量
5. href_max_length 最长href长度
6. href_avg_length 平均href长度
7. avg_a_href href数量与a标签数量之比
8. external_link_ratio href中外链数量
9. typo_flag: 是否是typo域名
10. digit_flag: 主域名是否是纯数字域名
11. digit_ratio: 主域名中数字比例

"""

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename="record.log",
                    filemode='a+')


dir_path = "D:/Domain Homework/data/source_code/"
# dir_path = "D:/Domain Homework/temp/"
typochecker = TypoChecker()
domain_columns = [ "size", "frame_flag", "location_flag","a_nums", "href_max_length", \
                  "href_avg_length", "avg_a_href", "external_link_ratio","typo_flag", "digit_flag", "digit_ratio"]
df = pd.DataFrame(index = ['domain'], columns = domain_columns)

def check_digit(main_domain_string):

    if str(main_domain_string).isdigit():
        return True
    else:
        return False

def get_digit_ratio(main_domain_string):

    domain = str(main_domain_string)
    digits = re.sub("\D", "", domain)
    digit_ratio = len(digits) / len(domain)
    return digit_ratio


def get_dir_filelist(dir_path):
    """
    :param path: the path of a dir
    :return: a list of files under the path
    """
    return os.listdir(dir_path)

def get_all_features():
    """
    """
    global dir_path
    filenames = get_dir_filelist(dir_path)

    length = len(filenames)
    for i, filename in enumerate(filenames):
        domain_name = domain_name = filename[:filename.find('.txt')]
        print("{} || {}: {}".format(str(i), str(length), domain_name))
        filepath = dir_path + filename
        with open(filepath, 'r', encoding = 'utf-8', errors='ignore') as f:
            content = f.read()
            size = get_html_features.get_FileSize(filepath)
            if '中国科学院大学校园网络' not in content:
                try:
                    size = get_html_features.get_FileSize(filepath)
                    frame_flag = get_html_features.check_frame(content)
                    location_flag = get_html_features.check_location(content)
                    a_nums, href_max_length, href_avg_length, avg_a_href, external_link_ratio = get_html_features.get_a_features(content, domain_name)
                    # 获取typo结果
                    t = tldextract.extract(domain_name)
                    main_domain = t.domain + "." + t.suffix
                    typo_flag = typochecker.is_typo_domain(main_domain)
                    # 判定是否是纯数字域名/数字比例
                    digit_flag = check_digit(t.domain)
                    digit_ratio = get_digit_ratio(t.domain)
                    # print (domain_name, size, frame_flag, location_flag,a_nums, href_max_length, \
                    #         href_avg_length, avg_a_href, external_link_ratio,typo_flag, digit_flag, digit_ratio)
                    res = [size, frame_flag, location_flag,a_nums, href_max_length, \
                            href_avg_length, avg_a_href, external_link_ratio,typo_flag, digit_flag, digit_ratio]
                    df.loc[domain_name] = res
                    # df.iloc[i] = res
                except Exception as err:
                    print ("特征提取异常: ", domain_name, err)
                    logging.info("特征提取异常: " + domain_name + "  " + str(err))
            else:
                print ("源码异常: " + domain_name + " 中国科学院大学校园网络 in content")
                logging.info("源码异常: " + domain_name + " 中国科学院大学校园网络 in content")

if __name__ == '__main__':
    get_all_features()
    # print (df)
    df.to_csv("test_feature_csy.csv",index = True)