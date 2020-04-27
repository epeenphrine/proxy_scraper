from proxy_scrape import scrape
from proxy_rotate import proxy_rotate
import time

scrape()
time.sleep(4)
print('scrape ran sleeping for 4s')
proxy_rotate('https://google.com')