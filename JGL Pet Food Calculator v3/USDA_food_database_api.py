"""A program that calls the USDA FoodData Central API to provide amounts
of human food to give to dogs and cats without unbalancing their diet

source:
U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2019. fdc.nal.usda.gov"""

# Using Blueprint 
from flask import Blueprint, flash, render_template, url_for, \
    redirect, request
import os 
import requests

# Define the Blueprint
human_foods = Blueprint("human_foods", __name__)

USDA_API_KEY = os.environ.get("USDA_API_KEY")
FOOD_DATA_CENTRAL_URL = f"https://api.nal.usda.gov/fdc/v1/foods/search"

@human_foods.route("/search_human_foods", methods=["GET", "POST"])
def search_human_foods():
    """Looks up a list of corresponding human foods in
    the USDA's food database"""

    if request.method == "POST":
        print(request.form.get("food_name"))
        
        params = {
            "api_key": USDA_API_KEY,
            "query":request.form.get("food_name")
        }
        
        # TODO: Call the string against USDA API via /foods/search
        fdc_response = requests.get(FOOD_DATA_CENTRAL_URL, params=params)
        
        if fdc_response.status_code == 200:
            # TODO: If the string matches anything in the USDA API, call a list
            data = fdc_response.json()
            found_foods = []
            
            for item in data.get("foods", []):
                description = item.get("description", "No description found")
                brand_name = item.get("brandName", "No brand name")
                
                energy_value = None
                energy_unit = None
                
                for nutrient in item.get("foodNutrients", []):
                    print(f"nutrient name: {nutrient.get("nutrientName")}, Nutrient value: {nutrient.get("value")}")
                    if nutrient.get("nutrientName") == "Energy":
                        energy_value = nutrient.get("value")
                        energy_unit = nutrient.get("unitName", [])
                        break
                    
                print(f"Description: {description}")
                if energy_value is not None and energy_unit is not None:
                    print(f"Energy: {energy_value} {energy_unit}")
                    
                    food_info = {
                        "description": description,
                        "brandName": brand_name,
                        "energy": f"{energy_value} {energy_unit}" if energy_value and energy_unit else "Energy information not available"
                    }
                    
                    found_foods.append(food_info)
                    
                else:
                    print("Energy information not available")
                
                print(f"Found foods: {found_foods}")
                return redirect(url_for("human_foods.search_human_foods", foods=found_foods))
        else:
            # TODO: Otherwise, provide an error message
            flash("Food not found. Please try again!")
            
            return redirect(url_for("human_foods.search_human_foods"))
        pass
    
    
            
    return render_template("query_human_food.html")


    # TODO: Have the user select an option

    # TODO: Call max treat amount per day from pet_food_calculator.db

        # TODO: Display human food treat amounts on the final report
        # # Database table? ID corresponding to a FK to USDA Treat Amounts table
        # # Limit to one option for now
        
        # TODO: Provide disclaimers
        
            # TODO: If the pet can have a large amount (i.e. >1 cup) of a certain type of
            # # human food, advise user to check with their vet that this amount will 
            # # cause no expected health issues 
        