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

#driver = webdriver.Firefox()

chromedrive_path = './chromedriver/chromedriver' # use the path to the driver you downloaded from previous steps 
driver = webdriver.Chrome(chromedrive_path)


# linksFile=open("links.txt",'r')
# allLinks = linksFile.readlines()

allLinks = [
    'https://www.google.com/maps/place/Lemon+Tree+Premier,+Leisure+Valley+2,+Gurgaon/data=!4m10!3m9!1s0x390d18fcf9a8eb31:0x221d7f9827536812!5m2!4m1!1i2!8m2!3d28.467708!4d77.0653!16s%2Fg%2F1tf9wt7v!19sChIJMeuo-fwYDTkREmhTJ5h_HSI?authuser=0&hl=en&rclk=1',
    'https://www.google.com/maps/place/THE+WOODS/data=!4m10!3m9!1s0x390d188a100d75c1:0x41445e6f3a27b526!5m2!4m1!1i2!8m2!3d28.442424!4d77.057245!16s%2Fg%2F1wfvl167!19sChIJwXUNEIoYDTkRJrUnOm9eREE?authuser=0&hl=en&rclk=1',
    'https://www.google.com/maps/place/Quality+Inn+Gurgaon/data=!4m10!3m9!1s0x390d18fc7ff70cbf:0xf928e52ca69690a6!5m2!4m1!1i2!8m2!3d28.4703831!4d77.0398463!16s%2Fg%2F1ptvzhc55!19sChIJvwz3f_wYDTkRppCWpizlKPk?authuser=0&hl=en&rclk=1',
    'https://www.google.com/maps/place/Hotel+Haut+Monde,+Gurgaon/data=!4m10!3m9!1s0x390d18466e76756b:0x3cb1e13cdf5ae45c!5m2!4m1!1i2!8m2!3d28.4552048!4d77.0381321!16s%2Fg%2F12ml2yqns!19sChIJa3V2bkYYDTkRXORa3zzhsTw?authuser=0&hl=en&rclk=1',
    'https://www.google.com/maps/place/Skycity+Hotel,+Gurgaon/data=!4m10!3m9!1s0x390d1944c1bdea0d:0x55e3c7fa345e02af!5m2!4m1!1i2!8m2!3d28.458394!4d77.0351739!16s%2Fg%2F1td089nb!19sChIJDeq9wUQZDTkRrwJeNPrH41U?authuser=0&hl=en&rclk=1',
    'https://www.google.com/maps/place/DS+Clarks+Inn+Gurgaon/data=!4m10!3m9!1s0x390d184816395391:0xb12c8ec92e20993d!5m2!4m1!1i2!8m2!3d28.4578148!4d77.0338472!16s%2Fg%2F1tmckm7l!19sChIJkVM5FkgYDTkRPZkgLsmOLLE?authuser=0&hl=en&rclk=1'
    ]

for link in tqdm(allLinks):

    try:
        driver.get(link)
        
    except Exception:
        print('Something went wrong with the URL: ')

    # time.sleep(15)

    while True:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Directions")] | //div[contains(text(), "Website")]'))
        )

        response0 = Selector(text=driver.page_source)

        #results = driver.find_elements_by_xpath('//div[contains(text(), "Directions")] | //div[contains(text(), "Website")]')
        results = response0.xpath('//div[contains(text(), "Directions")] | //div[contains(text(), "Website")]') 
        for result in results:
            # writing to the CSV file
            # outFile =  open("data.csv",'a+',newline="")
            # writer = csv.writer(outFile)

            business = response0.xpath('./a/@aria-label').extract_first('')
            print(business)
            
            #business.click()

            # waiting for the page to load
            # WebDriverWait(driver, 15).until(
            #     EC.presence_of_element_located((By.XPATH, '//div[@class="immersive-container"]'))
            # )


            # parcing response to the scrapy selector
            response = Selector(text=driver.page_source)
            

            #name = response.xpath('//h2[@data-attrid="title"]/span/text()').get()
            title = response.xpath('(//span[contains(text(), "Google reviews")])/parent::a/parent::span/parent::span/parent::div/parent::div/parent::div/following-sibling::div/div/span/span/text()').get()
            address = response.xpath('//a[contains(text(), "Address")]/parent::span/following-sibling::span/text()').get()
            website = response.xpath('(//a[contains(text(), "Website")])/@href').get()
            #phone = response.xpath('//a[contains(text(), "Phone")]/parent::span/following-sibling::span/a/span/text()').get()
            #hours = response.xpath('//a[contains(text(), "Hours")]/parent::span/following-sibling::div/label/span//btext()').get()
            total_reviews = response.xpath('(//span[contains(text(), "Google reviews")])[1]/text()').get()
            total_rating = response.xpath('(//span[contains(text(), "Google reviews")])/parent::a/parent::span/parent::span/parent::div/span/text()').get()


            input('Check: ')




            outFile =  open("data.csv",'a+',newline="")
            writer = csv.writer(outFile)
            
            vals = [title, address, website, total_reviews, total_rating]
            writer.writerow(vals)
            outFile.close()