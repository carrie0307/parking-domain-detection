import scrapy
from crawler.items import CrawlerItem
import os
import time
import sys

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

domain_file = "C:/Users/Lorwin/Desktop/crawler/crawler/new_domain_3.txt"
exception_file = "C:/Users/Lorwin/Desktop/crawler/crawler/exception.txt"
save_dir = "C:/Users/Lorwin/Desktop/crawler/crawler/saved_source/"


if not os.path.exists(save_dir):
    os.mkdir(save_dir)


class DmozSpider(scrapy.Spider):
    name = "kuan"
    allowed_domains = []

    def __init__(self, file=None,*args,**kwargs):
        super(DmozSpider, self).__init__(*args, **kwargs)
        self.crawl_file = file
        self.domain_list = list()


    def start_requests(self):
        self.load_domain_file()
        for index, url in enumerate(self.domain_list):
            url = "http://" + url
            try:
                # time.sleep(3)
                sys.stdout.write("{} / {} | url: {}\n".format(index, self.domain_list.__len__(), url))
                # print(url)
                # yield scrapy.Request(url=url,callback=self.parse_homepage,meta={'page':i},errback=self.errback_httpbin)
                yield scrapy.Request(url=url,callback=self.parse_homepage, meta={'url':url}, errback=self.errback_httpbin)
            except:
                print('!!!!!ERROR:{}\n'.format(url))
                with open(exception_file, mode="a") as f:
                    f.write("{}\n".format(url))


    def load_domain_file(self):
        with open(domain_file, mode="r") as f:
            for line in f:
                line = line.strip()
                self.domain_list.append(line)

    def parse_homepage(self,response):
        path_to_file = os.path.join(save_dir, response.meta['url'][7:]+".txt")
        # print(response.body)
        with open(path_to_file, mode="wb") as f:
            f.write(response.body)
        # for i in range(1,21):
        #     page = response.meta['page']
        #     # app_id = response.xpath('//*[@id="all-applist"]/li['+ str(i) +']/a/@href').extract_first()
        #     app_id = response.xpath('//*[@id="game_left"]/div/a['+ str(i) +']/@href').extract_first()
        #     domain = 'https://www.coolapk.com'
        #     link = domain + app_id
        #     info = 'Page:'+str(page)+' '+str(i)+'th '+app_id
        #     try:
        #         time.sleep(3)
        #         yield scrapy.Request(url=link,callback=self.parse_html,meta={'info':info},errback=self.errback_httpbin)
        #     except:
        #         print('Crawl',link,'error')
            

    # def parse_html(self,response):

    #     info = response.meta['info']

    #     print('-----',info,'-----')
        
    #     labels = response.xpath('/html/body/div/div[2]/div[2]/div[2]/div/div[5]/p[2]/a/@href').extract()

    #     name = response.xpath('/html/body/div/div[2]/div[2]/div[1]/div/div/div[1]/p[1]/text()').extract_first()

        
    #     down_link = response.xpath('/html/body/div/div[2]/div[2]/div[1]/div/div/div[1]/a/@href').extract_first()
        
    #     apk_name = response.xpath('/html/body/div/div[2]/div[2]/div[2]/div/div[6]/p[2]/text()').extract_first()
        

    #     item = CrawlerItem()

    #     item['label'] = labels
    #     item['name'] = name
    #     item['down_link'] = down_link
    #     item['apk_name'] = apk_name.replace('应用包名：','')

    #     yield item

    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)