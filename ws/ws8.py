from selenium import webdriver
from parsel import Selector
from extra_data import ExtraInfo

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from parsel import Selector
# from photos import Photos
import csv
import time


from selenium.webdriver.chrome.service import Service

# chromedrive_path=Service('./chromedriver/chromedriver')
# browser = webdriver.Chrome(service=s)
# chromedrive_path = './chromedriver/chromedriver' # use the path to the driver you downloaded from previous steps
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")



# url = 'https://www.google.com/maps/search/bars+near+NY,+USA/@40.7443439,-74.0197995,13z'
url = 'https://www.google.com/maps/search/Gurgaon+Hotel/@28.4510927,76.9895884,12z/data=!3m1!4b1'
driver.get(url)
# time.sleep(10)


page_content = driver.page_source
response = Selector(page_content)


results = []

# elements = response.xpath('//div[contains(@aria-label, "Results for Gurgaon Hotel")]')
elements = response.xpath('//div[contains(@aria-label, "Results for Gurgaon Hotel")]/div/div')

outFile =  open("data.csv",'a+',newline="")
writer = csv.writer(outFile)

for el in elements:
    link = el.xpath('./a/@href').extract_first('')
    results.append(el.xpath('./a/@href').extract_first(''))
    

    # elements.send_keys(Keys.PAGE_DOWN)
    # time.sleep(3)


writer.writerow(results)
