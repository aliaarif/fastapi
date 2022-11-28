from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from scrapy.selector import Selector
import csv
from tqdm import tqdm
import time


 

class GoogleMapScraper:

   

    def __init__(self):
        self.PATH = '/usr/lib/chromium-browser/chromedriver'
        self.driver = webdriver.Chrome(self.PATH)
        self.business_list = []
        self.business_info = {}
        self.business_info["name"] = "NA"
        self.business_info["rating"] = "NA"
        self.business_info["category"] = "NA"
        self.business_info["phone"] = "NA"
        self.business_info["address"] = "NA"
        self.business_info["contact"] = "NA"
        self.business_info["website"] = "NA"

    def get_business_info(self, url):
        self.driver.get(url)
        # Parse data out of the page
        # self.business_info["name"] = self.driver.find_element_by_class_name("x3AX1-LfntMc-header-title-title").text
        # self.business_info["phone"] = self.driver.find_element(By.CLASS_NAME, "rogA2c").text
        # self.business_info["address"] = self.driver.find_element(By.CLASS_NAME, "rogA2c").text
        self.business_info["address"] = self.driver.find_element(By.XPATH, "div").text
        # self.business_info["address"] =  self.driver.xpath('//a[contains(text(), "Address")]/parent::span/following-sibling::span/text()').get()
         

        self.business_info["name"] =  self.driver.find_element(By.CLASS_NAME, "DUwDvf").text
        self.business_info["rating"] =  self.driver.find_element(By.CLASS_NAME, "F7nice").text
        self.business_info["category"] =  self.driver.find_element(By.CLASS_NAME, "mgr77e").text

        
        
        
        

        # self.business_info["rating"] = self.driver.find_element_by_class_name("aMPvhf-fI6EEc-KVuj8d").text
        # self.business_info["reviews_count"] = self.driver.find_element_by_class_name("widget-pane-link").text
     
        # self.business_info["contact"] = self.driver.find_elements_by_class_name("QSFF4-text")[1].text
        # self.business_info["website"] = self.driver.find_elements_by_class_name("QSFF4-text")[2].text
        #add business info to business list
        # self.business_list.append(self.business_info)

urls = ["https://www.google.com/maps/place/Lemon+Tree+Premier,+Leisure+Valley+2,+Gurgaon/data=!4m10!3m9!1s0x390d18fcf9a8eb31:0x221d7f9827536812!5m2!4m1!1i2!8m2!3d28.467708!4d77.0653!16s%2Fg%2F1tf9wt7v!19sChIJMeuo-fwYDTkREmhTJ5h_HSI?authuser=0&hl=en&rclk=1",]
BusinessScraper = GoogleMapScraper()
for url in urls:
    BusinessScraper.get_business_info(url)
print(BusinessScraper.business_info)