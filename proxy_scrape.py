import urllib.request
import bs4 as bs
import pandas as pd
import json
import random
import os
import time



## getting the site
def scrape():
    ## json file check
    def json_load():
        with open("proxydictlist.json") as f:
            print("json file exists")
            time.sleep(1)
            proxies_list = json.load(f)
            return proxies_list

    def json_create():
        with open("proxydictlist.json", "w") as f:
            json.dump([], f)
            time.sleep(1)
            return

    if os.path.exists("proxydictlist.json"):
        proxies_list = json_load()
    else:
        print("json file doesn't exist creating json file ...")
        json_create()
        proxies_list = json_load()

    url = "https://free-proxy-list.net/" ## site containing the proxy.
    print(f"attempting to connect to: {url}")
    print(len(proxies_list))

    headers_list = [
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
        'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
    ]

    if proxies_list: ## check if proxies_list is empty or not
        for i in range(0, len(proxies_list)):
            try:
                #pick random proxy and header
                proxy_pick = random.choice(proxies_list)
                headers_pick = random.choice(headers_list)
                
                ## configuring urllib for use with proxies
                proxy_support = urllib.request.ProxyHandler(proxy_pick)
                opener = urllib.request.build_opener(proxy_support)
                urllib.request.install_opener(opener)

                ## requests
                req = urllib.request.Request(url, headers={'User-Agent' : f"{headers_pick}"})
                sauce = urllib.request.urlopen(req, timeout=5).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                print(soup)
                ## break when soup object obtained
                break
            except:
                ## proxies that do not work are removed from the list
                print(f"{proxy_pick} did not work")
                proxies_list.remove(proxy_pick)
                print(f"{proxy_pick} removed")
                print(len(proxies_list))
   
    ## if proxies_list is empty, proxies are retrieved from the site without using proxies
    else:
        req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
        sauce = urllib.request.urlopen(req).read()
        soup=bs.BeautifulSoup(sauce, 'lxml')
        print(soup)

    ## use pandas to get tables and choose columns
    df = pd.read_html(sauce)

    ##print(df, len(df))
    ##df = df[0]  ## df is a list of tables. We want first table.

    ##df.to_csv("proxyraw.csv", index=True) ## saving df to csv

    ## print(df[0].columns) ## choosing dataframe with the index 0 and checking all the columns. You may need to check columns if name of column have weird spacing and etc.
    df = df[0] ## setting df as the df[0] the data frame with the ip, port, and etc.


    ##df = pd.read_csv("proxyraw.csv")
    df = df[['IP Address', "Port", "Https"]]  ## making df only show the columns we want to see.
    df = df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False) ## dropping all rows with missing values
    return proxy_info(df)

#convert columns to list
def proxy_info(df):
    
    proxy_port = df['Port'].tolist()        ## column "Port" to list
    proxy_ip = df["IP Address"].tolist()    ## column "IP Address" to list
    https = df['Https'].tolist()           ## column "Https" to list
    https_list = []                            #3 empty list to make new list for "https" , "http"

    for item in https: ## convert https list with rows 'yes', 'no' to 'https', 'http' respectively and store them in https_list variable
        if item == "yes":
            #print (item)
            https_list.append("https://")  ## i write it like this because I'm going to concat all three components later. Right now it should print "'https':https://"
        else:
            #print(item)
            https_list.append("http://")
    print(proxy_port, proxy_ip, https)
    return proxy_construct(proxy_port, proxy_ip, https_list)    ## this will start the next function and feed it the arguments proxy_port, ProxyIP, https_list

# putting the strings together 
def proxy_construct(proxy_port, proxy_ip, https_list):

    string = ":"
    proxy_port = [string + str(int(proxy)) for proxy in proxy_port] ## concat ":" at the start of each element in the list proxy_port
    ##print(https_list)
    ##print(proxy_port)

    proxy_list = []
    for i in range(0, len(proxy_port)):      ## using for loop starting from 0 to size of proxy_port list. Doesn't matter which list you use. They should all be the same size
        PROXY = https_list[i] + proxy_ip[i] + proxy_port[i]
        proxy_list.append(PROXY)
        print(PROXY)
    return proxy_dict(https_list, proxy_list)

# making dictionaries using constructed strings 
def proxy_dict(https_list, proxy_list):
    proxy_dict_list = []
    for i in range(0, len(https_list)):
        if https_list[i] == "https://":
            proxies_dict = {"https": proxy_list[i]}
            proxy_dict_list.append(proxies_dict)
        if https_list[i] == "http://":
            proxies_dict = {"http": proxy_list[i]}
            proxy_dict_list.append(proxies_dict)
            
    return save_file(proxy_dict_list, https_list, proxy_list)

## save to local .csv .json .txt etc
def save_file(proxy_dict_list, https_list, proxy_list):
    with open('proxydictlist.json', 'w') as f:
        json.dump(proxy_dict_list, f)
    with open ("proxylist.json", "w") as f:
        json.dump(proxy_list, f)
    proxy_list1 = pd.DataFrame(proxy_list)
    proxy_list1.to_csv("proxylist.csv", index=False)
    new = []
    for proxy in proxy_list:
        new.append(proxy + "\n")
    f = open("proxylist.txt", "w")
    f.writelines(new) 
    f.close()
    print("******************************************************")
    print(proxy_dict_list)
    print("******************************************************")
    print("scrape completed !")

