"""A program that calls the USDA FoodData Central API to provide amounts
of human food to give to dogs and cats without unbalancing their diet

source:
U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2019. fdc.nal.usda.gov"""

# Using Blueprint 
from flask import Blueprint, render_template, request

# Define the Blueprint
human_foods = Blueprint("human_foods", __name__)

FOOD_DATA_CENTRAL_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

@human_foods.route("/search_human_foods", methods=["GET", "POST"])
def search_human_foods():
    """Looks up a list of corresponding human foods in
    the USDA's food database"""

    if request.method == "POST":

        # TODO: Call the string against USDA API via /foods/search

            # TODO: If the string matches anything in the USDA API, call a list
        
            # TODO: Otherwise, provide an error message
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
        