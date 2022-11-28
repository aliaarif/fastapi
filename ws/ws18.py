from selenium import webdriver
from parsel import Selector
from extra_data import ExtraInfo
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from parsel import Selector
import csv
import time

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

# url = 'https://www.google.com/maps/search/Gurgaon+Hotel/@28.4510568,76.9895883,1z/data=!4m5!2m4!5m2!5m1!1s2022-11-19!6e3'
url = 'https://www.google.com/maps/search/Hotel+near+Gurgaon/@28.4510568,76.9895883,3z/data=!4m4!2m3!5m2!5m1!1s2022-11-19'


driver.get(url)
page_content = driver.page_source
response = Selector(page_content)

pause_time = 2
max_count = 5
x = 0


for el in response.xpath('//div[contains(@aria-label, "Results for Gurgaon Hotel")]/div/div[./a]'):
    extraInfo = ExtraInfo()
    link = el.xpath('./a/@href').extract_first('')
    extraInfo.get_business_info(link)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "data-js-log-root")))

    while(x<max_count):
        scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
        try:
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        except:
            pass
        time.sleep(pause_time)
        x=x+1
        

# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "data-js-log-root")))

# while(x<max_count):
#         scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
#         try:
#             driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
#         except:
#             pass
#         time.sleep(pause_time)
#         x=x+1
        



print('Success!!!')
driver.quit()