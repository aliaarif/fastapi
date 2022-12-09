from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import re
from parsel import Selector
from extra_data import ExtraInfo

class WebDriver:

	location_data = {}

	def __init__(self):
		self.PATH = "/usr/lib/chromium-browser/chromedriver"
		self.options = Options()
		# self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
		self.options.add_argument("--headless")
		self.driver = webdriver.Chrome(self.PATH, options=self.options)

		self.location_data["name"] = "NA"
		self.location_data["link"] = "NA"
		self.location_data["rating"] = "NA"
		self.location_data["reviews_count"] = "NA"
		self.location_data["location"] = "NA"
		self.location_data["contact"] = "NA"
		self.location_data["website"] = "NA"
		self.location_data["Time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
		self.location_data["reviews"] = []
		self.location_data["popular_times"] = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[], "Sunday":[]}

		
    
		
	# def click_open_close_time(self, name):

	# 	if(len(list(self.driver.find_elements(By.CLASS_NAME, "cX2WmPgCkHi__section-info-hour-text")))!=0):
	# 		element = self.driver.find_element(By.CLASS_NAME, "cX2WmPgCkHi__section-info-hour-text")
	# 		self.driver.implicitly_wait(5)
	# 		ActionChains(self.driver).move_to_element(element).click(element).perform()

	# def click_all_reviews_button(self, name):

	# 	try:
	# 		WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "allxGeDnJMl__button")))

	# 		element = self.driver.find_element(By.CLASS_NAME, "allxGeDnJMl__button")
	# 		element.click()
	# 	except:
	# 		self.driver.quit()
	# 		return False

	
		
		
		

	def get_location_data(self,url):
		
		block = url[34:url.find('/data')]
		name = block.replace('+', ' ')
		link = url
		
		
		# WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "'+name+'")]')))
		# block.location_once_scrolled_into_view

		
		
		rating = self.driver.find_element(By.XPATH, "//div[@class='LBgpqf']/div/div/div/span/span").text
		
		
		# this_result_div = self.driver.find_element(By.XPATH, "//div[@aria-label='"+name+"']")
        
		# ugly_text_blob = this_result_div.text
		
		# text_blob = ugly_text_blob.splitlines()
        
		# addr = []
		
		# website = ''
		# phone = ''
		# location = ''
		# aux_unknown = ''
		# for line in range(len(text_blob)):
		# 	if line <= 1:
		# 		addr.append(text_blob[line])
		# 	elif line >= 2:
		# 		if 'closed' in text_blob[line].lower() or 'open' in text_blob[line].lower() or 'claim this' in text_blob[line].lower():
		# 			aux_unknown = ''    
		# 		else:
		# 			if text_blob[line].startswith('+9') or text_blob[line].startswith('9'):
		# 				phone = text_blob[line]
		# 			elif '+' in text_blob[line] and (re.search('[a-zA-Z]', text_blob[line]) != None):
		# 				location = text_blob[line]
		# 			else:
		# 				website = text_blob[line]
    
		# cleaned_block = {'addr1':addr[0], 'addr2':addr[1] if len(addr) > 1 else '', 'phone': phone, 'location': location, 'website': website, 'aux': aux_unknown}
		
		# print(cleaned_block)

		
			
			# avg_rating = self.driver.find_element(By.CLASS_NAME, "section-star-display")
			# total_reviews = self.driver.find_element(By.CLASS_NAME, "section-rating-term")

			# name = self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for Gurgaon Hotel")]/div/div[./a]/a/@aria-label')
			# link = self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "Results for Gurgaon Hotel")]/div/div[./a]/a/@href')
			# address = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']")
			# phone_number = self.driver.find_element(By.CSS_SELECTOR, "[data-tooltip='Copy phone number']")
			# website = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='authority']")
		
		try:
			# self.location_data["rating"] = avg_rating.text
			# self.location_data["reviews_count"] = total_reviews.text[1:-1]
			self.location_data['name'] = name
			self.location_data['link'] = link
			# self.location_data['rating'] = rating
			# self.location_data["link"] = link.get()
			# self.location_data["location"] = address.text
			# self.location_data["contact"] = phone_number.text
			# self.location_data["website"] = website.text
		except:
			pass


	# def get_location_open_close_time(self, name):

	# 	try:
	# 		days = self.driver.find_elements(By.CLASS_NAME, "lo7U087hsMA__row-header")
	# 		times = self.driver.find_elements(By.CLASS_NAME, "lo7U087hsMA__row-interval")

	# 		day = [a.text for a in days]
	# 		open_close_time = [a.text for a in times]

	# 		for i, j in zip(day, open_close_time):
	# 			self.location_data["Time"][i] = j
		
	# 	except:
	# 		pass

	# def get_popular_times(self, name):
	# 	try:
	# 		a = self.driver.find_elements(By.CLASS_NAME, "section-popular-times-graph")
	# 		dic = {0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday"}
	# 		l = {"Sunday":[], "Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[]}
	# 		count = 0

	# 		for i in a:
	# 			b = i.find_elements(By.CLASS_NAME, "section-popular-times-bar")
	# 			for j in b:
	# 				x = j.get_attribute("aria-label")
	# 				l[dic[count]].append(x)
	# 			count = count + 1

	# 		for i, j in l.items():
	# 			self.location_data["popular_times"][i] = j
	# 	except:
	# 		pass

	# def scroll_the_page(self, name):
	# 	try:
	# 		page_content = self.driver.page_source
	# 		response = Selector(page_content)
            
	# 		block = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "'+name+'")]')))
	# 		block.location_once_scrolled_into_view
	# 		# button.click()
            
	# 		# elements = response.xpath("//div[contains(@aria-label, '//div[contains(@aria-label, 'Information for "+name+")]")
			

	# 		for el in block:
				
	# 			try:
	# 				scrollable_div = self.driver.find_element(By.XPATH, '//div[contains(@aria-label, "Information for "'+name+'")]')
	# 				address = el.xpath('./div/button/@aria-label').extract_first('')
					
	# 				self.location_data['location'] = address
					
					
					
	# 				#self.driver.execute_script("window.scrollBy(0, arguments[0]);", 300)
	# 				# elements.send_keys(Keys.PAGE_DOWN)
	# 				# self.driver.execute_script
	# 			except:
	# 				# print('data nahi aa raha hai ')
	# 				pass
	# 			time.sleep(5)
	# 			x=x+1
	# 	except:
	# 		self.driver.quit()

	def expand_all_reviews(self, name):
		try:
			element = self.driver.find_elements(By.CLASS_NAME, "section-expand-review")
			for i in element:
				i.click()
		except:
			pass

	def get_reviews_data(self, name):
		try:
			review_names = self.driver.find_elements(By.CLASS_NAME, "section-review-title")
			review_text = self.driver.find_elements(By.CLASS_NAME, "section-review-review-content")
			review_dates = self.driver.find_elements(By.CSS_SELECTOR, "[class='section-review-publish-date']")
			review_stars = self.driver.find_elements(By.CSS_SELECTOR, "[class='section-review-stars']")

			review_stars_final = []

			for i in review_stars:
				review_stars_final.append(i.get_attribute("aria-label"))

			review_names_list = [a.text for a in review_names]
			review_text_list = [a.text for a in review_text]
			review_dates_list = [a.text for a in review_dates]
			review_stars_list = [a for a in review_stars_final]

			for (a,b,c,d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
				self.location_data["reviews"].append({"name":a, "review":b, "date":c, "rating":d})

		except Exception as e:
			pass

	def scrape(self, url):
		try:
			extraInfo = ExtraInfo()
			# self.driver.get(url)
			extraInfo.get_business_info(url)
		except Exception as e:
			self.driver.quit()
			# continue
		#time.sleep(1)
		
		# block = url[34:url.find('/data')]
		# name = block.replace('+', ' ')
	
		# self.click_open_close_time(name)
		# if url:
	    
		# extraInfo.get_business_info(url)
		
		# time.sleep(60)    
		
		# self.get_location_data(url)
		# self.get_location_open_close_time(name)
		# self.get_popular_times(name)
		# if(self.click_all_reviews_button(name)==False):
		# 	pass
		# time.sleep(10)
		# self.scroll_the_page(name)
		# self.expand_all_reviews(name)
		# self.get_reviews_data(name)
		#self.driver.quit()

		
        # return url
		# return(self.location_data)
		
		return True


# url = 'https://www.google.com/maps/place/The+Oberoi,+Gurgaon/@28.4510568,76.9895883,12z/data=!4m13!1m2!2m1!1sGurgaon+Hotel!3m9!1s0x390d194215555555:0xff1f79a278437064!5m2!4m1!1i2!8m2!3d28.5022034!4d77.0881901!15sCg1HdXJnYW9uIEhvdGVsWg8iDWd1cmdhb24gaG90ZWySAQVob3RlbOABAA!16s%2Fm%2F0h_9sml'


# with open('ouput.csv','w') as urls:
#     for url in urls:
# 	    final = allData.scrape(url)
	    
allData = WebDriver()


with open('output.csv','r') as urls:
    for url in urls:
        link = url
        # allData.scrape(url)
        #print('---------')
        final = allData.scrape(link)
	    # time.sleep(10)
        print(final)
	
    