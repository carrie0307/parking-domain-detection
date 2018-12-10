# -*- coding: utf-8 -*-

from browsermobproxy import Server
from selenium import webdriver
import ExtractLevelDomain
# import json


class GetHar(object):

    def __init__(self):
        self.domain_file = 'domain.txt'
        self.domain_list = list()
        self.temp_domain_str = ''
        self.har = dict()
        self.feature_list = list()
        self.save_path = 'har_features.txt'

    def _read_file(self):
        with open(self.domain_file, mode='r') as f:
            for line in f:
                line = line.strip()
                self.domain_list.append(line)

    def _get_har(self):
        # 登录操作
        server = Server("browsermob-proxy-2.0-beta-6/bin/browsermob-proxy.bat")
        server.start()
        proxy = server.create_proxy()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(chrome_options=chrome_options)
        proxy.new_har("google")
        browser.get("http://" + self.temp_domain_str)
        proxy.har  # returns a HAR JSON bl
        har = proxy.har
        server.stop()
        browser.quit()
        self.har = har

    def _get_feature(self):
        domain_filter = ExtractLevelDomain.ExtractLevelDomain()
        data = self.har
        title = data['log']['pages'][0]['title']
        this_domain_level2 = domain_filter.parse_url_level(title, level=2)
        third_party_requests = 0
        total_requests = 0
        third_party_body_size = 0
        third_party_content_size = 0
        total_content_size = 0
        first_body_size = 2 + data['log']['entries'][0]['response']['bodySize']
        total_body_size = 0
        for i in range(len(data['log']['entries'])):
            url = data['log']['entries'][i]['request']['url']
            request_domain_level2 = domain_filter.parse_url_level(url, level=2)
            body_size = data['log']['entries'][i]['response']['bodySize']
            content = data['log']['entries'][i]['response']['content']['size']
            total_requests += 1
            total_body_size += 2 + body_size
            total_content_size += 2 + content
            if request_domain_level2 != this_domain_level2:
                third_party_requests += 1
                third_party_body_size += 2 + body_size
                third_party_content_size += 2 + content
        list_feature = [third_party_requests, total_requests, third_party_body_size, third_party_content_size,
                        total_content_size, first_body_size, total_body_size]
        print(list_feature)
        self.feature_list = list_feature

    def start(self):
        self._read_file()
        for domain in enumerate(self.domain_list):
            try:
                # 提取har，并提取特征
                self.temp_domain_str = domain
                self._get_har()
                self._get_feature()
                har_list = self.feature_list
            except BaseException:
                har_list = [0, 0, 0, 0, 0, 0, 0]
            with open(self.save_path, mode='a') as f:
                f.writelines(har_list)
                f.writelines('\n')


if __name__ == "__main__":
    har_crawler = GetHar()
    har_crawler.start()
