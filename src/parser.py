import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
    

def crawl_urls():
    driver = webdriver.Chrome('/home/sktkddn777/Stack-Lounge/chromedriver.exe')
    url = "https://programmers.co.kr/job?gclid=CjwKCAjwuIWHBhBDEiwACXQYsbfxu6gxVCa6AjaNUN4qb0wpZ2ZIEoNjC9Ur2Nb_mSfHlVUNhd9hBRoC4tMQAvD_BwE&page={}&utm_campaign=job_hiring&utm_medium=cpc&utm_source=google"
    base_urls = "https://programmers.co.kr"
    link_urls = []

    for _pageNum in range(1, 10):
        driver.get(url.format(_pageNum))


        new_url = url.format(_pageNum)
        html = requests.get(new_url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        programmers_urls = soup.select(
            'h5 > a'
        )

        for title in programmers_urls:
            link_urls.append(base_urls + title.get('href'))
    
    crawl_data(link_urls)
        

def crawl_data(links):
    url = links[0]
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    
    heavy_use = soup.find('div', {'id': 'app'})#find_all('div', {'class' : 'content-body'})

 
   #app > div > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 > section.section-stacks > table > tbody > tr > td > code:nth-child(1)
   #app > div > div > div > div.content-body.col-item.col-xs-12.col-sm-12.col-md-12.col-lg-8 > section.section-stacks > table > tbody > tr


if __name__ == '__main__': 
    start_time = time.time()
    crawl_urls()
    print("launching time: %s seconds"%(time.time() - start_time))
