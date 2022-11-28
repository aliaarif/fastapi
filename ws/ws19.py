#Importing libraries 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
from parsel import Selector
import time 
import string
import openpyxl
import os

#Loading Selenium Webdriver 
# driver= webdriver.Firefox()
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
wait = WebDriverWait(driver, 5)

#Opening Google maps 
driver.get("https://www.google.com/maps/search/Hotel+near+Gurgaon/@28.4510568,76.9895883,3z/data=!4m4!2m3!5m2!5m1!1s2022-11-19")
time.sleep(3)

#Closing the google consent form 
# elements=driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for Hotel near Gurgaon")]/div/div[./a]')
# driver.switch_to_frame(widget)

# button=driver.find_element(By.XPATH, './/*[@id="introAgreeButton"]')
# button.click()

#Finding the search box 
# driver.switch_to_default_content()
# searchbox=driver.find_element_by_id('searchboxinput')
# location= "Málaga"
# searchbox.send_keys(location)
# searchbox.send_keys(Keys.ENTER)
# time.sleep(2)
# cancelbut=driver.find_element(By.CLASS_NAME,'gsst_a')
# cancelbut.click()
# searchbox.send_keys("seguro")
# searchbox.send_keys(Keys.ENTER)
# time.sleep(3)


page_content = driver.page_source
response = Selector(page_content)

#Locating the results section 
entries=response.xpath('//div[contains(@aria-label, "Results for Hotel near Gurgaon")]/div/div[./a]')



while True:
    elemsCount = driver.execute_script("return document.querySelectorAll('.m6QErb > div[2]').length")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        WebDriverWait(driver, 20).until(
            lambda x: x.find_element_by_xpath(
                "//*[contains(@class,'stream-items')]/li[contains(@class,'stream-item')]["+str(elemsCount+1)+"]"))
    except:
        break

    

# print(len(entries))

#Prepare the excel file using the Openpyxl  
# wb= openpyxl.load_workbook("places.xlsx")
# sheetname=wb.get_sheet_names()[0]
# sheet=wb[sheetname]
# sheet.title ="places"


#Extracting the information from the results  


# options = driver.find_element(By.XPATH, "//div[@area-label='Results for Hotel near Gurgaon']")
# print(len(options))
# driver.execute_script("arguments[0].scrollIntoView(true);",option)
# for option in options:
#     print(option.xpath(''))

pause_time = 1
max_count = len(entries)


for entry in entries:
    #Empty list 
    labels=[]
    #Extracting the Name, adress, Phone, and website:
    
    # name= entry.get_attribute("aria-label")
    name = entry.xpath('./a/@aria-label').extract_first()
    link = entry.xpath('./a/@href').extract_first('')
    # adress= entry.find_element(By.CLASS_NAME,'section-result-location').text
    # phone = entry.find_element(By.CLASS_NAME,'section-result-hours-phone-container').text.split(' · ')[-1]
    # try:
        # webcontainer= entry.find_element(By.CLASS_NAME,'section-result-action-container')
        #website=entry.find_element(By.TAG_NAME, 'a').get_attribute("href")
    #except NoSuchElementException:
        #website="No website could be found"
    print (name)
    scrollable_div = driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for Hotel near Gurgaon")]')
    driver.execute_script("arguments[0].scrollIntoView();", scrollable_div)

    time.sleep(1)
    x=x+1

    #Try/except  to write the extracted info in the Excel file pass if doessn't exist 
    try:
        pass
        # sheet.append([name,adress,phone,website])
    except IndexError:
        pass

# entries.send_keys(Keys.PAGE_DOWN)

# print(sheet)    
#saving the excel file 
# wb.save("places.xlsx")