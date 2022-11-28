from json import dumps
from time import sleep
from io import open
from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
from selenium import webdriver
# from webdriver_manager.chrome import Chrome, ChromeOptions, ChromeDriverManager

# driver = webdriver.Chrome(ChromeDriverManager().install())

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
class Scraper:
    def __init__(self, query: str, latitude: float, longitude: float):
        self.options = ChromeOptions()
        options:any.add_argument("--headless")
        options:any.add_argument("--incognito")
        self.browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser = Chrome(options = self.options)
        self.browser.get(f"https://www.google.com/maps/search/{query}/@{latitude},{longitude},12z/")
        # self.browser.get(f"https://www.google.com/maps/search/Gurugram,+Haryana/@28.4230906,76.9197093,12z/")
        
        sleep(0.1)

    def run(self):
        data = []
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        self.browser.quit()

        for business in soup.find_all("a", {"class": "hfpxzc"}):
            business_data = {}
            print(f'Scraping {business["aria-label"]}...')
            print(f'The URL to {business["aria-label"]} is at {business["href"]}')
            business_data["Name"] = business["aria-label"]
            business_data["URL"] = business["href"]

            temp_browser = Chrome(options = self.options)
            temp_browser.get(business["href"])
            sleep(0.1)
            temp_soup = BeautifulSoup(temp_browser.page_source, "html.parser")
            temp_browser.quit()
            print(f'Scraped {business["aria-label"]}! Now parsing it...')

            print(f'Scraping phone number of {business["aria-label"]}...')
            phone_number = temp_soup.find_all("div", {"class": "QSFF4-text gm2-body-2"})
            try:
                business_data["Phone Number"] = phone_number[0].get_text()
            except:
                business_data["Phone Number"] = None

            print(f'Scraping rating of {business["aria-label"]}...')
            rating = temp_soup.find_all("span", {"class": "aMPvhf-fI6EEc-KVuj8d"})
            try:
                business_data["Rating"] = rating[0].get_text()
            except:
                business_data["Rating"] = None

            print(f'Scraping number of reviews for {business["aria-label"]}...')
            num_reviews = temp_soup.find_all("button", {"class": "gm2-button-alt HHrUdb-v3pZbf"})
            try:
                business_data["Number of reviews"] = num_reviews[0].get_text()
            except:
                business_data["Number of reviews"] = None
            
            data.append(business_data)
        
        print("Finished entire scraping successfully!")
        self.data = dumps(data)
        return self.data

    def save(self, savepath: str):
        with open(savepath, "w") as json_writer:
            json_writer.write(self.data)

scraper = Scraper("transistors", 28.4510568, 76.9895883)
# 28.4510568,76.9895883
scraper.run()
scraper.save("data.json")
