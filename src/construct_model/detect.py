#encoding:utf-8
import pandas as pd
import os
import re
import tldextract
from typo_checker import TypoChecker
"""
    早期对数据特征进行测试和初步生成的代码
"""

path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
data_dir = os.path.join(path,'data')

domain_df = pd.read_csv(data_dir + '/domain_index_new2.csv', index_col = 0)
# alexa_df = pd.read_csv(data_dir + '/altextop.csv', index_col = 0)
parking_services = ['sedoparking.com', 'namedrive.com', 'parked.com', 'whypark.com',\
                    'astoriacompany.com', 'fabulous.com', 'domainsponsor.com', 'trafficz.com',\
                    'domainhop.com', 'parkingdots.com', 'dotzup.com', 'voodoo.com', 'parkingcrew.com',\
                    'rookmedia.net', 'bodis.com', 'smartname.com', 'parklogic.com', 'domainapps.com', \
                    'trafficz.com', 'dopa.com', 'internettraffic.com', '1and1.com', 'namesilo.com', \
                    'above.com', 'dnsexit.com', 'ztomy.com', 'pql.net', 'airportparkingtucson.com', '1plus.net']

def check_alexa(alexa_df, domain_df):
    alexa_main_domains = alexa_df['main_domain']
    domain_df.loc[domain_df['main_domain'].isin(alexa_df['main_domain']), 'white'] = 1
    print (domain_df.loc[domain_df['white']==1])

def check_dns_record(domain_df):
    assert_1, assert_2,assert_3 = get_dns_parking_domains()
    domain_df.loc[domain_df['main_domain'].isin(assert_1), 'service'] = 1
    domain_df.loc[domain_df['main_domain'].isin(assert_2), 'service'] = 2
    domain_df.loc[domain_df['main_domain'].isin(assert_3), 'service'] = 3
    print (len(domain_df.loc[domain_df['service'] == 1]))
    print(len(domain_df.loc[domain_df['service'] == 2]))
    print(len(domain_df.loc[domain_df['service'] == 3]))

def get_dns_parking_domains():

    assert_1,assert_2,assert_3 = [],[],[]
    with open(data_dir + '/domain300w.txt') as f:
        for line in f.readlines():
            line = line.strip().split(',')
            domain,dtype,content = line[1],line[4],line[5]
            if dtype == 'CNAME' or dtype == 'NS':
                items = content.split(';')
                for item in items:
                    if item in parking_services:
                        t = tldextract.extract(domain)
                        main_domain = t.domain + '.' + t.suffix
                        assert_1.append(main_domain)
                    elif 'park' in item:
                        print (domain, dtype, content)
                        t = tldextract.extract(domain)
                        main_domain = t.domain + '.' + t.suffix
                        assert_2.append(main_domain)
            elif 'park' in domain:
                t = tldextract.extract(domain)
                main_domain = t.domain + '.' + t.suffix
                assert_3.append(main_domain)
    return assert_1, assert_2,assert_3

def check_typo():

    typochecker = TypoChecker()
    main_domains = domain_df['main_domain'].values
    main_domains = list(set(main_domains))
    for i, main_dm in enumerate(main_domains):
        typo_flag = typochecker.is_typo_domain(main_dm)
        print (i, main_dm, typo_flag)
        domain_df.loc[domain_df['main_domain'] == main_dm, 'typo'] = typo_flag
    print (domain_df.loc[domain_df['typo'] == True])
    domain_df.to_csv(data_dir + "/domain_index_new2.csv", index=True)


def check_digit():

    domain_df['digit_flag'] = 0
    main_domains = domain_df['main_domain'].values
    main_domains = list(set(main_domains))
    digit_domains = []
    for i, main_domain in enumerate(main_domains):
        t = tldextract.extract(main_domain)
        domain = str(t.domain)
        if domain.isdigit():
            digit_domains.append(main_domain)
    print (digit_domains)
    #domain_df.loc[domain_df['main_domain'] == main_domain, 'digit'] = digit_flag
    domain_df.loc[domain_df['main_domain'].isin(digit_domains), 'digit_flag'] = 1
    domain_df.to_csv(data_dir + "/domain_index_new2.csv", index=True)


def digit_ratio():

    main_domains = domain_df['main_domain'].values
    main_domains = list(set(main_domains))

    for main_domain in main_domains:
        t = tldextract.extract(main_domain)
        domain = str(t.domain)
        digits = re.sub("\D", "", domain)
        digit_ratio = len(digits) / len(domain)
        print (main_domain, digit_ratio)



if __name__ == '__main__':
    check_dns_record(domain_df)
    check_alexa(alexa_df, domain_df)
    domain_df.to_csv(data_dir+"/domain_index_new1.csv", index=True)
    check_digit()
    digit_ratio()
    check_typo()

    print (len(domain_df.loc[domain_df['typo'] == True]))
    print(len(domain_df.loc[(domain_df['typo'] == True) & (domain_df['white'] == 1)]))
    black1 = domain_df.loc[((domain_df['white'] == -1) & (domain_df['service'] == 1))]['domain'].values.tolist()
    black2 = domain_df.loc[((domain_df['white'] == -1) & (domain_df['service'] == 2))]['domain'].values.tolist()
    # white = domain_df.loc[((domain_df['white'] == 1) & (domain_df['service'] == -1))]['domain'].values.tolist()
    print (len(black1), len(black2))
    explored_domains = []
    explored_domains.extend(list(black1))
    explored_domains.extend(list(black2))
    # explored_domains.extend(list(white))
    explored_domains = list(set(explored_domains))
    print (len(explored_domains))
    domains = domain_df.loc[~domain_df["domain"].isin(explored_domains)]['domain']
    print (len(domains))
    first = len(domains) // 3
    domains1, domains2, domains3 = domains[:first], domains[first:first+first], domains[first+first:]
    with open('domain_1.txt', 'w') as f:
        f.write('\n'.join(domains1))
    with open('domain_2.txt', 'w') as f:
        f.write('\n'.join(domains2))
    with open('domain_3.txt', 'w') as f:
        f.write('\n'.join(domains3))



