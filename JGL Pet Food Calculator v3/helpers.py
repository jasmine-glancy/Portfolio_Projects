"""Contains additional checks and decorators (i.e. is user logged in, login decorator)"""

from cs50 import SQL
from flask import request, session

# Configure CS50 Library to use SQLite database (for login checks)
db = SQL("sqlite:///pet_food_calculator.db")

def login_check_for_species():
    """Checks if user is logged in, then assigns species"""
    # Conditional rewrite suggested by CoPilot 
    
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        species_result = db.execute(
            "SELECT species FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if species_result:
            species = species_result[0]["species"]
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

def der_factor():
    """Finds the latest der_factor set, if applicable"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        pet_info = db.execute(
            "SELECT species, canine_der_factor_id, feline_der_factor_id FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if pet_info:
            species = pet_info[0]["species"]
            if species == "Canine":
                der_factor_id = pet_info[0]['canine_der_factor_id']
            elif species == "Feline":
                der_factor_id = pet_info[0]['feline_der_factor_id']
                
            print(f"species: {species}, der_factor_id: {der_factor_id}")
        else:
            species = session["species"]
            der_factor_id = session["der_factor_id"]
            print(f"Non-db species: {species}, der_factor_id: {der_factor_id}") 
            
    else:
        # If a user isn't logged in, grab species variable
        species = session["species"]
        der_factor_id = session["der_factor_id"]
        
        if species == None:
            species = request.args.get("species")
        print(f"Non-db species: {species}") 
    
    # Return whatever DER factor id variable ends up being found 
    return der_factor_id  

def check_if_pregnant():
    """Checks if the pet is pregnant"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        species_result = db.execute(
            "SELECT is_pregnant FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if species_result:
            is_pregnant = species_result[0]['is_pregnant']
            print(is_pregnant)
        else:
            is_pregnant = session["pregnancy_status"]
            print(f"Non-db pregnancy status: {is_pregnant}") 
            
    else:
        # If a user isn't logged in, grab species variable
        is_pregnant = session["pregnancy_status"]
        
        print(f"Non-db pregnancy status: {is_pregnant}") 
    
    # Return whatever species variable ends up being found 
    return is_pregnant  

def find_repro_status():
    """Returns the reproductive status of the pet"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        species_result = db.execute(
            "SELECT sex FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if species_result:
            pet_sex = species_result[0]["sex"]
            print(pet_sex)
        else:
            pet_sex = session["pet_sex"]
            print(f"Non-db pregnancy status: {pet_sex}") 
            
    else:
        # If a user isn't logged in, grab species variable
        pet_sex = session["pet_sex"]
        
        print(f"Non-db pregnancy status: {pet_sex}") 
    
    # Return whatever species variable ends up being found 
    return pet_sex    

def calculcate_rer():
    """Calculates the minimum number of calories a pet needs at rest per day"""
    if session["user_id"] != None:
        # If the user is logged in, verify table variables 
        pet_info = db.execute(
            "SELECT weight, units FROM pets WHERE owner_id = ? AND name = ?", 
            session["user_id"], session["pet_name"]
        )
            
        print(pet_info)
            
        weight = pet_info[0]["weight"]
        units = pet_info[0]["units"]
    else:
        # If a user isn't logged in, grab session variables
        weight = session["weight"]
        units = session["units"]
        
    print(weight, units)
        
    # Convert lbs weighs to kgs
    if units == "lbs":
        weight = weight / 2.2
        units = "kgs"
        
    print(weight, units)
        
    rer = 0
    # If pet weighs more than 2kg and less than 45kg, use 30 × (BW kg) + 70 = RER
    if weight >= 2 and weight <= 45:
        rer = round((30 * weight) + 70, 2)
            
    # If pet weighs less than 2kg or more than 45kg, use 70 × (BW kg)^0.75 = RER
    if weight < 2 or weight > 45:
        rer = round(70 * weight**0.75, 2)
            
    print(rer) 
    session["rer"] = rer
     
    return rer

def find_breed_id():
    """Returns the breed of the pet"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        species = login_check_for_species()
        
        breed_result = db.execute(
            "SELECT canine_breed_id, feline_breed_id FROM pets WHERE owner_id = ? AND name = ?",
            session["user_id"], session["pet_name"]
        )
        

        if breed_result:
            if species == "Canine":
                breed_id = breed_result[0]["canine_breed_id"]
            if species == "Feline":
                breed_id = breed_result[0]["feline_breed_id"]

            print(breed_id)
   
    else:
        # If a user isn't logged in, grab breed ID variable
        breed_id = session["breed_id"]
        
        print(f"Non-db breed ID: {breed_id}") 
    
    # Return whatever breed ID variable ends up being found 
    return breed_id 