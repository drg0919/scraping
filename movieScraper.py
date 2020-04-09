from selenium import webdriver
from bs4 import BeautifulSoup
from pprint import pprint
import time
import requests
import sys

driver = webdriver.Chrome('chromedriver.exe')
driver.minimize_window()
driver.get('https://www.themoviedb.org/')
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')
wraps = soup.select('.wrapper')
recs = []

for wrap in wraps:
    if len(list(wrap.findChildren('a'))):
        rec = wrap.findChildren('a')[0] 
    else :
        continue
    data = {
        'title': rec.get('title'),
        'href': rec.get('href')
    }
    recs.append(data) 

driver.quit()

for rec in recs:
    temp = rec['href'].split('?')
    rec_url = '/watch?'.join(temp)
    res = requests.get(f'https://www.themoviedb.org{rec_url}')
    soup = BeautifulSoup(res.text, 'html.parser')
    final = soup.find('div', {"class": "ott_provider"}).find('a')
    rec.pop('href')
    rec['service'] = final.get('title')
    rec['link'] = final.get('href')
    if len(sys.argv) > 1 and sys.argv[1] == 'f':
        with open("data.txt", mode="a") as res_file:
            res_file.write(str(rec))
            res_file.write("\n")
    else:
        print(rec)