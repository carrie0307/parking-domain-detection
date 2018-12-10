import multiprocessing
import os
import re
import whois
import tldextract
import json


class QueryAgent(object):
    
    def __init__(self):  
        self.DNS_INFO = "dns_info.txt"
        self.WHOIS_INFO = "whois_info.txt"
        self.domain_names = list()
        self.dns_whois_list = dict()
        self.dns_dict = dict()
        self.whois_dict = dict()
        self.load_info_dict()


    def load_info_dict(self):
        if not os.path.exists(self.DNS_INFO) or not os.path.exists(self.WHOIS_INFO):
            print("Start crawling DNS_INFO and WHOIS_INFO...")
            info_agent = InfoAgent()
            info_agent.start()
        else:
            print("Already exist the DNS_INFO and WHOIS_INFO:)\nStart loading DNS_INFO and WHOIS_INFO")
            self._parse_dns_file()
            self._parse_whois_json()


    def _parse_dns_file(self):
        with open(self.DNS_INFO, mode='r') as f:
            for line in f:
                line = line.strip()
                domain, ns_str, cname_str = line.split(";")
                self.dns_dict[domain] = {
                    "name_server":ns_str.split(","),
                    "cname":cname_str.split(",")
                }

    
    def _parse_whois_json(self):
        with open(self.WHOIS_INFO, mode='r') as f:
            for line in f:
                domain, dict_str = line.strip().split("||")
                d = eval(dict_str)
                self.whois_dict[domain] = d

    
    def query_dns(self, domain):
        """
        API for query dns info
        """
        try:
            return self.dns_dict[domain]
        except KeyError:
            return "Whoops! Not Find :( "


    def query_whois(self, domain):
        """
        API for query whois info
        """
        try:
            return self.whois_dict[domain]
        except KeyError:
            return "Whoops! Not Find :( "



class InfoAgent(object):

    def __init__(self):
        self.domain_file = "filter_domain.txt"
        self.DNS_INFO = "dns_info.txt"
        self.WHOIS_INFO = "whois_info.txt"
        self.domain_names = list()
        self.dns_whois_list = dict()
        self.dns_dict = dict()
        self.whois_dict = dict()


    def _parse_domain_file(self):
        with open(self.domain_file, mode='r') as f:
            for line in f:
                line = line.strip()
                self.domain_names.append(line)
        


    def _parse_ns_value(self, ns_value):
        pattern = re.compile(r'nameserver = (.*)')
        result = pattern.findall(ns_value.read())
        return result


    def _parse_cname_value(self, cname_value):
        pattern = re.compile(r'canonical name = (.*)')
        result = pattern.findall(cname_value.read())
        return result


    def _get_dns(self, domain):
        commands = {
            "ns":"nslookup -query=ns {}".format(domain),
            "cname":"nslookup -query=cname {}".format(domain)
        }
        ns_return = os.popen(commands['ns'])
        cname_return = os.popen(commands['cname'])
        ns_list = self._parse_ns_value(ns_return)
        cname_list = self._parse_cname_value(cname_return)
        return {"ns_list":ns_list, "cname_list":cname_list}


    def _get_whois(self, domain):
        try:
            ext = tldextract.extract(domain)
            query_domain = ".".join([ext.domain, ext.suffix])
            # whois_info = whois.query(query_domain)
            whois_info = whois.whois(query_domain)
            return whois_info
        except Exception:
            return None


    def _get_dns_whois_list(self):
        for i, domain in enumerate(self.domain_names):
            print("[ {} | {} ] [ domain : {} ]".format(i+1, len(self.domain_names), domain))
            dns = self._get_dns(domain) # dns is dict
            Domain_Obj = self._get_whois(domain) # whois is Domain Object
            whois_info=dict()
            if Domain_Obj:
                # whois_info['name'] = Domain_Obj.name
                # whois_info['registrar'] = Domain_Obj.registrar
                # whois_info['creation_date'] = str(Domain_Obj.creation_date)
                # whois_info['expiration_date'] = str(Domain_Obj.expiration_date)
                # whois_info['last_updated'] = str(Domain_Obj.last_updated)
                # whois_info['name_servers'] = ",".join(Domain_Obj.name_servers)
                whois_info['name'] = Domain_Obj.domain_name[-1] if isinstance(Domain_Obj.domain_name, list) else Domain_Obj.domain_name
                whois_info['registrar'] = Domain_Obj.registrar
                whois_info['creation_date'] = str(Domain_Obj.creation_date)
                whois_info['expiration_date'] = str(Domain_Obj.expiration_date)
                whois_info['last_updated'] = str(Domain_Obj.last_updated)
                whois_info['name_servers'] = ",".join(Domain_Obj.name_servers) if Domain_Obj.name_servers else None
            else:
                whois_info['name'] = domain
                whois_info['info'] = None
            self.dns_whois_list[domain] = {"dns":dns,"whois":whois_info}
            self._save_dns_whois()
        

    def _save_dns_whois(self):
        whois_dict = dict()
        with open(self.DNS_INFO, mode="a") as f:
            for domain, dns_whois_dict in self.dns_whois_list.items():
                ns_str = ",".join(dns_whois_dict["dns"]["ns_list"])
                cname_str = ",".join(dns_whois_dict["dns"]["cname_list"])
                line = ";".join([domain, ns_str, cname_str])
                f.write("{}\n".format(line))

                whois_dict[domain] = dns_whois_dict["whois"]
            
        
        with open(self.WHOIS_INFO, mode='a',encoding='utf8') as f:
            for domain, d in whois_dict.items():
                f.write("{}||{}\n".format(domain, d))
        
        self.dns_whois_list = dict()

           

    def start(self):
        self._parse_domain_file()
        self._get_dns_whois_list()
    


if __name__ == "__main__":
    agent = InfoAgent()
    agent.start()
