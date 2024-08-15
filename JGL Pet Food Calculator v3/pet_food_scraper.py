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

pet_food_db = pf.PET_FOOD_SESSION

RC_DOG_FOOD_SEARCH = "https://www.royalcanin.com/us/dogs/products/retail-products"
HILLS_DOG_FOOD_SEARCH = "https://www.hillspet.com/products/dog-food"
EUKANUBA_FOOD_SEARCH = "https://www.eukanuba.com/us/all-products"

def find_aafco_statement(text):
    """Queries the database for the AAFCO statement"""
    
    aafco_statements = pet_food_db.query(
                pf.AAFCOStatements
            ).all()
    
    formulated_to_meet = re.compile(r'formulated to meet', re.IGNORECASE)
    feeding_tests = re.compile(r'feeding tests using', re.IGNORECASE)
    
    for statement in aafco_statements:
        # Find the index of the AAFCO statement
        match = formulated_to_meet.search(text) or feeding_tests.search(text)
        
        # If the phrase is found, return the substring starting from the index
        if match:
            matched_text = text[match.start():]
            
            if statement.aafco_statement.lower() in matched_text.lower():
                return statement.statement_id
        
    return -1
            
def find_size_id(sizes):
    """Queries the database for the AAFCO statement"""
    
    
    normalized_sizes = sizes.strip().lower()
    
    container_sizes = pet_food_db.query(pf.PackageSizes).filter(
            pf.PackageSizes.package_size.ilike(normalized_sizes)
        ).all()
    
    
    if container_sizes:
        for size in container_sizes:
            return size.size_id
               
    return -1

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
            self.rc_dog_food_find_ingredient_list()
        
            self.driver.execute_script("arguments[0].click();", self.ingredients)
            self.driver.execute_script("arguments[0].click();", self.calorie_content)

            self.rc_dog_food_find_aafco_statement()
            self.rc_get_container_size()
    
    def rc_dog_food_click_nutritional_info_category(self):
        """Clicks on nutritional information"""
        
        nutritional_info = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-qa='product-accordion' and @tabindex='-1' and contains(@class, 'sc-gsFSXq') and contains(@class, 'gCjrge')]/button[@data-qa='product-accordion-button' and contains(@class, 'sc-dcJsrY') and contains(@class, 'iVRqTF')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", nutritional_info)
        
        # Retry clicking nutritional info category up to 3 times
        for _ in range(3):  
            try:
                print(nutritional_info.text)
                self.driver.execute_script("arguments[0].click();", nutritional_info)
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

        ingredient_text = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, ".//div[@class='sc-fPXMVe gTOXlX' and @data-testid='product-nutrition-content']"))
        )
        
        # Extract contents within "Vitamins [" and "Trace Minerals ["
        vitamins_content = re.findall(r'vitamins \[(.*?)\]', ingredient_text.text, flags=re.DOTALL)
        trace_minerals_content = re.findall(r'trace minerals \[(.*?)\]', ingredient_text.text, flags=re.DOTALL)
        
        print("Vitamins Content:", vitamins_content)
        print("Trace Minerals Content:", trace_minerals_content)
        
        # Remove "Vitamins [" and "Trace Minerals [" sections
        cleaned_text = re.sub(r'vitamins \[.*?\]', "", ingredient_text.text, flags=re.DOTALL)
        cleaned_text = re.sub(r'trace minerals \[.*?\]', "", cleaned_text, flags=re.DOTALL)
        
        print("Cleaned Text:", cleaned_text)
        
        # Add vitamin and mineral content to cleaned_text
        if vitamins_content:
            cleaned_text += ", " + ", ".join(vitamins_content[0].replace("\n", ", ").split(", "))
        if trace_minerals_content:
            cleaned_text += ", " + ", ".join(trace_minerals_content[0].replace("\n", ", ").split(", "))
        
        # Split the cleaned text into a list of ingredients
        ingredient_list = [ingredient.strip() for ingredient in cleaned_text.title().split(",") if ingredient.strip()]
        print("Ingredient List:", ingredient_list)
        
        # Pick protein sources out of the ingredient list 
        animal_proteins = []
        other_proteins = []
        for ingredient in ingredient_list:
            # Search entire ingredient list against the ProteinSources database

            if ingredient != "Fish Oil":
                protein_source = ingredient.split(" ")[0]
            elif ingredient == "Hydrolyzed Poultry" or ingredient == "Hydrolyzed Soy" or ingredient == "Hydrolyzed Chicken" or ingredient == "Hydrolyzed Salmon":
                protein_source = ingredient
                
            protein_search = pet_food_db.query(
                pf.ProteinSources
            ).filter(pf.ProteinSources.protein_source == protein_source).all()
            
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
        
        proteins = animal_proteins + other_proteins
        print(proteins)
        
        try:
            # First protein source
            first_protein_source = proteins[0]
            
            print(f"1st protein source: {first_protein_source}")
            # Second protein source
            second_protein_source = proteins[1]
            
            print(f"2nd protein source: {second_protein_source}")
            # Third protein source
            third_protein_source = proteins[2]
            
            print(f"3rd protein source: {third_protein_source}")
        except Exception as e:
            print(f"Can't find protein sources. Exception: {e}")
                # TODO: If ingredient matches a protein source in the database
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
        aafco_statement_text = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, ".//div[@class='sc-dLMFU fGHSVp']//div[@class='sc-fPXMVe gTOXlX' and @data-testid='product-nutrition-content']"))
        )
        

        print(aafco_statement_text.text)
                  
                # CREATE TABLE "DogFoods" (
                #     "food_id" INTEGER UNIQUE,
                #     "food_name" VARCHAR(300) UNIQUE,
                #     "food_form" INTEGER,
                #     "life_stage" VARCHAR(300),
                #     "description" VARCHAR(500),
                #     "size" INTEGER,
                #     "aafco_statement" INTEGER,
                #     "kcal_per_kg" INTEGER,
                #     "kcal_per_cup_can_pouch" INTEGER,
                #     "first_protein_source" INTEGER,
                #     "second_protein_source" INTEGER,
                #     "third_protein_source" INTEGER,
                #     "ingredient_list" VARCHAR(2000),
                #     PRIMARY KEY ("diet_id"),
                #     FOREIGN KEY ("food_form") REFERENCES "FoodForms"("form_id"),
                #     FOREIGN KEY ("life_stage") REFERENCES "LifeStages"("life_stage_id"),
                #     FOREIGN KEY ("size") REFERENCES "PackageSizes"("size_id"),
                #     FOREIGN KEY ("aafco_statement") REFERENCES "AAFCOStatements"("statement_id"),
                #     FOREIGN KEY ("first_protein_source") REFERENCES "ProteinSources"("protein_id"),
                #     FOREIGN KEY ("second_protein_source") REFERENCES "ProteinSources"("protein_id"),
                #     FOREIGN KEY ("third_protein_source") REFERENCES "ProteinSources"("protein_id")
                # )
        print(f"AAFCO index: {find_aafco_statement(aafco_statement_text.text)}")
        return aafco_statement_text
    
    def rc_get_container_size(self):
        """Grab the bag or case size"""
    
        # TODO: Grab selection dropdown menu or text string for dog food package sizes
        container_sizes_dropdown = self.driver.find_element(By.XPATH, value="//*[@id='packweightselector']")

        # Retrieve all options within the dropdown
        options = container_sizes_dropdown.find_elements(By.TAG_NAME, 'option')
        
        # Iterate through each option and print its text
        package_size = ""
        case_size_options = 0
        container_size_options = 0
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
                
                if case_sizes != None and case_sizes != 1:
                    case_size_options += 1
                
                # Format package size string for canned food
                if case_size_options == 1 and container_size:
                    package_size += f"{container_size}, case of {case_sizes}"
                elif case_sizes > 1:
                    print(f"{container_size}")
                else:
                    package_size += f", case of {case_sizes}"
            except (ValueError, IndexError):
                case_sizes = None
                container_size = sizes[0]
            
            print(sizes)
            
            # Add to the container_size_options if there is a container size
            if container_size != None:
                container_size_options += 1
                
            # Format package size string for dry food
            if container_size_options == 1:
                package_size += f"{container_size}"
            elif container_size_options > 1:
                package_size += f", {container_size}"
                
        # Checks formatting for package sizes
        print(f"Package sizes: {package_size}")
        
        # Finds the size_id of the package size string
        print(f"Size ID: {find_size_id(package_size)}")
        
        
                
            
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
    