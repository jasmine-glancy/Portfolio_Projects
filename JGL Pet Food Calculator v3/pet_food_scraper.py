"""A web scraper that creates a log of currently
available pet food and treats and logs their caloric
content"""

import re
from dotenv import load_dotenv
import pet_food_and_treats as pf
import selenium as s
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

load_dotenv("D:/Python/EnvironmentVariables/.env")


RC_DOG_FOOD_SEARCH = "https://www.royalcanin.com/us/dogs/products/retail-products"
HILLS_DOG_FOOD_SEARCH = "https://www.hillspet.com/products/dog-food"
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
        """Scrapes each item in the dog food list"""
        
        # Navigate to the specified URL
        print(f"Navigating to {RC_DOG_FOOD_SEARCH}")
        self.driver.get(RC_DOG_FOOD_SEARCH)
        
        time.sleep(5)
        # Verify the correct page is loaded
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        
        # Gets all the card elements
        while True:
            food_links = self.driver.find_elements(By.XPATH, "//li[@data-qa='product-grid-item']//a[@data-qa='product-card' and @data-testid='product-card-link']")
            
            if not food_links:
                break
            
            # Loops through each object in the list
            for i in range(len(food_links)):
                try:
                    # Re-fetch the list of links to avoid stale element reference
                    food_links = self.driver.find_elements(By.XPATH, "//li[@data-qa='product-grid-item']//a[@data-qa='product-card' and @data-testid='product-card-link']")
                    
                    # Scroll the element into view, suggested by CoPilot
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", food_links[i])
            
                    # Click on the food name link
                    print(food_links[i].text)
                    food_links[i].click()
                    
                    time.sleep(5)
                    
                    # Scrape product information
                    self.rc_scrape_dog_food()
                    
                    # Go back to the diet list page using JavaScript
                    self.driver.execute_script("window.history.go(-1)")
                    
                    # Wait for the page to load
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//li[@data-qa='product-grid-item']//a[@data-qa='product-card' and @data-testid='product-card-link']"))
                    )
                except Exception as e:
                    print(f"Error processing item: {e}")
                    continue 
        
    def rc_scrape_dog_food(self):
        """Scrapes the information on the diet page"""
        
        # Get the product's name
        food_name = self.driver.find_element(By.XPATH, value=".//h1[@class='ProductTitle-module_product-title__oY0UJ' and @data-qa='product-title']")
        print(food_name.text)
        
        # Find the product's form and verify species
        form_and_species = self.driver.find_element(By.XPATH, value=".//h2[@class='sc-bmzYkS cAMzIs' and @data-qa='product-category']")
        print(form_and_species.text)

        print(f"Life Stage ID: {pf.find_life_stage(food_name.text, form_and_species.text)}")
        
        print(f"Food Form ID: {pf.find_food_form(food_name.text, form_and_species.text)}")

        time.sleep(3)
        
        self.rc_dog_food_click_nutritional_info_category()
        self.rc_dog_food_find_calorie_content()
        self.rc_dog_food_find_ingredient_list()
    
        self.driver.execute_script("arguments[0].click();", self.ingredients)
        self.driver.execute_script("arguments[0].click();", self.calorie_content)

        self.rc_dog_food_find_aafco_statement()
        self.rc_get_container_size()
        self.rc_get_product_description()
        
        
    def rc_dog_food_click_nutritional_info_category(self):
        """Clicks on nutritional information"""
        
        self.nutritional_info = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-qa='product-accordion' and @tabindex='-1' and contains(@class, 'sc-gsFSXq') and contains(@class, 'gCjrge')]/button[@data-qa='product-accordion-button' and contains(@class, 'sc-dcJsrY') and contains(@class, 'iVRqTF')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.nutritional_info)
        
        # Retry clicking nutritional info category up to 3 times
        for _ in range(3):  
            try:
                print(self.nutritional_info.text)
                self.driver.execute_script("arguments[0].click();", self.nutritional_info)
                print("click successful")
                
                # Exit loop if click is successful
                break  
            except s.common.exceptions.ElementClickInterceptedException:
                print("Click intercepted, retrying...")
                
                # Wait before retrying
                time.sleep(1)  
            
    def rc_dog_food_find_calorie_content(self):
        """Gets kcal/kg and kcal/can or cup"""
        
        # "Click" on "calorie content" category
        self.calorie_content = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, ".//button[h3[contains(text(), 'Calorie Content')]]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.calorie_content)
        time.sleep(1)
        
        # Attempt to find calorie content category up to 3 times
        for _ in range(3): 
            try:
                self.driver.execute_script("arguments[0].click();", self.calorie_content)
                calorie_content_text = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, ".//div[@class='sc-fPXMVe gTOXlX' and @data-testid='product-nutrition-content']"))
                )
                
                self.internal_calorie_content_text = calorie_content_text.text
                print("Calorie Content Text:", self.internal_calorie_content_text)
                
                # Re suggested by CoPilot
                per_kg = r"\d+ kcal ME/kg|\d+ kilocalories of metabolizable energy \(ME\) per kilogram"
                per_can_cup = r"\d+ kcal ME/can|\d+ kcal ME/cup|\d+ kilocalories ME per cup|\d+ kilocalories ME per can"
                
                # Get ME/kg
                me_per_kg = re.search(per_kg, self.internal_calorie_content_text)
                if me_per_kg:
                    kcal_per_kg = me_per_kg.group(0)
                    self.kcal_per_kg_number = kcal_per_kg.split(" ")[0]
                    print(f"kcal per kg: {kcal_per_kg}")
                    print(self.kcal_per_kg_number)
                else:
                    print("ME per kg pattern not found")
                
                # Get kcal/can or kcal/cup
                per_unit = re.search(per_can_cup, self.internal_calorie_content_text)
                if per_unit:
                    kcal_per_can_or_cup = per_unit.group(0)
                    self.kcal_per_can_or_cup_number = kcal_per_can_or_cup.split(" ")[0]
                    
                    print(f"kcal per unit: {kcal_per_can_or_cup}")
                    print(self.kcal_per_can_or_cup_number)
                else:
                    print("kcal per can or cup pattern not found")
                    
                # Exit loop if scrape is successful
                break  
            except s.common.exceptions.ElementClickInterceptedException:
                # Wait before retrying
                time.sleep(1)  
                
        # TODO: if at the end of the result page, click on the next page
            # TODO: If no "next" page, stop scraping
        
    def rc_dog_food_find_ingredient_list(self):
        """Extract ingredient list"""
        
        # "Click" on "ingredients" 
        self.ingredients = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, ".//button[h3[contains(text(), 'Ingredients')]]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self.ingredients)
        time.sleep(1)
        
        self.driver.execute_script("arguments[0].click();", self.ingredients)

        self.ingredient_text = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, ".//div[@class='sc-fPXMVe gTOXlX' and @data-testid='product-nutrition-content']"))
        )
        
        print(f"Ingredients: {self.ingredient_text.text}")
        # Extract contents within "Vitamins [" and "Trace Minerals ["
        vitamins_content = re.findall(r'vitamins \[(.*?)\]|vitamins\[(.*?)\]', self.ingredient_text.text, flags=re.DOTALL)
        trace_minerals_content = re.findall(r'trace minerals \[(.*?)\]|trace minerals\[(.*?)\]', self.ingredient_text.text, flags=re.DOTALL)
        
        # Flatten lists, suggested by CoPilot
        vitamins_content = [item for sublist in vitamins_content for item in sublist if item]
        trace_minerals_content = [item for sublist in trace_minerals_content for item in sublist if item]
    
        print("Vitamins Content:", vitamins_content)
        print("Trace Minerals Content:", trace_minerals_content)
        
        # Remove "Vitamins [" and "Trace Minerals [" sections
        cleaned_text = re.sub(r'vitamins \[.*?\]|vitamins\[(.*?)\]', "", self.ingredient_text.text, flags=re.DOTALL)
        cleaned_text = re.sub(r'trace minerals \[.*?\]|trace minerals\[(.*?)\]', "", cleaned_text, flags=re.DOTALL)

        # Remove periods
        cleaned_text = re.sub(r'\.', "", cleaned_text)
        
        print("Cleaned Text:", cleaned_text)
        
        # Add vitamin and mineral content to cleaned_text
        if vitamins_content:
            cleaned_text += ", " + ", ".join(vitamins_content[0].replace("\n", ", ").split(", "))
        if trace_minerals_content:
            cleaned_text += ", " + ", ".join(trace_minerals_content[0].replace("\n", ", ").split(", "))


        # Split the cleaned text into a list of ingredients
        ingredient_list = [ingredient.strip() for ingredient in cleaned_text.title().split(",") if ingredient.strip()]
        print("Ingredient List:", ingredient_list)
        
        # Initialize ingredient_string with the first ingredient
        self.ingredient_string = ingredient_list[0] if ingredient_list else ""
        
        # Pick protein sources out of the ingredient list 
        animal_proteins = []
        other_proteins = []
        
        # Add remaining ingredients to ingredient_string
        for ingredient in ingredient_list[1:]:
            self.ingredient_string += f", {ingredient}"
            
        for ingredient in ingredient_list:
                
            # Search entire ingredient list against the ProteinSources database

            if ingredient != "Fish Oil":
                protein_source = ingredient.split(" ")[0]
            # Don't split any hydrolyzed ingredients or general/nonspecific protein ingredients 
            elif ingredient == "Hydrolyzed Poultry" or ingredient == "Hydrolyzed Soy" \
                or ingredient == "Hydrolyzed Chicken" or ingredient == "Hydrolyzed Salmon" \
                    or ingredient == "Meat By-product":
                protein_source = ingredient
                
            protein_search = pf.check_protein_type(protein_source)
            
            if protein_search:
                # If ingredient matches a protein source in the database
                for protein in protein_search:
                    if protein.protein_source not in animal_proteins and protein.protein_source not in other_proteins:
                        # Add protein to protein list if it is not there already
                        if protein.protein_type == "animal":
                            animal_proteins.append(protein.protein_source)
                        else:
                            # Add other protein sources by weight after animal sources 
                            other_proteins.append(protein.protein_source)
        
        # TODO: If ingredient matches a protein source in the database

        self.proteins = animal_proteins + other_proteins
        print(self.ingredient_string)
        print(self.proteins)
        
        try:
            # First protein source
            self.first_protein_source = self.proteins[0]
            
            print(f"1st protein source: {self.first_protein_source}")
            # Second protein source
            self.second_protein_source = self.proteins[1]
            
            print(f"2nd protein source: {self.second_protein_source}")
            # Third protein source
            self.third_protein_source = self.proteins[2]
            
            print(f"3rd protein source: {self.third_protein_source}")
        except Exception as e:
            print(f"Can't find protein sources. Exception: {e}")
                #  # add protein source to first/second/third_protein_source
                
                # first/second/third_protein_source is added to by ingredient weight
                
                # TODO: add protein sources to database by top 5 ingredients by weight
                # TODO: add the rest of ingredients to the db
                # TODO: if protein sources contain a common allergen, add to db
        
                        # TODO: add caloric content to database
    
    def rc_dog_food_find_aafco_statement(self):
        """Extract AAFCO statement if there is one"""
        
        # "Click" on "Nutritional Adequacy Statement" 
        aafco_statement = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, ".//div[@class='sc-dLMFU fGHSVp']//button[h3[contains(text(), 'Nutritional Adequacy Statement')]]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", aafco_statement)
        time.sleep(1)
        
        self.driver.execute_script("arguments[0].click();", aafco_statement)
        
        # Find AAFCO statement  
        self.aafco_statement_text = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, ".//div[@class='sc-dLMFU fGHSVp']//div[@class='sc-fPXMVe gTOXlX' and @data-testid='product-nutrition-content']"))
        )
        
        # Check the statement text
        print(self.aafco_statement_text.text)
                  
        # Match the text to the corresponding index in the AAFCOStatements table
        print(f"AAFCO index: {pf.find_aafco_statement(self.aafco_statement_text.text)}")
        return self.aafco_statement_text
    
    def rc_get_container_size(self):
        """Grab the bag or case size"""
    
        # Grab selection dropdown menu or text string for dog food package sizes
        container_sizes_dropdown = self.driver.find_element(By.XPATH, value="//*[@id='packweightselector']")

        # Retrieve all options within the dropdown
        options = container_sizes_dropdown.find_elements(By.TAG_NAME, 'option')
        
        self.package_size = []
        case_size_options = 0
        container_sizes = []

        for size in options:
            # Match RC's size formatting to match the PackageSize table entries
            size_text = size.text.replace("lb", " lbs").replace("oz", " oz")
            
            # Split by both "x" and "•" using regular expressions
            sizes = re.split(r'[x•]', size_text)
            
            # Strip leading and trailing whitespace from each element
            sizes = [s.strip() for s in sizes]
            
            # Gets the number in a case of cans
            try:
                case_sizes = int(sizes[0])
                
                # Gets the bag or can size
                container_size = sizes[1]
                if container_size not in container_sizes:
                    container_sizes.append(f"{container_size}")
                    
                if case_sizes != None and case_sizes != 1:
                    case_size_options += 1
                
                # Format package size string for canned food
                if case_sizes == 1 and container_size:
                    if container_size not in self.package_size:
                        self.package_size.append(f"{container_size}")
                elif case_sizes > 1:
                    formatted_size = f"case of {case_sizes}"
                    if formatted_size not in self.package_size:
                        self.package_size.append(formatted_size)
                
                
            except (ValueError, IndexError):
                case_sizes = None
                container_size = sizes[0]
                    
                # Format package size string for dry food
                self.package_size.append(f"{container_size}")
            print(sizes)

        # Remove duplicates and join all collected sizes with a comma and a space
        self.package_size = ", ".join(sorted(set(self.package_size), key=self.package_size.index))
        print(f"Package sizes: {self.package_size}")

        # Finds the size_id of the package size string
        print(f"Size ID: {pf.find_size_id(self.package_size)}")
        
    def rc_get_product_description(self):
        """Scrapes the product description for dog foods"""
        
        # Get the text for the product description
        self.product_description = self.driver.find_element(By.XPATH, value="//div[@data-qa='product-description' and @class='sc-eqUAAy eYrTKE']/p[contains(@class, 'sc-gEvEer fSrWKp')]")

        print(self.product_description.text)
                
            
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
# jg_web_scraper.eukanuba_food_search()
# TODO: Scraper should query brands that follow WSAVA guidelines in addition
## to BEG brands (Boutique, Exotic, Grain-Free)

# TODO: Scrape the main merchant websites for product name, form, and kcal information
    
# TODO: Add information to database if it is not already there
    