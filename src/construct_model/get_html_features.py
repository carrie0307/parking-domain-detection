#encoding:utf-8

"""
    从HTML源码提取特征函数
"""

import os
from pandas import Series, DataFrame
import pandas as pd
from lxml import etree
import re
import tldextract
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename="record.log",
                    filemode='a+')

dir_path = "D:/Domain Homework/temp/"


def get_FileSize(filepath):
    """
    :param filepath: the path of a file
    :return: the size of the file
    """
    size = os.path.getsize(filepath)
    size_MB = size
    return size_MB

def check_frame(content):
    """
    :param dir_path: the path of a dir
    :return: the number of frames&iframes tags
    """
    content = bytes(bytearray(content, encoding='utf-8'))
    html_content = etree.HTML(content)
    frame_res = html_content.xpath('//frame')
    iframe_res = html_content.xpath('//iframe')
    res = len(frame_res) + len(iframe_res)
    return res



def check_location(content):
    """
    :param dir_path: path of a dir
    :return: the number of files which contains "window.location"
    """

    if "window.location" in content:
        return True
    else:
        return False

def get_a_features(content,domain_name):
    """
    :param dir_path: path of a dir
    :return:a_nums: a 标签数量
            href_max_length,  href最大长度
            href_avg_length,  href平均长度
            avg_a_href,       平均每个a标签下href的数量
            external_link_ratio, 外链比例
    """
    pattern = '(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
    content = bytes(bytearray(content, encoding='utf-8'))
    html_content = etree.HTML(content)
    a_nums = len(html_content.xpath('//a'))
    a_hrefs = html_content.xpath('//a/@href')
    valid_href_count,href_max_length, href_length_total,external_hrefs = 0,0,0,0
    for href in a_hrefs:
        href = 'http://' + href if 'http' not in href else href
        if re.match(pattern, href):
            # features about <a> and hrefs
            valid_href_count += 1
            href_length = len(href)
            href_length_total += href_length
            href_max_length = href_length if href_length > href_max_length else href_max_length
            # external ratio
            t = tldextract.extract(href)
            curr_main_domain = t.domain + "." + t.suffix
            if curr_main_domain != domain_name:
                external_hrefs += 1
    href_avg_length = href_length_total / valid_href_count if valid_href_count != 0 else '/'
    avg_a_href = valid_href_count / a_nums if a_nums != 0 else '/'
    external_link_ratio = external_hrefs / valid_href_count if valid_href_count != 0 else '/'
    return a_nums, href_max_length, href_avg_length, avg_a_href,external_link_ratio

def get_dir_filelist(dir_path):
    """
    :param path: the path of a dir
    :return: a list of files under the path
    """
    return os.listdir(dir_path)

def get_all_htmlfeatures():
    """
    """
    global dir_path
    filenames = get_dir_filelist(dir_path)
    for filename in filenames:
        domain_name = domain_name = filename[:filename.find('.txt')]
        filepath = dir_path + filename
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            size = get_FileSize(filepath)
            if '中国科学院大学校园网络' not in content:
                try:
                    size = get_FileSize(filepath)
                    frame_flag = check_frame(content)
                    location_flag = check_location(content)
                    a_nums, href_max_length, href_avg_length, avg_a_href, external_link_ratio = get_a_features(content, domain_name)
                    print (domain_name, size, frame_flag, location_flag,a_nums, href_max_length, href_avg_length, avg_a_href, external_link_ratio)
                    """
                    这里单个文件的结果后，对结果进行汇总返回即可
                    """
                except Exception as err:
                    print (domain_name, err)
                    logging.info("特征提取异常: " + domain_name + "  " + str(err))
            else:
                logging.info("源码异常: " + domain_name + " 中国科学院大学校园网络 in content")


if __name__ == '__main__':
    """
    每读一个判断文件是否存在
    文件不存在置source_code=-1,相关特征也是/;存在置source_Code为1
    先把black domains的全部写完，然后单独写white domains的
    """
    pass
    # get_all_htmlfeatures()


    # domain_df = pd.read_csv('./features.csv', index_col=0)
    # domains = domain_df.loc[domain_df['white'] == 1, 'domain'].values
    # print (len(domains))
    # for domain_name in domains:
    #     filepath = "D:/Domain Homework/data/alexa/" + domain_name + ".txt"
    #     # filepath = "D:/Domain Homework/spider/black/ww1.bananaidol.com.txt"
    #     if not os.path.exists(filepath):
    #         print (domain_name + "   not exist")
    #     else:
    #         try:
    #             with open(filepath, 'r', encoding='utf-8') as f:
    #                 content = f.read()
    #                 if '中国科学院大学校园网络' not in content:
    #                     size = get_FileSize(filepath)
    #                     frame_flag = check_frame(content)
    #                     location_flag = check_location(content)
    #                     a_nums, href_max_length, href_avg_length, avg_a_href, external_link_ratio = get_a_features(content, domain_name)
    #                     print (domain_name, size, frame_flag, location_flag,a_nums, href_max_length, href_avg_length, avg_a_href, external_link_ratio)
    #                     domain_df.loc[domain_df['domain'] == domain_name,['size', 'frame_flag', 'location_flag', 'a_nums', 'href_max_length',\
    #                         'href_avg_length', 'avg_a_href', 'external_link_ratio','source_code']] = size, frame_flag, location_flag, a_nums, href_max_length,\
    #                                                                                  href_avg_length, avg_a_href, external_link_ratio, 1
    #         except:
    #             pass
    # domain_df.to_csv('./features.csv')