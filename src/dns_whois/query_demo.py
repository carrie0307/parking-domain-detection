from crawl_dns_whois import QueryAgent

agent = QueryAgent()

print(agent.query_dns('google.com'))  # param is FQDN
print(agent.query_whois('www.jd.com')) # param is FQDN
