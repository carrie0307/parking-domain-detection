import urllib.request
import pandas as pd
import os
import logging
import queue
import time
import threading
path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
data_dir = os.path.join(path,'data')
domain_df = pd.read_csv(data_dir + '/domain_index_new1.csv', index_col = 0)
domains = domain_df.loc[domain_df['service'] == 2]['domain'].values
domain_q = queue.Queue()
res_q = queue.Queue()
for domain in domains:
    domain_q.put(domain)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename="record.log",
                    filemode='a+')


# for i,domain in enumerate(domains):
#     try:
#         f = urllib.request.urlopen('http://' + domain)
#         result = f.read().decode('utf-8')
#         http_code = f.code
#         print (i, domain, http_code)
#         with open(data_dir + '/source_code/' + domain + '.txt', 'w') as f:
#             f.write(result)
#     except:
#         print (i, domain, '-1')


def get_resp():

    while not domain_q.empty():
        domain = domain_q.get()
        try:
            f = urllib.request.urlopen('http://' + domain)
            result = f.read().decode('utf-8')
            http_code = f.code
            print ("source code: ", domain, http_code)
            res_q.put((domain, result))
        except:
            print ("source code: ", domain, '-1')

def write_html2file():

    string = ''
    while True:
        domain, res = res_q.get(timeout=100)
        try:
            print ("save: ", domain)
            with open(data_dir + '/source_code/' + domain + '.txt', 'w', encoding='utf-8') as f:
                f.write(res)
        except Exception as err:
            logging.info("exception    ", domain)


if __name__ == '__main__':

    thread_num = 10
    get_resp_td = []
    for _ in range(thread_num):
        get_resp_td.append(threading.Thread(target=get_resp))
    print ('开始获取权威source code...')
    for td in get_resp_td:
        td.start()
    time.sleep(5)
    save_td = threading.Thread(target=write_html2file)
    save_td.start()
    save_td.join()