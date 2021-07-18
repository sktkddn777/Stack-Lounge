import requests
import json
import re
from selenium import webdriver
from bs4 import BeautifulSoup

from name1 import txt_to_lst

from multiprocessing import Process, Semaphore
from pathos.multiprocessing import ProcessingPool as Pool #pip install pathos



def setting_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    return driver

def txt_to_dic():
    stack_dict = {}
    with open("tech_stack.txt") as f:
        for line in f:
            line = line.replace("\n","")
            stack_dict[line] = []

    return stack_dict


def get_cop_data(id, links, sem):
    driver = setting_driver()
    korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
    for link in links:
        # driver.implicitly_wait(5)
        driver.get(link)
        
        try:
            cop_name = driver.find_element_by_class_name("sub-title").text
            code_data = driver.find_element_by_class_name("heavy-use").find_elements_by_tag_name("code")
            requirement = driver.find_element_by_id("job-position-requirement-view-section")
            preference = driver.find_element_by_id("job-position-preferredExperience-view-section")
        except:
            continue
        
        sem.acquire()
        list_code = code_data.split()
        
        list_requirement = re.sub(korean, '', requirement.text).split()
        list_preference = re.sub(korean, '', preference.text).split()
        
        list_data = list_requirement + list_preference + list_code
        for data in list_data:
            if data in stack_dict:
                if cop_name not in stack_dict[data] or cop_name != "":
                    stack_dict[data].append(cop_name)
        sem.release()
    return True


def makeJson():
    with open('cop_by_tech.json','w',encoding="utf-8") as make_file:
        json.dump(stack_dict, make_file,  ensure_ascii=False, indent='\t')



if __name__ == '__main__': 
    stack_dict = txt_to_dic()
    urls_lst = txt_to_lst()

    sem = Semaphore()

    th1 = Process(target=get_cop_data, args=(1, urls_lst, sem))
   # th2 = Process(target=get_cop_data, args=(2, urls_lst, sem))

    th1.start()
    #th2.start()
    
    th1.join()
   # th2.join()

    makeJson()

