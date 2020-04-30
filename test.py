#%%
import time
import urllib
import random
import bs4 as bs 
import pandas as pd 
import json


## settings for making requests avoiding blacklist

url = 'https://socks-proxy.net'
headers_list = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

#pick random proxy and header

headers_pick = random.choice(headers_list)
                
## configuring urllib for use with proxies

## requests
req = urllib.request.Request(url, headers={'User-Agent' : f"{headers_pick}"})
res = urllib.request.urlopen(req, timeout=5).read()

df = pd.read_html(res)
df = df[0]
print(df)
# %%

# selecting columns and converting to list
proxy_address= df['IP Address'].to_list()
proxy_port= df['Port'].to_list()
proxy_https = df['Https'].to_list()
proxy_version = df['Version'].to_list()


# %%

with open('proxydictlist.json') as f:
    proxy_dict_list = json.load(f)

proxy_list = [

]

#processing
for address, port, https, version in zip(proxy_address,proxy_port, proxy_https, proxy_version):
    if https == 'Yes' and address:

        proxy_dict_construction = {
            f"https": f"https://{address}:{str(port).replace('.0', '')}"
        }
        proxy_non_dict_construction = f"https://{address}:{str(port).replace('.0','')}"

        if proxy_dict_construction not in proxy_dict_list:  
            proxy_dict_list.append(proxy_dict_construction)
            proxy_list.append(proxy_non_dict_construction) 

with open('proxydictlist.json', 'w') as f:
    json.dump(proxy_dict_list, f)
with open('proxylist.csv')
#print(proxy_dict_list)
#print(len(proxy_dict_list))

