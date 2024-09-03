"""A program that calls the Nutrition API from FatSecret to provide amounts
of human food to give to dogs and cats without unbalancing their diet"""

# Using Blueprint 
import json
from flask import Blueprint, flash, render_template, url_for, \
    redirect, request
import os 
import re
import requests

# Define the Blueprint
human_foods = Blueprint("human_foods", __name__)

NUTRITION_API_URL = "https://platform.fatsecret.com/rest/server.api"
NUTRITION_CLIENT_ID = os.environ.get("NUTRITION_CLIENT_ID")
NUTRITION_API_SECRET = os.environ.get("NUTRITION_SECRET")
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"

# def get_oauth_token():
#     if not NUTRITION_CLIENT_ID or not NUTRITION_API_SECRET:
#         raise Exception("Client ID or Client Secret not set in environment variables")
    
#     response = requests.post(TOKEN_URL, data={
#         "grant_type": "client_credentials",
#         "client_id": NUTRITION_CLIENT_ID,
#         "client_secret": NUTRITION_API_SECRET,
#         "scope": "premier"
#     }, headers={
#         "Content-Type": "application/x-www-form-urlencoded"
#     })
#     response_data = response.json()
    
#     if "access_token" in response_data:
#         return response_data["access_token"]
#     else:
#         raise Exception(f"Failed to obtain access token: {response_data}")



@human_foods.route("/search_human_foods", methods=["GET", "POST"])
def search_human_foods():
    """Looks up a list of corresponding human foods in
    the Fatscreen food database"""

    found_foods_json = request.args.get("found_foods", "[]")
    found_foods = json.loads(found_foods_json)


    if request.method == "POST":
        print(request.form.get("food_name"))
        
        params = {
            "method":"foods.search",
            "search_expression":request.form.get("food_name"),
            "format":"json"
        }
        
        token = os.environ.get("token")
        
        headers = {
            "Content-Type":"application/json",
            "Authorization": f"Bearer {token}"
        }
        
        
        # Call the string against API 
        api_response = requests.get(NUTRITION_API_URL, params=params, headers=headers)
        
        if api_response.status_code == 200:
            # If the string matches anything in the  API, call a list
            data = api_response.json()
            print(data)
            found_foods = []
            
            foods_list = data.get("foods", {}).get("food", [])

            
            for item in foods_list:
                
                print(item)
                description = item.get("food_description", None)
                food_name = item.get("food_name", None)
                food_type = item.get("food_type", None)
                food_id = item.get("food_id", None)
                
                if food_type == "Brand":
                    brand_name = item.get("brand_name", None)
                else:
                    brand_name = "Generic"
                    
                serving_size = description.split("|")[0]
                serving_size_unit_full = serving_size.split("-")[0].strip()
                
                # Use regular expression to find the serving size number
                match = re.search(r'Per\s+(\d+)', serving_size_unit_full)
                
                if match:
                    serving_size_unit_number = match.group(1)
                else:
                    serving_size_unit_number = "Unknown"
                    
                calories = serving_size.split("-")[1].split(":")[1]
                calorie_number = calories.split("kcal")[0]
                
                print(brand_name, food_name, description, serving_size, serving_size_unit_full, serving_size_unit_number, calories, calorie_number)
                
                # Build a new dictionary to iterate over
                food_info = {
                    "description": description,
                    "food_name": food_name,
                    "food_type": food_type,
                    "brand_name": brand_name,
                    "serving_size_number": int(serving_size_unit_number),
                    "serving_size_string": serving_size_unit_full,
                    "num_calories": int(calorie_number),
                    "calorie_string": calories,
                    "food_id": food_id
                }
                    
                found_foods.append(food_info)
                    
            print(f"Found foods: {found_foods}")
            
            # Serialize found_foods to JSON
            found_foods_json = json.dumps(found_foods)
            
            
            return redirect(url_for("human_foods.search_human_foods", found_foods=found_foods_json))
        else:
            # Otherwise, provide an error message
            flash("Food not found. Please try again!")
            
            return redirect(url_for("human_foods.search_human_foods"))
              
    return render_template("query_human_food.html", found_foods=found_foods)

@human_foods.route("/calculate_treat_amounts", methods=["GET", "POST"])
def calculate_treat_amounts():
    pass
    # TODO: Have the user select an option

    # TODO: Call max treat amount per day from pet_food_calculator.db

        # TODO: Display human food treat amounts on the final report
        # # Database table? ID corresponding to a FK to USDA Treat Amounts table
        # # Limit to one option for now
        
        # TODO: Provide disclaimers
        
            # TODO: If the pet can have a large amount (i.e. >1 cup) of a certain type of
            # # human food, advise user to check with their vet that this amount will 
            # # cause no expected health issues 
        