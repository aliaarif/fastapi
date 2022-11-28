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


# driver.execute_script("window.scrollTo(300, document.body.scrollHeight);")
page_content = driver.page_source
response = Selector(page_content)


results = []

time.sleep(20)

# element = driver.find_element(By.TAG_NAME, "body")

prev_height = driver.execute_script('return document.body.scrollHeight)')






while True:
    # element.send_keys(Keys.PAGE_DOWN)
    driver.execute_script("window.scrollTo(300, document.body.scrollHeight);")
    time.sleep(3)
    
    new_height = driver.execute_script('return document.body.scrollHeight)')

    if new_height == prev_height:
        break
    prev_height = new_height




   