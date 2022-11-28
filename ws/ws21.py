from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
from parsel import Selector

import io 
import csv 
import json 
import requests 
from bs4 import BeautifulSoup
import time 
import urllib.parse 
import time 
from tqdm import tqdm
import pickle 
import re
import openpyxl
import os


STARTUP_DELAY = 2
NEXT_PAGE_DELAY= 2
WAIT_AFTER_ELEMENTS_LOADED = 1
DELAY_TO_CHECK_IF_NEW_ELEMENT_IS_VISIBLE = 1
LOAD_SPECIFIC_RESULT_DELAY = 2
BACK_TO_MAIN_LIST_DELAY= 1

STOP_EXECUTION_AFTER = 50

data = []

csv_file = 'hotels.csv'
csv_columns = ['name','addr1','addr2','phone','web','loc','aux']


with open('data.csv', 'w') as data_file, open('output.csv', 'w') as output_file:
   pass 
# print("Empty data File Created Successfully")


# csv_columns = ['name']
# map_query = 'https://www.google.com/maps/search/hotels+near+Riyadh+Saudi+Arabia/'
map_query = 'https://www.google.com/maps/search/hotels+in+gurgaon/@28.4511895,76.8989557,11z/data=!3m1!4b1'
# map_query = 'https://www.google.com/maps/search/atm+in+sadulpur/@28.6392666,75.3604669,14z/data=!4m2!2m1!6e2'

def clean_panel(ugly_text_blob):
    text_blob = ugly_text_blob.splitlines()
    addr = []
    website = ''
    phone = ''
    location = ''
    aux_unknown = ''
    for line in range(len(text_blob)):
        if line <= 1:
            addr.append(text_blob[line])
        elif line >= 2:
            if 'closed' in text_blob[line].lower() or 'open' in text_blob[line].lower() or 'claim this' in text_blob[line].lower():
                aux_unknown = ''    
            else:
                if text_blob[line].startswith('+966') or text_blob[line].startswith('966'):
                    phone = text_blob[line]
                elif '+' in text_blob[line] and (re.search('[a-zA-Z]', text_blob[line]) != None):
                    location = text_blob[line]
                else:
                    website = text_blob[line]


    print('Details: ')
    for address in addr:
        print(f'Address: {address[0:5]}...')
    print(f'Phone: {phone}')
    print(f'Location: {location}')
    print(f'Website: {website}')
    print(f'Aux: {aux_unknown}')
    print('---------------------')
    
    # cleaned_block = {'addr1':addr[0], 'addr2':addr[1] if len(addr) > 1 else '', 'phone': phone, 'location': location, 'website': website, 'aux': aux_unknown}
    cleaned_block = {'addr1':addr[0], 'addr2':addr[1] if len(addr) > 1 else '', 'phone': phone, 'location': location, 'website': website, 'aux': aux_unknown}
    return cleaned_block


def google_map_extractor(driver, uri):
    #load up the page
    driver.get(uri)

    more_pages = True

    master_hotel_array = []
    ctr = 0


    while more_pages:
        time.sleep(NEXT_PAGE_DELAY)

        html = driver.page_source

        divs = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a')))

        soup = BeautifulSoup(html, 'html.parser')
        
        
        response = Selector(html)
        # entries=response.xpath('//div[contains(@aria-label, "Results for hotels in gurgaon")]/div/div[./a]')

        time.sleep(WAIT_AFTER_ELEMENTS_LOADED)
 

        # result_list = soup.find_all('div', attrs={'class': 'm6QErb DxyBCb kA9KIf dS8AEf ecceSd'})
        result_list = response.xpath('//div[contains(@aria-label, "Results for hotels in gurgaon")]/div/div[./a]')

        # result_scroll_panel = driver.find_element(By.CSS_SELECTOR, "div[class^='m6QErb DxyBCb kA9KIf dS8AEf ecceSd']")
        result_scroll_panel = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Results for hotels in gurgaon')]")

        total_results = len(result_list)
        
        

        

        

    # x = 0
    # while x < total_results:   
        i = 1
        

        for result_val in result_list:
            print(f"Number of results found in this page: {total_results} and iteration is {i}")    
            
                
            # print(f"\t {result_val['data-result-index']} ({result_val['area-label']})")
            name = result_val.xpath('./a/@aria-label').extract_first()
            link = result_val.xpath('./a/@href').extract_first()
            # name = result_val['area-label']
            # print('---------------------\n')
            print(name)
            # print('---------------------\n')

            with open('data.csv', 'a') as fd:
                fd.write(f'\n{link}')
                # if (i == 122):
                #     more_pages = False

           

            


            # if name not in data:
            #     data.append(name)
            #     print(data)
            # break

            try:

                this_result_div = driver.find_element(By.XPATH, "//div[@aria-label='"+name+"']")

                driver.execute_script("arguments[0].scrollIntoView();", this_result_div)

                i = i + 1 

            except NoSuchElementException:
                print('no data found for '+name)
                pass

            


        # if x == total_results:
        #     total_results =  total_results - x
        #     print(f"Number of results found in this page: {total_results}")

        # x=x+1
        
        # print(this_result_div)
            
        


        

        # ActionChains(driver).click(this_result_div).perform()

        # time.sleep(LOAD_SPECIFIC_RESULT_DELAY)

        # back_btn = driver.find_element(By.XPATH, "//button[@class='hYBOP FeXq4d']")

        # this_hotel_html = driver.page_source

        # this_hotel_info_panel = driver.find_element(By.XPATH, "//div[@aria-label='"+name+"']")
        # # this_hotel_info_panel = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for Hotel near Gurgaon")]/div/div[@aria-label='+name+']')
        
        # print(this_hotel_info_panel)

        # # if this_hotel_info_panel:

        # #     cleaned_data = clean_panel(this_hotel_info_panel.text)
        # # else:
        # #     print('sKIP dATA')

        # cleaned_data = clean_panel(this_hotel_info_panel.text)
        # cleaned_data['name'] = name

        # try:
        #    with open(csv_file, 'a+', encoding='utf-8') as csvfile:
        #         writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter='|')
        #         writer.writerow(name)
        # except IOError:
        #    print("I/O error while typing to write to CSV file")

        # ActionChains(driver).click(this_result_div).perform()

        # time.sleep(BACK_TO_MAIN_LIST_DELAY)

        # next_btn = driver.find_element(By.XPATH, "//*[contains(@id, 'section-pagination-button-next')]")

        # if back_btn is None:
        #     # print('Aarif please find back btn')
        #     more_pages = False
        #     break
        # time.sleep(NEXT_PAGE_DELAY)
        # ActionChains(driver).click(this_result_div).perform()
        # print('Next Clicked')
            
        with open('data.csv','r') as in_file, open('output.csv','w') as out_file:
            seen = set() # set for fast O(1) amortized lookup
            for line in in_file:
                if line in seen: 
                    continue # skip duplicate
                seen.add(line)
                out_file.write(line)




    # print(data)

    # outFile =  open("data.csv",'a+',newline="")
    # writer = csv.writer(outFile)
    # writer.writerow(data)

    

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
time.sleep(5)
google_map_extractor(driver, map_query)

















