"""Contains additional checks and decorators (i.e. is user logged in, login decorator)"""

from cs50 import SQL
from flask import request, session

# Configure CS50 Library to use SQLite database (for login checks)
db = SQL("sqlite:///pet_food_calculator.db")

def login_check_for_species():
    # Conditional rewrite suggested by CoPilot 
    
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        species_result = db.execute(
            "SELECT species FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if species_result:
            species = species_result[0]['species']
            print(species)
        else:
            species = session["species"]
            print(f"Non-db species: {species}") 
    else:
        # If a user isn't logged in, grab species variable
        species = session["species"]
        
        if species == None:
            species = request.args.get("species")
        print(f"Non-db species: {species}") 
    
    # Return whatever species variable ends up being found 
    return species   

