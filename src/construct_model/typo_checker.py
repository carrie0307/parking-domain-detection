#!/usr/bin/env python

"""
    From https://github.com/kdsec/Domain-Parking-Sensors/blob/master/includes/typo_checker.py
    根据论文，newdomain是一个潜在的typodomain，它所属的typo类型进行还原操作，
    如果得到比它Alexa排名高的域名authoritive domain，则认为newtdomain可能是authoritive domain的一个typo
"""

import os
import tldextract
import pandas as pd
import os
path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
print (path)
data_dir = os.path.join(path,'data')

def get_alexaTop():
    # alexa_df = pd.read_csv(data_dir + '/alexatop.csv', index_col=0)
    alexa_df = pd.read_csv('./alexatop.csv', index_col=0)
    ranks = alexa_df.index
    domains = alexa_df.domain
    entries = []
    for rank,domain in zip(ranks, domains):
        entries.append((rank, domain))
    return entries




class TypoChecker:
    def __init__(self):
        self.f_fingers = {}
        self.top_1m_dict = {}

        # Read in the qwerty maps
        # f = open(os.path.join(os.path.dirname(__file__), 'qwerty.map'))
        f = open('qwerty.map')
        for line in f:
            line = line.strip()
            parts = line.split(" ")
            self.f_fingers[parts[0]] = parts[1]
        f.close()
        # print ("self.f_fingers: ", self.f_fingers)
        entries = get_alexaTop()
        for entry in entries:
            self.top_1m_dict[entry[1]] = entry[0]
        # Alexa文件里面没有google
        self.top_1m_dict['google.com'] = 0
        # print (self.top_1m_dict)

    def cleanup_domain(self, domain):
        parts = tldextract.extract(domain.strip())
        return (parts.domain, '.' + parts.suffix)

    def generate_ts_domains(self, domain):
        ts_domains = {}

        # google.com -> ['google', '.com']
        cl_domain = self.cleanup_domain(str(domain))
        # print ("cl_domain: ", cl_domain)
        f_clean_domain = cl_domain[0] + cl_domain[1]
        # print ("f_clean_domain: ", f_clean_domain)

        ts_domains[f_clean_domain] = {}

        cld_len = len(cl_domain[0])
        if cld_len < 6:
            # We do not account for domains with 5 characters or less
            return ts_domains

        # Model 1: Character substitution, fat finger one
        ts_domains[f_clean_domain]["c_subs"] = []
        # print 'f_clean_domain:', f_clean_domain
        for i in range(0, cld_len):
            # 把cl_domain[0]的第i个字符替换为map中该字符对应的字符
            # ts_characters = self.f_fingers[cl_domain[0][i]]
            # for c in ts_characters:
            for c in 'abcdefghijklmnopqrstuvwxyz0123456789':
                ts_domains[f_clean_domain]["c_subs"].append(
                    "%s%c%s%s" % (cl_domain[0][0:i], c, cl_domain[0][i + 1:], cl_domain[1]))
                # print ("domain: ", "%s%c%s%s" % (cl_domain[0][0:i], c, cl_domain[0][i + 1:], cl_domain[1]))
        # print("c_subs:", ts_domains)

        # Model 2: Missing dot typos:
        # Changed to www detection for reversing
        ts_domains[f_clean_domain]["c_mdot"] = []
        if 'www' in f_clean_domain:
            ts_domains[f_clean_domain]["c_mdot"].append(f_clean_domain.replace('www', ''))
        if 'www-' in f_clean_domain:
            ts_domains[f_clean_domain]["c_mdot"].append(f_clean_domain.replace('www-', ''))
        # print ("c_mdot:", ts_domains)

        # Model 3: Character omission
        # Dropped for reversing
        # ts_domains[f_clean_domain]["c_omm"] = []
        # for i in range(0, cld_len):
        #   ts_domains[f_clean_domain]["c_omm"].append(f_clean_domain[:i]+ f_clean_domain[i + 1:])

        # Model 4: Character permutation(调换位置)
        ts_domains[f_clean_domain]["c_perm"] = []
        for i in range(0, cld_len - 1):
            ts_domains[f_clean_domain]["c_perm"].append(
                f_clean_domain[:i] + f_clean_domain[i + 1] + f_clean_domain[i] + f_clean_domain[i + 2:])

        # Model 5: Character duplication
        # Changed to deduplicate
        ts_domains[f_clean_domain]["c_dupl"] = []
        for i in range(0, cld_len - 1):
            if f_clean_domain[i] == f_clean_domain[i + 1]:
                ts_domains[f_clean_domain]["c_dupl"].append(f_clean_domain[:i] + f_clean_domain[i + 1:])

                # Model 6: Changing TLD
        # Introduced for reversing
        ts_domains[f_clean_domain]["c_tld"] = []
        # Cancelled out due too many false positives
        popular_tlds = []  # popular_tlds = ['.com','.net','.org', '.co.uk','.info','.us']
        for tld in popular_tlds:
            if tld != cl_domain[1]:
                ts_domains[f_clean_domain]["c_tld"].append(cl_domain[0] + tld)

        return ts_domains[f_clean_domain]

    def is_typo_domain(self, newdomain):

        reverse_typo_set = set()
        # newdomain是一个潜在的typo(即可能是某个AlexaTop域名的typop),
        # 通过对它进行还原，如果能得到排名更高的域名，则认为它的确是某个AlexaTop域名的typo
        models = self.generate_ts_domains(newdomain)
        for kind in models:
            for domain in models[kind]:
                reverse_typo_set.add(domain)
        # print ("reverse_domains: ", reverse_typo_set)
        u = set.intersection(reverse_typo_set, self.top_1m_dict)
        typolist = []
        for match in u:
            # Check if original typo also is in Alexa to 1m
            if newdomain in self.top_1m_dict.keys():
                # Check if original typo has lower (=bigger number) Alexa rank as claimed autoritative domain
                if self.top_1m_dict[match] < self.top_1m_dict[newdomain]:
                    typolist.append(match)
            else:
                # Original typo domain was not in Alexa top 1m => just add it
                typolist.append(match)
        if len(typolist) > 0:
            return True
        else:
            return False



if __name__ == '__main__':
    # entries = get_alexaTop()
    typochecker = TypoChecker()
    flag = typochecker.is_typo_domain("m.flycua.com")
    if flag:
        print ("True")
    else:
        print ("False")


