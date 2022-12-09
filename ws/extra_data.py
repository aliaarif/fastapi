from ast import Not
from cmath import phase
from selenium.webdriver.chrome.service import Service
from tracemalloc import start
from selenium import webdriver
from selenium.webdriver.common.by import By
from parsel import Selector
# from photos import Photos
import csv
import time
import os


isExistDataFile = os.path.exists('hotels.csv')
if isExistDataFile:
    os.remove('hotels.csv')
    outFile =  open("hotels.csv","w",newline="")
    writer = csv.writer(outFile)
    writer.writerow(["name",	 "address",	 "telephone",	 "email",	 "website",	 "category",	 "sub_category",	 "rating",	 "reviews",	 "opening_hours",	 "search_keyword",	 "search_location",	 "claimed",	 "permanently_closed",	 "latitude",	 "longitude",	 "map_link",	 "image_url",	 "title",	 "title_url",	 "description"])
    



class ExtraInfo:

    

    def __init__(self):
        # self.fileName = name
        self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

    def get_business_info1(self, url):
        self.driver.get(url)
        
        page_content = self.driver.page_source 
        response = Selector(page_content) 

        results = [] 


        nameEnd = url.find('/data')

        name = latLongUrl[34:nameEnd].replace("+", " ")
        
        info = response.xpath("//div[contains(@aria-label, 'Information for "+name+"')]")

        for i in info:
            ci = i.xpath('./div[8]/div/div[2]/div[2]/span/text()').get()
            co = i.xpath('./div[8]/div/div[2]/div[2]/span[2]/text()').get()
            results.append(ci+'|'+co)

        results.append(description)
        outFile =  open("hotels.csv","a+",newline="")
        writer = csv.writer(outFile)
        writer.writerow(results)
        return True

    
    def get_business_info(self, url):
        self.driver.get(url)
        
        page_content = self.driver.page_source 
        response = Selector(page_content) 
        
    
        results = []        
        photos = response.xpath('//img[@style="position: absolute; top: 50%; left: 50%; width: 84px; height: 97px; transform: translateY(-50%) translateX(-50%);"]/@src').get()
 

        if photos != None:
            photos = photos.replace("=w80-h92-p-k-no", '')

        latLongUrl = url 
        latLongUrl = latLongUrl.replace("!16s%2Fg%", '|||')
        latLongUrl = latLongUrl.replace("!5m2!4m1!1i2!8m2!3d", '???')
        latLongUrl = latLongUrl.replace("!4d", ",,,")

        latStart = latLongUrl.find('???')
        latEnd = latLongUrl.find(",")
        
        llLat = latLongUrl[latStart+3:latEnd+1]

        longStart = latLongUrl.find(",")
        longEnd = latLongUrl.find('|||')

        llLong = latLongUrl[longStart+3:longEnd]



        nameEnd = latLongUrl.find('/data')

        name = latLongUrl[34:nameEnd].replace("+", " ")
        
        info = response.xpath("//div[contains(@aria-label, 'Information for "+name+"')]")

        
        

        
        

        #name
        title = self.driver.find_element(By.CLASS_NAME, "DUwDvf").text
        results.append(title)

        #address
        address = response.xpath('//button[@data-tooltip="Copy address"]/@aria-label').get()
        results.append(address[9:len(address)])

        #phone
        phone = response.xpath('//button[@data-tooltip="Copy phone number"]/@aria-label').get()
        results.append(phone[7:len(phone)])

        #email
        results.append('')

        #website
        results.append(response.xpath('//a[@data-tooltip="Open website"]/@href').get())

        #category
        # results.append(response.xpath('//span[@class="mgr77e"]/text()').get())
        cat = self.driver.find_element(By.CLASS_NAME, "e07Vkf").text
        results.append(cat)
        #sub_category
        if cat.find('hotel'):
            sub_category = "A,B,C"
            results.append(sub_category)
        else:
            sub_category = ""
            results.append(sub_category)
        #rating
        results.append(self.driver.find_element(By.CLASS_NAME, "F7nice").text)
        
        #review
        #results.append(self.driver.find_element(By.CLASS_NAME, "DkEaL").text)
        results.append('')
        
        for i in info:
            ci = i.xpath('./div[8]/div/div[2]/div[2]/span/text()').get()
            co = i.xpath('./div[8]/div/div[2]/div[2]/span[2]/text()').get()
            results.append(ci+'|'+co)

        #search_keyword
        results.append(response.xpath('//input[@id="searchboxinput"]/@value').get())
        #search_location
        sl = response.xpath('//button[@data-tooltip="Copy plus code"]/@aria-label').get()
        search_location = sl[11:len(sl)]
        # results.append(self.driver.find_element(By.CLASS_NAME, "Io6YTe").text)
        results.append(search_location)
        #claimed
        cl = self.driver.find_element(By.CLASS_NAME, "rogA2c").text
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
        results.append(url)
        #image_url
        results.append(photos)
        #title
        results.append(title)
        #title_url
        results.append(title)
        city = search_location[7:sl.find(",")]
        description = title +'is a '+cat+ ' which is located on '+address+' in '+city+'. The '+title+' offers '+sub_category+' services. If you need '+cat+' related services in '+city+' and nearby areas then you can use the below given '+title+' contact details or directly call on compnay helpline number '+phone+' for any question & quveries./n'
        description += 'For more detail, users can visit the officail website (website) of (Company Name)./n'
        description += 'Frequently Asked Question/n'
        description += 'What are the services Offered by '+title+'/n'
        description += sub_category+'/n'
        description += 'Which is the address of '+title+'/n'
        description += address+'/n'
        description += 'Which are service areas is covered by '+title+'/n'
        description += city
        results.append(description)
        outFile =  open("hotels.csv","a+",newline="")
        writer = csv.writer(outFile)
        writer.writerow(results)
        return True