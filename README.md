# proxy_scraper

scrapes  "https://free-proxy-list.net/" for proxies and store them in a json, csv, txt for use in projects involved in scraping that may require proxies

pandas was used because it was just a quick way to parse the tables for me

## install libraries

- make sure you have bs4, lxml, pandas libraries for python3 
- you can also run `pip install -r requirements.txt` or if you have pipenv `pipenv install -r requirements.txt` to get the dependencies


## rotation

- rotation built in. It tries to make connection and any proxy that fail to make connections are removed

## running

- i use this in other projects so you can just import the scrape() function from proxy_scrape and it will give you the local files. Example how is shown in test.py. 
- proxy_rotate.py will rotate proxies and headers for the URL you are interested in and give you a bs4 object as return. Import the function and run it the same way  

## Docker 

there is a dockerfile, I still need to test it out
