"""A web scraper that creates a log of currently
available pet food and treats and logs their caloric
content"""

import re
from dotenv import load_dotenv
import selenium as s
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager



load_dotenv("D:/Python/EnvironmentVariables/.env")

RC_DOG_FOOD_SEARCH = "https://www.royalcanin.com/us/dogs/products/retail-products"
HILLS_DOG_FOOD_SEARCH = "https://www.hillspet.com/products/dog-food"
IAM_DRY_DOG_FOOD_SEARCH = "https://www.iams.com/dog/dog-food/dry"
EUKANUBA_FOOD_SEARCH = "https://www.eukanuba.com/us/all-products"

class JgWebScraper:
    def __init__(self):
        # Create the web driver
        
        options = Options()
                
        # Option to keep Chrome open
        options.add_experimental_option("detach", True)  
        
        # Use a temporary profile to avoid conflicts
        options.add_argument("--incognito")
        
        # Ignore SSL certificate errors
        options.add_argument("--ignore-certificate-errors")
        
        # Set a custom User-Agent string
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

        
        self.driver = webdriver.Chrome(options=options)
        
    def rc_dog_food_search(self):
        # Navigate to the specified URL
        print(f"Navigating to {RC_DOG_FOOD_SEARCH}")
        self.driver.get(RC_DOG_FOOD_SEARCH)
        
        time.sleep(5)
        # Verify the correct page is loaded
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        
        # Gets all the card elements
        food_card = self.driver.find_elements(By.XPATH, value="//*[@id='product-grid-ref']/ul")
        for item in food_card:
            food_link = item.find_element(By.XPATH, ".//h2[@data-qa='product-card-title' and contains(@class, 'sc-bypJrT') and contains(@class, 'hzXXXA')]")
            
            # "Click" on the food name link 
            print(food_link.text)
            food_link.click()
            
            time.sleep(5)
            
            # Get the product's name
            food_name = self.driver.find_element(By.XPATH, value=".//h1[@class='ProductTitle-module_product-title__oY0UJ' and @data-qa='product-title']")
            print(food_name.text)
            time.sleep(5)
            
            self.rc_dog_food_click_nutritional_info_category()
            self.rc_dog_food_find_calorie_content()
    
    def rc_dog_food_click_nutritional_info_category(self):
        """Clicks on nutritional information"""
        
        nutritional_info = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-qa='product-accordion' and @tabindex='-1' and contains(@class, 'sc-gsFSXq') and contains(@class, 'gCjrge')]/button[@data-qa='product-accordion-button' and contains(@class, 'sc-dcJsrY') and contains(@class, 'iVRqTF')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", nutritional_info)
        
        for _ in range(3):  # Retry up to 3 times
            try:
                print(nutritional_info.text)
                self.driver.execute_script("arguments[0].click();", nutritional_info)
                print("click successful")
                break  # Exit loop if click is successful
            except s.common.exceptions.ElementClickInterceptedException:
                print("Click intercepted, retrying...")

                time.sleep(1)  # Wait before retrying
            
    def rc_dog_food_find_calorie_content(self):
        """Gets kcal/kg and kcal/can or cup"""
        
        # "Click" on "calorie content" category
        calorie_content = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, ".//button[h3[contains(text(), 'Calorie Content')]]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", calorie_content)
        time.sleep(1)
        
        for _ in range(3):  # Retry up to 3 times
            try:
                self.driver.execute_script("arguments[0].click();", calorie_content)
                calorie_content_text = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//div[@class='sc-fPXMVe gTOXlX' and @data-testid='product-nutrition-content']"))
                )
                
                internal_calorie_content_text = calorie_content_text.text
                print("Calorie Content Text:", internal_calorie_content_text)
                
                # Re suggested by CoPilot
                per_kg = r"\d+ kcal ME/kg|\d+ kilocalories of metabolizable energy \(ME\) per kilogram"
                per_can_cup = r"\d+ kcal ME/can|\d+ kcal ME/cup|\d+ kilocalories ME per cup|\d+ kilocalories ME per can"
                
                # Get ME/kg
                me_per_kg = re.search(per_kg, internal_calorie_content_text)
                if me_per_kg:
                    kcal_per_kg = me_per_kg.group(0)
                    print(f"kcal per kg: {kcal_per_kg}")
                else:
                    print("ME per kg pattern not found")
                
                # Get kcal/can or kcal/cup
                per_unit = re.search(per_can_cup, internal_calorie_content_text)
                if per_unit:
                    kcal_per_can_or_cup = per_unit.group(0)
                    print(f"kcal per unit: {kcal_per_can_or_cup}")
                else:
                    print("kcal per can or cup pattern not found")
                    
                break  # Exit loop if click is successful
            except s.common.exceptions.ElementClickInterceptedException:
                time.sleep(1)  # Wait before retrying
                
                # TODO: add caloric content to database
                
            # TODO: "click" on "ingredients" 
                # TODO: pick protein sources out of the ingredient list 
                    # TODO: add protein sources to database
                    # TODO: if protein sources contain a common allergen, add to db
            
        # TODO: if at the end of the result page, click on the next page
            # TODO: If no "next" page, stop scraping
        
    def hills_dog_food_search(self):
        # Navigate to the specified URL
        print(f"Navigating to {HILLS_DOG_FOOD_SEARCH}")
        self.driver.get(HILLS_DOG_FOOD_SEARCH)
        
        time.sleep(5)
        # Verify the correct page is loaded
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        
        # Click truste-consent-button to consent to cookies
                
        # TODO: For each result in the page, "click" on result 
        
            # TODO: "click" on "average nutrient and caloric content" 
        
                # TODO: add caloric content to database
                
            # TODO: "click" on "ingredients" 
                # TODO: pick protein sources out of the ingredient list 
                    # TODO: add protein sources to database
                    # TODO: if protein sources contain a common allergen, add to db
            
        # TODO: if at the end of the result page, click on the next page
            # TODO: If no "next" page, stop scraping
            
    def iams_dry_dog_food_search(self):
        
        # Navigate to the specified URL
        print(f"Navigating to {IAM_DRY_DOG_FOOD_SEARCH}")
        self.driver.get(IAM_DRY_DOG_FOOD_SEARCH)
        
        time.sleep(5)
        # Verify the correct page is loaded
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        
        # TODO: For each result in the page, "click" on result 
        
            # TODO: "click" on "ingredients" 
        
                # TODO: add caloric content to database
                
                # TODO: pick protein sources out of the ingredient list 
                    # TODO: add protein sources to database
                    # TODO: if protein sources contain a common allergen, add to db
            
        # TODO: if at the end of the result page, click on the next page
            # TODO: If no "next" page, stop scraping
            
    def eukanuba_food_search(self):
        
        # Navigate to the specified URL
        print(f"Navigating to {EUKANUBA_FOOD_SEARCH}")
        self.driver.get(EUKANUBA_FOOD_SEARCH)
        
        time.sleep(5)
        # Verify the correct page is loaded
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        
        # TODO: For each result in the page, "click" on result 
        
            # TODO: "click" on "ingredients" 
        
                # TODO: add caloric content to database
                
                # TODO: pick protein sources out of the ingredient list 
                    # TODO: add protein sources to database
                    # TODO: if protein sources contain a common allergen, add to db
            
        # TODO: if at the end of the result page, click on the next page
            # TODO: If no "next" page, stop scraping
                
                
jg_web_scraper = JgWebScraper()
jg_web_scraper.rc_dog_food_search()
# jg_web_scraper.hills_dog_food_search()
# jg_web_scraper.iams_dry_dog_food_search()
# jg_web_scraper.eukanuba_food_search()
# TODO: Scraper should query brands that follow WSAVA guidelines in addition
## to BEG brands (Boutique, Exotic, Grain-Free)

# TODO: Scrape the main merchant websites for product name, form, and kcal information
    
# TODO: Add information to database if it is not already there
    