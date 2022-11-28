from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from parsel import Selector
from extra_data import ExtraInfo
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chromedrive_path = '/usr/lib/chromium-browser/chromedriver' # use the path to the driver you downloaded from previous steps 
driver = webdriver.Chrome(chromedrive_path)

url = 'https://www.google.com/maps/search/bars+near+NY,+USA/@40.7443439,-74.0197995,13z' 
# url = 'https://www.google.com/maps/place/Gurugram,+Haryana/@28.4230906,76.9197093,12z/data=!3m1!4b1!4m5!3m4!1s0x390d19d582e38859:0x2cf5fe8e5c64b1e!8m2!3d28.4594965!4d77.0266383' 
# url = 'https://www.google.com/maps/place/Lemon+Tree+Premier,+Leisure+Valley+2,+Gurgaon/@28.467708,77.0653,17z/data=!4m8!3m7!1s0x390d18fcf9a8eb31:0x221d7f9827536812!5m2!4m1!1i2!8m2!3d28.467708!4d77.0653?authuser=0&hl=en'



driver.get(url) 

page_content = driver.page_source 
response = Selector(page_content) 




results = [] 
 

for el in response.xpath('//div[contains(@aria-label, "Results for Gurgaon Hotel")]/div/div[./a]'):
    # phone = el.xpath('./@class/text()').get()
     
#     #extraInfo = ExtraInfo()
    url = el.xpath('./a/@href').extract_first('')

    #name
    title = driver.find_element(By.CLASS_NAME, "DUwDvf").text
    results.append(title)

    # phone = el.xpath('//a[contains(text(), "Phone")]/parent::span/following-sibling::span/a/span/text()').get()
    # print(el.xpath('./div/@class/text()').extract_first())
#     # business = el.xpath('//div[@role="heading"]/div')
#     # business.click()

    # results.append({ 
#         'title': el.xpath('./a/@aria-label').extract_first(''), 
#         #'address': el.xpath('./a/@aria-label').extract_first(''), 
        
#         #'telephone': el.xpath('./a/@aria-label').extract_first(''), 
        # 'link': url,
#         #'extra': extraInfo.get_business_info(url),

#             #'name':el.xpath('//h2[@data-attrid="title"]/span/text()').get(),
#             #'title':el.xpath('(//span[contains(text(), "Google reviews")])/parent::a/parent::span/parent::span/parent::div/parent::div/parent::div/following-sibling::div/div/span/span/text()').get(),
#             # 'address':el.xpath('//a[contains(text(), "Address")]/parent::span/following-sibling::span/text()').get(),
#             # 'website':el.xpath('(//a[contains(text(), "Website")])/@href').get(),
#             # #'phone':el.xpath('//a[contains(text(), "Phone")]/parent::span/following-sibling::span/a/span/text()').get(),
#             # #'hours':el.xpath('//a[contains(text(), "Hours")]/parent::span/following-sibling::div/label/span//btext()').get(),
#             # 'total_reviews':el.xpath('(//span[contains(text(), "Google reviews")])[1]/text()').get(),
#             # 'total_rating':el.xpath('(//span[contains(text(), "Google reviews")])/parent::a/parent::span/parent::span/parent::div/span/text()').get(),

    # }) 
 
print(results) 