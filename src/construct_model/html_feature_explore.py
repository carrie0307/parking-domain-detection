#encoding:utf-8

"""
对HTML源码特征进行初步研究的代码
"""
import os
from pandas import Series, DataFrame
import pandas as pd
from lxml import etree
import re
import tldextract

# black_path = "D:/Domain Homework/spider/black/"
# white_path = "D:/Domain Homework/spider/white/"
black_path = "D:/Domain Homework/data/source_code/black/"
white_path = "D:/Domain Homework/data/alexa/"

# ww1.bananaidol.com
# with open("D:/Domain Homework/spider/black/ww1.909900tk.com.txt", 'r', encoding='utf-8') as f:
#     print (f.read())

def get_FileSize(filepath):
    """
    :param filepath: the path of a file
    :return: the size of the file
    """
    size = os.path.getsize(filepath)
    size_MB = size
    return size_MB

def get_dir_filelist(dir_path):
    """
    :param path: the path of a dir
    :return: a list of files under the path
    """
    return os.listdir(dir_path)

def get_filesize_series(dir_path):
    """
    :param dir_path: the path of a dir
    :return: a siries of size of files under dir_path
    """
    filesize_list = []
    filelist = get_dir_filelist(dir_path)
    for filename in filelist:
        file_path = dir_path + filename
        size = get_FileSize(file_path)
        filesize_list.append(size)
    filesize_series = Series(filesize_list)
    return filesize_series

# normal_count = 0
# abnormal_count = 0
# filelist = get_dir_filelist(black_path)
# for filename in filelist:
#     file_path = black_path + filename
#     with open(file_path, 'r', encoding='utf-8') as f:
#         content = f.read()
#     if '中国科学院大学校园网络' not in content:
#         normal_count += 1
#     else:
#         abnormal_count += 1
# print ("校园网: ", abnormal_count)
# print ("正常: ", normal_count)

def frame_check(dir_path):
    """
    :param dir_path: the path of a dir
    :return: a series of number of frames&iframes tags of files under dir_path
    """
    frame_list = []
    filelist = get_dir_filelist(dir_path)
    for filename in filelist:
        file_path = dir_path + filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '中国科学院大学校园网络' not in content:
                    html_content = etree.HTML(content)
                    frame_res = html_content.xpath('//frame')
                    iframe_res = html_content.xpath('//iframe')
                    res = len(frame_res) + len(iframe_res)
                    frame_list.append(res)
        except Exception as err:
            pass
            # print (filename, err)
    frame_series = Series(frame_list)
    return frame_series


def check_location(dir_path):
    """
    :param dir_path: path of a dir
    :return: the number of files which contains "window.location"
    """
    count = 0
    filelist = get_dir_filelist(dir_path)
    for filename in filelist:
        file_path = dir_path + filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '中国科学院大学校园网络' not in content:
                    if "window.location" in content:
                        # print (filename)
                        count += 1
        except:
            pass
    print ("location count: ", count)
    return count

def check_a(dir_path):
    """
    :param dir_path: path of a dir
    :return:
    """
    a_list = []
    filelist = get_dir_filelist(dir_path)
    for filename in filelist:
        file_path = dir_path + filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '中国科学院大学校园网络' not in content:
                    html_content = etree.HTML(content)
                    a_res = html_content.xpath('//a')
                    a_list.append(len(a_res))
        except Exception as err:
            pass
                    # print (filename, err)
    a_series = Series(a_list)
    return a_series


def check_avg_a2href(dir_path):
    """
    计算平均每个<a>拥有href的数量
    :param dir_path:
    :return:
    """
    res_list = []
    pattern = '(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
    filelist = get_dir_filelist(dir_path)
    for filename in filelist:
        file_path = dir_path + filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '中国科学院大学校园网络' not in content:
                    html_content = etree.HTML(content)
                    a_hrefs = html_content.xpath('//a/@href')
                    a_href_nums = []
                    for href in a_hrefs:
                        href = 'http://' + href if 'http' not in href else href
                        if re.match(pattern, href):
                            a_href_nums.append(href)
                    a_nums = html_content.xpath('//a')
                    avg_a_href = len(a_href_nums) / len(a_nums)
                    res_list.append(avg_a_href)
                    # for a_tag in a_res:
                    #     print (a_tag.xpath('@href'))
        except Exception as err:
            pass
            # print (filename, err)
    res_series = Series(res_list)
    return res_series

def check_length_ahref(dir_path):
    """
    :function: 计算<a>标签链接的长度
    :param dir_path:
    :return:
    """

    avg_res, max_res = [], []
    pattern = '(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
    filelist = get_dir_filelist(dir_path)
    for filename in filelist:
        file_path = dir_path + filename
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                length_sum,length_count,max_length = 0,0,0
                html_content = etree.HTML(content)
                a_hrefs = html_content.xpath('//a/@href')
                for href in a_hrefs:
                    href = 'http://' + href if 'http' not in href else href
                    if re.match(pattern, href):
                        curr_href_length = len(href)
                        length_sum += curr_href_length
                        length_count += 1
                        max_length = curr_href_length if curr_href_length > max_length else max_length
            if length_count == 0:
                avg_res.append(0)
                max_res.append(0)
            else:
                avg_res.append(length_sum / length_count)
                max_res.append(max_length)
        except Exception as err:
            pass
    avg_res, max_res = Series(avg_res), Series(max_res)
    return avg_res, max_res

def check_external_link_ratio(dir_path):

    res_list = []
    pattern = '(https?)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
    filelist = get_dir_filelist(dir_path)
    for filename in filelist:
        file_path = dir_path + filename
        domain_name = filename[:filename.find('.txt')]
        t = tldextract.extract(domain_name)
        domain = t.domain + "." + t.suffix
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                total_hrefs, external_hrefs = 0, 0
                html_content = etree.HTML(content)
                a_hrefs = html_content.xpath('//a/@href')
                for href in a_hrefs:
                    href = 'http://' + href if 'http' not in href else href
                    if re.match(pattern, href):
                        total_hrefs += 1
                        t = tldextract.extract(href)
                        curr_main_domain = t.domain + "." + t.suffix
                        if curr_main_domain != domain:
                            external_hrefs += 1
                if total_hrefs != 0:
                    external_ratio = external_hrefs / total_hrefs
                    res_list.append(external_ratio)
        except:
            pass
    return Series(res_list)







# print ("size black:")
# black_res = get_filesize_series(black_path)
# print (black_res.describe())
# print ("seze white:")
# white_res = get_filesize_series(white_path)
# print (white_res.describe())
#
# print ("frame black:")
# black_res = frame_check(black_path)
# print (black_res.describe())
# print ("frame white: ")
# white_res = frame_check(white_path)
# print (white_res.describe())
#
# print ("num of <a> black:")
# black_res = check_a(black_path)
# print (black_res.describe())
# print ("num of <a> white:")
# white_res = check_a(white_path)
# print (white_res.describe())
#
# print ("avg href/<a> black: ")
# black_res = check_avg_a2href(black_path)
# print (black_res.describe())
# print ("avg href/<a> white: ")
# white_res = check_avg_a2href(white_path)
# print (white_res.describe())
#
# print ("num of pages which contain 'window.location()' black: ")
# black_res = check_location(black_path)
# print (black_res)
# print ("num of pages which contain 'window.location()' white: ")
# black_res = check_location(black_path)
# print (black_res)

# print ("avg/max length of hrefs in black: ")
# black_avg_res, black_max_res = check_length_ahref(black_path)
# print (black_avg_res.describe(), black_max_res.describe())
# print ("avg/max length of hrefs in white: ")
# white_avg_res, white_max_res = check_length_ahref(white_path)
# print (white_avg_res.describe(), white_max_res.describe())

print ("external link ratio black: ")
black_res = check_external_link_ratio(black_path)
print (black_res.describe())
print ("external link ration white: ")
white_res = check_external_link_ratio(white_path)
print (white_res.describe())


