import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from multiprocessing import Process, Semaphore
    


def crawl_urls():
    base_url = "https://programmers.co.kr"
    link_urls = []
    _pageNum = 1
    while True:
        # 프로그래머스 url
        url = "https://programmers.co.kr/job?page={}&utm_campaign=job_hiring&utm_medium=cpc&utm_source=google"
        url = url.format(_pageNum)
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        
        cop_link = soup.select(
            'h5 > a'
        )
        for link in cop_link:
            link_urls.append(base_url + link.get('href'))


        if len(soup.select('nav > ul > li.next.next_page.disabled.page-item')) > 0:
            break
        _pageNum += 1
    
    make_link_txt(link_urls)
    
    # while True:
    #     driver.get(url.format(_pageNum))
    #     driver.implicitly_wait(3)
    #     url_data = driver.find_elements_by_class_name('position-title')
    #     for data in url_data:
    #         link_urls.append(data.find_element_by_tag_name("a").get_attribute("href"))

    #     try:
    #         driver.find_element_by_class_name('next.next_page.disabled.page-item')
    #         break
    #     except:
    #         _pageNum += 1
    #         continue

    # get_stack_data(link_urls)
        



def get_stack_data(id, links, sem):
    global frequency_dict

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    code_data = []

    for link in links:
        # driver.implicitly_wait(5)
        if(link[:5] == "https"):
            driver.get(link)

        try:
            use_data = driver.find_element_by_class_name("heavy-use")
            code_data.append(use_data.find_elements_by_tag_name("code"))
        except:
       
            continue
# use single thread when global variable occurs 
# another use multiprocessing
    
    
    sem.acquire()
    for data in code_data:
        for d in data:
            print(d.text)
            frequency_dict[d.text] = 1 if data.text not in frequency_dict else frequency_dict[data.text] + 1
    
    sorted_frequency_dict = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
    tech_stack = sorted_frequency_dict[:100]

    sem.release()

    make_tech_txt(tech_stack)


def make_tech_txt(tech_stack):
    tech_name = []
    for name in tech_stack:
        tech_name.append(name[0])
    with open('tech_stack.txt', 'w') as f:
        f.write('\n'.join(tech_name))


def make_link_txt(tech_links):
    with open('tech_links.txt', 'w') as f:
        f.write('\n'.join(tech_links))


def txt_to_lst():
    urls_list = []
    with open("tech_links.txt") as f:
        for line in f:
            line = line.replace("\n","")
            urls_list.append(line)

    return urls_list



if __name__ == '__main__': 
    frequency_dict = {}
    #crawl_urls()
    urls_lst = txt_to_lst()

    sem = Semaphore()
    
    th1 = Process(target=get_stack_data, args=(1, urls_lst, sem))
    th2 = Process(target=get_stack_data, args=(2, urls_lst, sem))

    th1.start()
    th2.start()

    th1.join()
    th2.join()


    
