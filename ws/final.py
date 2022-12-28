from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from slugify import slugify


class WebDriver:

  location_data = {}

  def __init__(self):
    self.PATH = "/usr/lib/chromium-browser/chromedriver"
    self.options = Options()
#   Try adding this line if you get the error of chrome chrashed
#   self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
    self.options.add_argument("--headless")
    self.driver = webdriver.Chrome(self.PATH, options=self.options)
    
    self.location_data["name"] = "NA"
    self.location_data["title_slug"] = "NA"
    self.location_data["category"] = "NA"
    self.location_data["sub_category"] = []
    self.location_data["city"] = "NA"
    self.location_data["state"] = "NA"
    self.location_data["country"] = "India"
    self.location_data["address"] = "NA"
    self.location_data["phone"] = "NA"
    self.location_data["website"] = "NA"
    self.location_data["rating"] = "NA"
    self.location_data["reviews_count"] = "NA"
    self.location_data["search_keyword"] = "NA"
    self.location_data["search_location"] = "NA"
    self.location_data["claimed"] = "NA"
    self.location_data["permanently_closed"] = "NA"
    self.location_data["map_link"] = "NA"
    self.location_data["latitude"] = "NA"
    self.location_data["longitude"] = "NA"
    self.location_data["image_url"] = "NA"
    # self.location_data["opening_hours"] = "NA"
    self.location_data["time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
    self.location_data["popular_times"] = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[], "Sunday":[]}
    self.location_data["reviews"] = []
    self.location_data["description"] = "NA"


  def get_location_data(self, url:str):

    try:
		
      name = self.driver.find_element(By.CLASS_NAME, "DUwDvf").text
      title_slug = slugify(name)
      category = self.driver.find_element(By.CLASS_NAME, "mgr77e").text.replace('.', '')
      sub_category = self.driver.find_element(By.CLASS_NAME, "mgr77e").text.replace('.', '')
      copy_plus_code = self.driver.find_element(By.CSS_SELECTOR, "[data-tooltip='Copy plus code']").get_attribute('aria-label').strip()
      city = copy_plus_code[19:len(copy_plus_code)].split(',')[0]
      state = copy_plus_code[19:len(copy_plus_code)].split(',')[1]
      avg_rating = self.driver.find_element(By.CLASS_NAME, "ceNzKf").get_attribute('aria-label').strip()
      # total_reviews = self.driver.find_element(By.CLASS_NAME, "F7nice").find_elements('span[2]/span').text
      address = self.driver.find_element(By.CSS_SELECTOR, "[data-tooltip='Copy address']").get_attribute('aria-label').strip()
      
      phone = self.driver.find_element(By.CSS_SELECTOR, "[data-tooltip='Copy phone number']").get_attribute('aria-label').strip()
      website = self.driver.find_element(By.CSS_SELECTOR, "[data-tooltip='Open website']").get_attribute('aria-label').strip()
      # search_keyword = self.driver.find_element(By.CSS_SELECTOR, "[id='searchboxinput']/@value").get()
    #   merchant = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='merchant']").get_attribute('aria-label').strip()
    #   if(merchant == 'Claim this business'):
    #     claimed = 'Unvarified'
    #   else:
    #     claimed = 'Varified'
    #   image_url = self.driver.find_element(By.CLASS_NAME, "aoRNLd").get_attribute('aria-label').strip()
    #   image_url = self.driver.find_element(By.XPATH, '//img[@style="position: absolute; top: 50%; left: 50%; width: 408px; height: 284px; transform: translateY(-50%) translateX(-50%);"]/@src').get()
	
    #   if image_url != None:
    #     image_url = image_url.replace("=w80-h92-p-k-no", '')
	
     

    
    except:
      pass

    try:
      self.location_data["name"] = name
      self.location_data["title_slug"] = title_slug
      self.location_data["category"] = category
      self.location_data["sub_category"] = sub_category
      self.location_data["city"] = city
      self.location_data["state"] = state
      self.location_data["rating"] = avg_rating[0:-6]
      # self.location_data["reviews_count"] = total_reviews
      self.location_data["address"] = address
      self.location_data["phone"] = phone[7:len(phone)]
      self.location_data["website"] = website[9:len(website)]
      # self.location_data["search_keyword"] = search_keyword
      self.location_data["search_location"] = city+', '+state
      # self.location_data["claimed"] = merchant
      self.location_data["map_link"] = url
      self.location_data["latitude"] = url.split('!3d')[1][0:9]
      self.location_data["longitude"] = url.split('!3d')[1][12:21]
    #   self.location_data["image_url"] = image_url
      
	 
      
    except:
      pass

  def click_open_close_time(self):
    if(len(list(self.driver.find_elements(By.CLASS_NAME, "y0skZc")))!=0):
            element = self.driver.find_element(By.CLASS_NAME, "y0skZc")
            self.driver.implicitly_wait(5)
            ActionChains(self.driver).move_to_element(element).click(element).perform()

  def get_location_open_close_time(self):
    try:
        days = self.driver.find_elements(By.CLASS_NAME, "ylH6lf") # It will be a list containing all HTML section the days names.
        times = self.driver.find_elements(By.CLASS_NAME, "mxowUb") # It will be a list with HTML section of open and close time for the respective day.

        day = [a.text for a in days] # Getting the text(day name) from each HTML day section.
        open_close_time = [a.text for a in times] # Getting the text(open and close time) from each HTML open and close time section.

        for i, j in zip(day, open_close_time):
            self.location_data["time"][i] = j
    except:
        pass

  def get_popular_times(self):
    
    try:
      a = self.driver.find_elements_by_class_name("section-popular-times-graph") # It will be a List of the HTML Section of each day.
      dic = {0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday"}
      l = {"Sunday":[], "Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[]}
      count = 0

      for i in a:
        b = i.find_elements_by_class_name("section-popular-times-bar") # It will be a list of HTML Section of each hour in a day.
        for j in b:
          x = j.get_attribute("aria-label") # It gets the busy percentage value from HTML Section of each hour.
          l[dic[count]].append(x)
        count = count + 1

      for i, j in l.items():
        self.location_data["popular_times"][i] = j

    except:
      pass

  def click_all_reviews_button(self):
    try:
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "allxGeDnJMl__button")))

        element = self.driver.find_element_by_class_name("allxGeDnJMl__button")
        element.click()

    except:
        self.driver.quit()
        return False

    
    return True
  

  def scroll_the_page(self):
    try:
      WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root"))) # Waits for the page to load.
      pause_time = 2 # Waiting time after each scroll.
      max_count = 5 # Number of times we will scroll the scroll bar to the bottom.
      x = 0

      while(x<max_count):
        scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show') # It gets the section of the scroll bar.
        try:
          self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div) # Scroll it to the bottom.
        except:
          pass

        time.sleep(pause_time) # wait for more reviews to load.
        x=x+1

    except:
      self.driver.quit()

# 
  def expand_all_reviews(self):
    try:
      element = self.driver.find_elements_by_class_name("section-expand-review")
      for i in element:
        i.click()
    except:
      pass
  



# Step 10: Scrape Reviews Data
# Now that everything is been loaded we will create a function 
# that scrapes the reviews data like each reviewer name, text, posted date, and rating.
  def get_reviews_data(self):
    try:
      review_names = self.driver.find_elements_by_class_name("section-review-title") # Its a list of all the HTML sections with the reviewer name.
      review_text = self.driver.find_elements_by_class_name("section-review-review-content") # Its a list of all the HTML sections with the reviewer reviews.
      review_dates = self.driver.find_elements_by_css_selector("[class='section-review-publish-date']") # Its a list of all the HTML sections with the reviewer reviewed date.
      review_stars = self.driver.find_elements_by_css_selector("[class='section-review-stars']") # Its a list of all the HTML sections with the reviewer rating.

      review_stars_final = []

      for i in review_stars:
        review_stars_final.append(i.get_attribute("aria-label"))

      review_names_list = [a.text for a in review_names]
      review_text_list = [a.text for a in review_text]
      review_dates_list = [a.text for a in review_dates]
      review_stars_list = [a for a in review_stars_final]


      for (a,b,c,d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
        self.location_data["Reviews"].append({"name":a, "review":b, "date":c, "rating":d})

    except Exception as e:
      pass



# Final Step
# Now that we have all our functions created let’s just create the main function 
# that will simply call them one by one and execute the entire scraping process.
  def scrape(self, url): # Passed the URL as a variable
    try:
      self.driver.get(url) # Get is a method that will tell the driver to open at that particular URL

    except Exception as e:
      self.driver.quit()
      return

    time.sleep(10) # Waiting for the page to load.

    self.click_open_close_time() # Calling the function to click the open and close time button.
    self.get_location_data(url) # Calling the function to get all the location data.
    self.get_location_open_close_time() # Calling to get open and close time for each day.
    # self.get_popular_times() # Gets the busy percentage for each hour of each day.
    
    # if(self.click_all_reviews_button()==False): # Clicking the all reviews button and redirecting the driver to the all reviews page.
    #   return(self.location_data)

    time.sleep(5) # Waiting for the all reviews page to load.

    self.scroll_the_page() # Scrolling the page to load all reviews.
    # self.expand_all_reviews() # Expanding the long reviews by clicking see more button in each review.
    # self.get_reviews_data() # Getting all the reviews data.

    self.driver.quit() # Closing the driver instance.

    return(self.location_data) # Returning the Scraped Data.    
  


url = 'https://www.google.com/maps/place/Park+Inn,+Gurgaon/data=!4m10!3m9!1s0x390d1837b438e73f:0x9aa67946e7ae2cc4!5m2!4m1!1i2!8m2!3d28.459012!4d77.031737!16s%2Fg%2F1hdzgxscw!19sChIJP-c4tDcYDTkRxCyu50Z5ppo?authuser=0&hl=en&rclk=1'
x = WebDriver()
print(x.scrape(url))