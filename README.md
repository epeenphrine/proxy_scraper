# PROXYscraper
scrapes  "https://free-proxy-list.net/" for proxies and store them in a dictionary format for use in other projects
stored in proxydictlist.json

make sure you have bs4, lxml, pandas libraries for python3 

I've configured urllib in a way so that it uses a proxy and it looks like you are using a browser.
The proxies in the list are chosen at random and proxies that fail to make connections are removed. 

to run type in terminal:
python -i proxyscrape.py
proxyscrape()