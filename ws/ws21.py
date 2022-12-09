from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
from parsel import Selector
from extra_data import ExtraInfo
from slugify import slugify

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


isExistDataFile = os.path.exists('data.csv')
if isExistDataFile:
    os.remove('data.csv') 

isExistOutputFile = os.path.exists('output.csv')
if isExistOutputFile:
    os.remove('output.csv') 

# isExistDataFile = os.path.exists('hotels.csv')
# if isExistDataFile:
#     os.remove('hotels.csv')
#     outFile =  open("hotels.csv","w",newline="")
#     writer = csv.writer(outFile)
#     writer.writerow(["name",	 "address",	 "telephone",	 "website",	 "category",	 "sub_category",	 "rating",	 "reviews",	 "search_keyword",	 "search_location",	 "claimed",	 "permanently_closed",	 "latitude",	 "longitude",	 "map_link",	 "image_url",	 "title",	 "title_url", 	 "description", "opening_hours"])    





def google_map_extractor(driver, uri):
    #load up the page
    driver.get(uri)
    more_pages = True
    

    while more_pages:
        time.sleep(2)
        html = driver.page_source
        divs = WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a')))
        soup = BeautifulSoup(html, 'html.parser')
        response = Selector(html)
        time.sleep(1)
        result_list = response.xpath('//div[contains(@aria-label, "Results for hotels in gurgaon")]/div/div[./a]')
        # result_scroll_panel = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'Results for hotels in gurgaon')]")
        # total_results = len(result_list)
        i = 1
        for result_val in result_list:
            #print(f"Number of results found in this page: {total_results} and iteration is {i}")    
            name = result_val.xpath('./a/@aria-label').extract_first()
            link = result_val.xpath('./a/@href').extract_first()
            print(name)
            with open('data.csv', 'a') as fd:
                fd.write(f'\n{link}')
                if (i == 1):
                    more_pages = False
            try:
                this_result_div = driver.find_element(By.XPATH, '//div[@aria-label="'+name+'"]')
                driver.execute_script("arguments[0].scrollIntoView();", this_result_div)
                i = i + 1 
            except NoSuchElementException:
                #print('no data found for '+name)
                pass
        j = 0
        with open('data.csv','r') as in_file, open('output.csv','w') as out_file:
            seen = set() #set for fast O(1) amortized lookup
            for link in in_file:
                if link in seen: 
                    continue # skip duplicate
                seen.add(link)
                if j != 0:
                    out_file.write(link)
                j = j +1


driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
time.sleep(1)
map_query = 'https://www.google.com/maps/search/hotels+in+gurgaon'
google_map_extractor(driver, map_query)
                
                



with open('output.csv','r') as out_file:
    for link in out_file:
        # extraInfo = ExtraInfo()
        # extraInfo.get_business_info(link)

        results = [] 
        driver.get(link)
        
        page_content = driver.page_source 
        response = Selector(page_content) 

    
        photos = response.xpath('//img[@style="position: absolute; top: 50%; left: 50%; width: 84px; height: 97px; transform: translateY(-50%) translateX(-50%);"]/@src').get()
 

        if photos != None:
            photos = photos.replace("=w80-h92-p-k-no", '')

        latLongUrl = link 
        latLongUrl = latLongUrl.replace("!16s%2Fg%", '|||')
        latLongUrl = latLongUrl.replace("!5m2!4m1!1i2!8m2!3d", '???')
        latLongUrl = latLongUrl.replace("!4d", ",,,")

        latStart = latLongUrl.find('???')
        latEnd = latLongUrl.find(",")
        
        llLat = latLongUrl[latStart+3:latEnd+1]
        llLat = str(llLat)
        #llLat =  llLat.replace(',', '')

        longStart = latLongUrl.find(",")
        longEnd = latLongUrl.find('|||')

        llLong = latLongUrl[longStart+3:longEnd+1]
        llLong = str(llLong)
        #llLong = llLong.replace('|', '')
        

        nameEnd = link.find('/data')

        name = link[34:nameEnd].replace("+", " ")
        results.append(name)


       


        address = response.xpath('//button[@data-tooltip="Copy address"]/@aria-label').get()
        results.append(address[9:len(address)])


        #phone
        phone = response.xpath('//button[@data-tooltip="Copy phone number"]/@aria-label').get()
        results.append(phone[7:len(phone)])
        
        

        #website
        website = response.xpath('//a[@data-tooltip="Open website"]/@href').get()
        results.append(website)

        #category
        # results.append(response.xpath('//span[@class="mgr77e"]/text()').get())
        cat = driver.find_element(By.CLASS_NAME, "mgr77e").text
        results.append(cat)
        #sub_category
        if cat.find('hotel'):
            sub_category = "A,B,C"
            results.append(sub_category)
        else:
            sub_category = ""
            results.append(sub_category)
        #rating
        rt = driver.find_element(By.CLASS_NAME, "F7nice").text
        rating = rt[0:3]
        results.append(rating)
        
        #review
        #results.append(self.driver.find_element(By.CLASS_NAME, "DkEaL").text)
        reviewRow1 = rt.replace(rating, '')
        reviewRow2 = reviewRow1.replace('reviews', '')
        #review = reviewRow[4:len(reviewRow)]
        results.append(reviewRow2)


        

        #search_keyword
        results.append(response.xpath('//input[@id="searchboxinput"]/@value').get())
        #search_location
        sl = response.xpath('//button[@data-tooltip="Copy plus code"]/@aria-label').get()
        search_location = sl[11:len(sl)]
        # results.append(self.driver.find_element(By.CLASS_NAME, "Io6YTe").text)
        results.append(search_location)
        #claimed
        cl = driver.find_element(By.CLASS_NAME, "rogA2c").text
        if cl.find('Claim'):
            results.append("Unvarified")
        else:
            results.append('Verified')
        #permanently_closed
        results.append('')
        #latitude
        # results.append(url[latStart:latStart+3])
        results.append(llLat)
        #longitude
        results.append(llLong)
        #map_link
        results.append(link)
        #image_url
        results.append(photos)
        #title
        results.append(name)
        #title_url
        results.append(slugify(name))
        city = search_location[7:sl.find(",")]
        description = name +'is a '+cat+ ' which is located on '+address+' in '+city+'. The '+name+' offers '+sub_category+' services. If you need '+cat+' related services in '+city+' and nearby areas then you can use the below given '+name+' contact details or directly call on compnay helpline number '+phone+' for any question & quveries./n'
        description += 'For more detail, users can visit the officail website '+''+' of '+name+'./n'
        description += 'Frequently Asked Question/n'
        description += 'What are the services Offered by '+name+'/n'
        description += sub_category+'/n'
        description += 'Which is the address of '+name+'/n'
        description += address+'/n'
        description += 'Which are service areas is covered by '+name+'/n'
        description += city
        results.append(description)

        info = response.xpath("//div[contains(@aria-label, 'Information for "+name+"')]")

        for i in info:
            ci = i.xpath('./div[8]/div/div[2]/div[2]/span/text()').get()
            co = i.xpath('./div[8]/div/div[2]/div[2]/span[2]/text()').get()
            results.append(ci+'|'+co)

            
        #imgBtn = response.xpath("//div[contains(@aria-label, 'Photo of "+name+"')]").text
        # imgBtn = driver.find_element(By.CLASS_NAME, "Dx2nRe")

        # #button=driver.find_element(By.CLASS_NAME, ".//*[@class='Photo of "+name+"']")
        # imgBtn.click()
       
        # print(imgBtn.click())
        
        #imagesBtn = response.xpath("//div[contains(@class, 'm6QErb')]/div/div/button").get()
        # imagesBtn = driver.find_element(By.XPATH, "//div[contains(@class, 'm6QErb')]/div/div/button")
        # imagesBtn.click()

        # time.sleep(5)


        # img = driver.find_element(By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf"]/div/div[1]/a').get()
        # # img = driver.find_element(By.CLASS_NAME, "//a[contains(@data-photo-index, '1')]").get()
        # print(img)


        # time.sleep(5)
        
        
        #for btn in imagesBtn:

        #     print(btn)
        #     #imagesBtn.click()
        #     time.sleep(1)

        #imgessss = driver.find_element(By.CLASS_NAME, "U39Pmb").get()
        

        # for img in imgessss:
        #     #imgessss = driver.find_element(By.CLASS_NAME, "U39Pmb").get()
        #     print(img)


        outFile =  open("hotels.csv","a+",newline="")
        writer = csv.writer(outFile)
        writer.writerow(results)
        

print('All data successfully scrapped!!!')  


with open('../dist.csv','r') as out_file:
    for search_str in out_file:
        print(search_str)
        # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        #time.sleep(1)
        # map_query = 'https://www.google.com/maps/search/hotels+in+gurgaon'+search_str
        # google_map_extractor(driver, map_query)