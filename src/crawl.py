import requests
import json
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from name1 import txt_to_lst
from multiprocessing import Process, Semaphore


class Crawl:
    def __init__(self, url, detailed_url):
        self.url = url
        self.detailed_url = detailed_url
        self.url_list = []
        self.stack_dict = {}
        self.cop_dict = {}

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=self.options)
        self.sem = Semaphore()

    def crawl_urls(self):
        _pageNum = 1
    
        while True:
            copy_url = self.detailed_url
            # 프로그래머스 url 다른 url은 다른 url별로 함수 만들기
            copy_url = copy_url.format(_pageNum)
            html = requests.get(copy_url).text
            soup = BeautifulSoup(html, 'html.parser')

            cop_link = soup.select(
                'h5 > a'
            )
            for link in cop_link:
                self.url_list.append(self.url + link.get('href'))

            if len(soup.select('nav > ul > li.next.next_page.disabled.page-item')) > 0:
                break
            _pageNum += 1

        with open('tech_links.txt', 'w') as f:
            f.write('\n'.join(self.url_list))

    
    def make_tech_stack(self):
        for link in self.url_list:
            if (link[:5] == "https"):
                self.driver.get(link)
            try:
                use_data = self.driver.find_element_by_class_name("heavy-use")
                code_data = use_data.find_elements_by_tag_name("code")
                self.sem.acquire()
                for data in code_data:
                    self.stack_dict[data.text] = 1 if data.text not in self.stack_dict else self.stack_dict[data.text] + 1
                self.sem.release()
            except:
                continue
    
        self.stack_dict = sorted(self.stack_dict.items(), key=lambda x: x[1], reverse=True)
        self.stack_dict = self.stack_dict[:100]

        tech_name = []
        for name in self.stack_dict:
            tech_name.append(name[0])
        
        with open('tech_stack.txt', 'w') as f:
            f.write('\n'.join(tech_name))


    def txt_to_dic(self):
        with open("tech_stack.txt") as f:
            for line in f:
                line = line.replace("\n","")
                self.cop_dict[line] = []


    def get_cop_data(self):
        korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
        characters = "/()?%,#"

        for link in self.url_list:
            # driver.implicitly_wait(5)
            if (link[:5] == "https"):
                self.driver.get(link)
            try:
                cop_name = self.driver.find_element_by_class_name("sub-title").text
                code_data = self.driver.find_element_by_class_name("heavy-use").find_elements_by_tag_name("code")
                requirement = self.driver.find_element_by_id("job-position-requirement-view-section").text
                preference = self.driver.find_element_by_id("job-position-preferredExperience-view-section").text
            except:
                continue
            
            self.sem.acquire()
            
            requirement = ''.join(x for x in requirement if x not in characters)
            preference = ''.join(x for x in preference if x not in characters)

            list_requirement = re.sub(korean, '', requirement).split()
            list_preference = re.sub(korean, '', preference).split()

            list_data = list_requirement + list_preference

            for data in code_data:
                list_data.append(data.text)
            
            list_data = list(set(list_data)) # 중복 제거

            for data in list_data:
                if data in self.cop_dict:
                    if cop_name not in self.cop_dict[data] and cop_name != '':
                        self.cop_dict[data].append(cop_name)
            self.sem.release()

        with open('cop_by_tech.json', 'w', encoding="utf-8") as make_file:
            json.dump(self.cop_dict, make_file, ensure_ascii=False, indent='\t')


if __name__ == '__main__': 

    url = ["https://programmers.co.kr"]
    detailed_url = ["https://programmers.co.kr/job?page={}&utm_campaign=job_hiring&utm_medium=cpc&utm_source=google"]
    
    programmers = Crawl(url[0], detailed_url[0]) # 사이트별 홈페이지와 데이터를 따오기 위한 url을 삽입
    programmers.crawl_urls() # url_list를 url링크들로 채워준다.
    programmers.make_tech_stack()
    programmers.txt_to_dic()
    th1 = Process(target=programmers.get_cop_data())
    th1.start()
    th1.join()



# def setting_driver():
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)

#     return driver

# def txt_to_dic():
#     stack_dict = {}
#     with open("tech_stack.txt") as f:
#         for line in f:
#             line = line.replace("\n","")
#             stack_dict[line] = []

#     return stack_dict


# def get_cop_data(id, links, sem, stack_dict):
#     driver = setting_driver()
#     characters = "/()?%,#"
#     korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')

#     for link in links:
#         # driver.implicitly_wait(5)
#         driver.get(link)
        
#         try:
#             cop_name = driver.find_element_by_class_name("sub-title").text
#             code_data = driver.find_element_by_class_name("heavy-use").find_elements_by_tag_name("code")
#             requirement = driver.find_element_by_id("job-position-requirement-view-section").text
#             preference = driver.find_element_by_id("job-position-preferredExperience-view-section").text
#         except:
#             continue
        
#         sem.acquire()
        
#         requirement = ''.join(x for x in requirement if x not in characters)
#         preference = ''.join(x for x in preference if x not in characters)

#         list_requirement = re.sub(korean, '', requirement).split()
#         list_preference = re.sub(korean, '', preference).split()
#         list_data = list_requirement + list_preference
#         for data in code_data:
#             list_data.append(data.text)
        
#         list_data = list(set(list_data))
#         for data in list_data:
#             if data in stack_dict:
#                 if cop_name not in stack_dict[data] and cop_name != '':
#                     stack_dict[data].append(cop_name)
                    
                    
#         sem.release()

#     makeJson(stack_dict)


# def makeJson(stack_dict):
#     with open('cop_by_tech.json','w',encoding="utf-8") as make_file:
#         json.dump(stack_dict, make_file,  ensure_ascii=False, indent='\t')



# if __name__ == '__main__': 
#     stack_dict = txt_to_dic()
#     urls_lst = txt_to_lst()

#     sem = Semaphore()

#     th1 = Process(target=get_cop_data, args=(1, urls_lst, sem, stack_dict))
#     th1.start()
#     th1.join()

