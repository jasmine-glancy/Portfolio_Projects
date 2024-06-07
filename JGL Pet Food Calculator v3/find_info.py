from cs50 import SQL
from flask import request, session, flash

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pet_food_calculator.db")

class FindInfo():
    def __init__(self, user_id, pet_id):
        """Verifies user_id and pet_id"""
    
        try:
            self.user_id = user_id
        except Exception as e:
            print(f"Exception: {e}, reassigning User ID as 0")
            self.user_id = 0  
            
        try: 
            self.pet_id = pet_id
        except Exception as e:
            print(f"Exception: {e}, reassigning pet ID as 0")
            self.pet_id = 0  
        
        self.pet_data = self.pet_data_dictionary(self.user_id, self.pet_id)
    
    def pet_data_dictionary(self, user_id, pet_id) -> dict:
        """Builds a dictionary of the current SQL row if logged in or session
        variables if no user is logged in"""
        
        try:
            self.user_id = user_id
        except Exception as e:
            print(f"Exception: {e}, reassigning User ID as 0")
            self.user_id = 0  
            
        try: 
            self.pet_id = pet_id
        except Exception as e:
            print(f"Exception: {e}, reassigning pet ID as 0")
            self.pet_id = 0  
        
        # If user is logged in and pet ID hasn't been assigned, use SQL query
        if pet_id != 0 and user_id != 0:
            self.pet_data = db.execute(
                "SELECT * FROM pets WHERE owner_id = :user_id AND pet_id = :pet_id",
                user_id=user_id, pet_id=pet_id
            )       
                
            # Check if pet_data is empty
            if not self.pet_data:
                print("The pet hasn't been added yet.")
            
            print(self.pet_data)
            
            
        # Otherwise, pass session variables
        else:        
            # Check Session variables for emptiness and update the dictionary if found
            
            pet_data = self.guest_pet_data_dictionary(self, user_id)    
            self.pet_data = pet_data
        
        return self.pet_data 
    
    def guest_pet_data_dictionary(self, user_id, pet_id) -> dict:
        """Builds a dictionary of session variables if no user is logged in"""

        if user_id == 0 or pet_id == 0:
            # Check Session variables for emptiness and update the dictionary if found
            self.guest_pet_data = [{"pet_id": None, "name": None, "age_in_years": None,
                        "age_in_months": None, "is_pediatric": None, "species": None,
                        "breed": None, "sex": None, "bcs": None, "weight": None, 
                        "units": None, "converted_weight": None, "converted_weight_units": None,
                        "ideal_weight_kgs": None, "ideal_weight_lbs": None, "activity_level": None,
                        "rer": None, "der": None, "der_factor_id": None, "der_modifier": None,
                        "current_food_amt_rec": None, "current_food_kcal": None, "current_food_form": None,
                        "meals_per_day": None, "current_food_amt_per_meal": None, "is_pregnant": None,
                        "weeks_gestating": None, "is_nursing": None, "litter_size": None, "weeks_nursing": None,
                        "rec_treat_kcal_per_day": None, "transitioning_food_one_kcal": None, "transitioning_food_one_form": None,
                        "transitioning_food_two_kcal": None, "transitioning_food_two_form": None}]
        
            if session["pet_id"] != None:
                self.guest_pet_data[0]["pet_id"] = session["pet_id"]
            elif session["pet_name"] != None:
                self.guest_pet_data[0]["name"] = session["pet_name"]
            elif session["pet_age_years"] != None:
                self.guest_pet_data[0]["age_in_years"] = session["pet_age_years"]
            elif session["pet_age_months"] != None:
                self.guest_pet_data[0]["age_in_months"] = session["pet_age_months"]
            elif session["is_pediatric"] != None:
                self.guest_pet_data[0]["is_pediatric"] = session["is_pediatric"]
            elif session["species"] != None:
                self.guest_pet_data[0]["species"] = session["species"]
            elif session["pet_breed"] != None:
                self.guest_pet_data[0]["breed"] = session["pet_breed"]
            elif session["pet_sex"] != None:
                self.guest_pet_data[0]["sex"] = session["pet_sex"]
            elif session["bcs"] != None:
                self.guest_pet_data[0]["bcs"] = session["bcs"]            
            elif session["weight"] != None:
                self.guest_pet_data[0]["weight"] = session["weight"]       
            elif session["units"] != None:
                self.guest_pet_data[0]["units"] = session["units"]
            elif session["converted_weight"] != None:
                self.guest_pet_data[0]["converted_weight"] = session["converted_weight"]       
            elif session["converted_weight_units"] != None:
                self.guest_pet_data[0]["converted_weight_units"] = session["converted_weight_units"]          
            elif session["activity_level"] != None:
                self.guest_pet_data[0]["activity_level"] = session["activity_level"]
            elif session["pregnancy_status"] != None:
                self.guest_pet_data[0]["is_pregnant"] = session["pregnancy_status"]
            elif session["number_weeks_pregnant"] != None:
                self.guest_pet_data[0]["weeks_gestating"] = session["number_weeks_pregnant"]
            elif session["lactation_status"] != None:
                self.guest_pet_data[0]["is_nursing"] = session["lactation_status"]
            elif session["litter_size"] != None:
                self.guest_pet_data[0]["litter_size"] = session["litter_size"]
            elif session["duration_of_nursing"] != None:
                self.guest_pet_data[0]["weeks_nursing"] = session["duration_of_nursing"]
            elif session["rer"] != None:
                self.guest_pet_data[0]["rer"] = session["rer"]
            elif session["der"] != None:
                self.guest_pet_data[0]["der"] = session["der"]
            elif session["der_factor_id"] != None:
                self.guest_pet_data[0]["der_factor_id"] = session["der_factor_id"]
            elif session["der_modifier"] != None:
                self.guest_pet_data[0]["der_modifier"] = session["der_modifier"]
            elif session["daily_amount_to_feed_cur_food"] != None:
                self.guest_pet_data[0]["current_food_amt_rec"] = session["daily_amount_to_feed_cur_food"] 
            elif session["current_food_form"] != None:
                self.guest_pet_data[0]["current_food_form"] = session["current_food_form"]                
            elif session["current_food_kcal"] != None:
                self.guest_pet_data[0]["current_food_kcal"] = session["current_food_kcal"] 
            elif session["meals_per_day"] != None:
                self.guest_pet_data[0]["meals_per_day"] = session["meals_per_day"]        
            elif session["current_food_amt_per_meal"] != None:
                self.guest_pet_data[0]["current_food_amt_per_meal"] = session["current_food_amt_per_meal"]            
            elif session["rec_treat_kcal_per_day"] != None:
                self.guest_pet_data[0]["rec_treat_kcal_per_day"] = session["rec_treat_kcal_per_day"]
            elif session["first_new_food_kcal"] != None:
                self.guest_pet_data[0]["transitioning_food_one_kcal"] = session["first_new_food_kcal"] 
            elif session["first_new_food_form"] != None:
                self.guest_pet_data[0]["transitioning_food_one_form"] = session["first_new_food_form"]                
            elif session["second_new_food_kcal"] != None:
                self.guest_pet_data[0]["transitioning_food_two_kcal"] = session["second_new_food_kcal"] 
            elif session["second_new_food_form"] != None:
                self.guest_pet_data[0]["transitioning_food_two_form"] = session["second_new_food_form"]    
                         
        return self.guest_pet_data

    def find_pet_id(self, user_id, animal_id) -> int:
        """Finds the specific pet ID"""
        
        print(f"ID arg: {animal_id}")
        
        if user_id != 0:
            # Check if pet_data is empty
            if not self.pet_data:
                print("The pet hasn't been added yet.")
            
            # See if the pet is already added 
            if "pet_id" in self.pet_data[0] or "pet_id" in self.guest_pet_data:
                pet_id = self.pet_data[0]["pet_id"]
                print(f"ID of pet: {pet_id}")
            else:
                print("Pet ID not found in pet_data.")
                pet_id = 0
        else:
            pet_id = 0
        
        return pet_id
            
            
    def find_all_user_pets(self):
        """Finds all pets under a user id"""
        
        if session["user_id"] != None:
            try:
                pet_list = db.execute(
                    "SELECT * FROM pets WHERE owner_id = :user",
                    user=session["user_id"]
                )
            
            except Exception as e:
                flash(f"Couldn't find pet list. Exception: {e}")
        
        return pet_list
            
    def login_check_for_species(self):
        """Checks if user is logged in, then assigns species"""
        # Conditional rewrite suggested by CoPilot 
        
        try:
            print(self.pet_data)
            species = self.pet_data[0]["species"]
            print(f"Class species: {species}")
        except Exception as e:
            flash(f"Can't find species ID. Exception: {e}")
        # if "user_id" in session and session["user_id"] != None:
            # If the user is logged in, verify table variables 
            # print(f"Species check User ID: {session["user_id"]}")
            # print(f"Species check Name: {session["pet_name"]}")
            
        
            # species_result = db.execute(
            #     "SELECT species FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
            # )
            

            # if species_result:
            #     species = species_result[0]["species"]
            #     print(species)
            # else:
            #     species = session["species"]
            #     print(f"Non-db species: {species}") 
                
        else:
            # If a user isn't logged in, grab species variable
            species = session["species"]
            
            # if species == None:
            #     species = request.args.get("species")
            # print(f"Non-db species: {species}") 
        
        # Return whatever species variable ends up being found 
        return species   


    def find_breed_id(self):
        """Returns the breed of the pet"""
    
        
        try:
            species = self.pet_data[0]["species"]
            if species == "Canine":
                breed_id = self.pet_data[0]["canine_breed_id"]
            if species == "Feline":
                breed_id = self.pet_data[0]["feline_breed_id"]
                
            print(f"Breed ID: {breed_id}")
            # if self.user_id != 0:
                # If the user is logged in, verify table variables 
                
                # try:
                #     print(session["user_id"])
                #     print(session["pet_name"])
                    
                #     species = login_check_for_species()
                    
                #     breed_result = db.execute(
                #         "SELECT canine_breed_id, feline_breed_id FROM pets WHERE owner_id = ? AND name = ?",
                #         session["user_id"], session["pet_name"]
                #     )
                # except Exception as e:
                #     flash("Unable to find a list of your pets. Please try again.")    
                # else:
                #     if species == "Canine":
                #         breed_id = breed_result[0]["canine_breed_id"]
                #     if species == "Feline":
                #         breed_id = breed_result[0]["feline_breed_id"]

                #     print(breed_id)
        
        except Exception as e:
            # If a user isn't logged in, grab breed ID variable
                
            try:
                breed_id = session["breed_id"]
                print(f"Non-db breed ID: {breed_id}") 
            except Exception as e:
                flash(f"Breed ID session variable not found, Exception: {e}")
                return None
        else:
            # Return whatever breed ID variable ends up being found if no errors
            return breed_id


def find_repro_status():
    """Returns the reproductive status of the pet"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(f"Check sex, User ID: {session["user_id"]}")
        print(f"Check sex, Name: {session["pet_name"]}")
        
        
        species_result = db.execute(
            "SELECT sex FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if species_result:
            pet_sex = species_result[0]["sex"]
            print(pet_sex)
        else:
            pet_sex = session["pet_sex"]
            print(f"Non-db repro status: {pet_sex}") 
            
    else:
        # If a user isn't logged in, grab session variable
        pet_sex = session["pet_sex"]
        
        print(f"Non-db repro status: {pet_sex}") 
    
    # Return whatever reproductive status variable ends up being found 
    return pet_sex


def check_if_pregnant():
    """Checks if the pet is pregnant"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(f"Pregnancy check, User ID: {session["user_id"]}")
        print(f"Pregnancy check, Name: {session["pet_name"]}")
        
        
        pregnancy_result = db.execute(
            "SELECT is_pregnant FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if pregnancy_result:
            is_pregnant = pregnancy_result[0]["is_pregnant"]
            print(is_pregnant)
        else:
            is_pregnant = session["pregnancy_status"]
            print(f"Non-db pregnancy status: {is_pregnant}") 
            
    else:
        # If a user isn't logged in, grab session variable
        is_pregnant = session["pregnancy_status"]
        
        print(f"Non-db pregnancy status: {is_pregnant}") 
    
    # Return whatever pregnancy variable ends up being found 
    return is_pregnant  


def check_if_nursing():
    """Checks if the pet is pregnant"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(f"Nursing check, User ID: {session["user_id"]}")
        print(f"Nursing check, Name: {session["pet_name"]}")
        
        
        nursing_result = db.execute(
            "SELECT is_nursing FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if nursing_result:
            is_nursing = nursing_result[0]["is_nursing"]
            print(is_nursing)
        else:
            is_nursing = session["lactation_status"]
            print(f"Non-db nursing status: {is_nursing}") 
            
    else:
        # If a user isn't logged in, grab session variable
        is_nursing = session["lactation_status"]
        
        print(f"Non-db nursing status: {is_nursing}") 
    
    # Return whatever nursing status variable ends up being found 
    return is_nursing  


def check_litter_size():
    """Checks if the pet is pregnant"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(f"Litter size check, User ID: {session["user_id"]}")
        print(f"Litter size check, Name: {session["pet_name"]}")
        
        
        litter_result = db.execute(
            "SELECT litter_size FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if litter_result:
            litter_size = litter_result[0]["litter_size"]
            print(litter_size)
        else:
            litter_size = session["litter_size"]
            print(f"Non-db litter size: {litter_size}") 
            
    else:
        # If a user isn't logged in, grab session variable
        is_pregnant = session["litter_size"]
        
        print(f"Non-db litter size: {litter_size}") 
    
    # Return whatever litter size variable ends up being found 
    return litter_size 


def check_if_pediatric():
    """Checks if the pet is pediatric"""
    
    if session["user_id"] != None:
        # If user isn logged in, query the database
            
        try:
            check_peds_status = db.execute(
                "SELECT is_pediatric FROM pets WHERE name = :pet_name AND owner_id = :user_id",
                pet_name=session["pet_name"], user_id=session["user_id"]
            )
        except Exception as e:
            flash(f"Unable to find pediatric status, Exception: {e}")
        else:
            is_pediatric = check_peds_status[0]["is_pediatric"]
    else:
        # If the user isn't logged in, grab session variables
        is_pediatric = session["is_pediatric"]
            
    print(f"Is Pediatric? {is_pediatric}")
    
    return is_pediatric


def check_obesity_risk():
    """Checks if a pet's breed has a predisposed risk to obesity"""
    
    # Use helpers.py to check for breed ID
    breed_id = find_breed_id()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    if species == "Canine":
        # Check if pet breed is predisposed to obesity
            breed_obesity_data = db.execute(
                "SELECT ObeseProneBreed FROM dog_breeds WHERE BreedID = :breed_id",
                breed_id=breed_id
            )
            
            if breed_obesity_data:
                obese_prone_breed = breed_obesity_data[0]["ObeseProneBreed"]
                  
    elif species == "Feline":
        # Check if pet breed is predisposed to obesity
            breed_obesity_data = db.execute(
                "SELECT ObeseProneBreed FROM cat_breeds WHERE BreedID = :breed_id",
                breed_id=breed_id
            )
            
            if breed_obesity_data:
                obese_prone_breed = breed_obesity_data[0]["ObeseProneBreed"]
                
    return obese_prone_breed


def find_food_form():
    """Find the form of the pet's current diet"""
    
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 
        print(session["user_id"])
        print(session["pet_name"])
        
        
        food_result = db.execute(
            "SELECT current_food_form FROM pets WHERE owner_id = ? AND name = ?", 
            session["user_id"], session["pet_name"]
        )
        

        if food_result:
            current_food_form = food_result[0]["current_food_form"]
            print(current_food_form)
        else:
            current_food_form = session["current_food_form"]
            print(f"Non-db current_food_form: {current_food_form}") 
            
    else:
        # If a user isn't logged in, grab food form variable
        current_food_form = session["current_food_form"]
        
        print(f"Non-db current_food_form: {current_food_form}")
    
    # Return whatever form variable ends up being found 
    return current_food_form 



def der_factor():
    """Finds the latest der_factor set, if applicable"""
    if "user_id" in session and session["user_id"] != None:
        # If the user is logged in, verify table variables 

        
        pet_info = db.execute(
            "SELECT species, canine_der_factor_id, feline_der_factor_id FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        )
        

        if pet_info:
            species = pet_info[0]["species"]
            if species == "Canine":
                der_factor_id = pet_info[0]["canine_der_factor_id"]
            elif species == "Feline":
                der_factor_id = pet_info[0]["feline_der_factor_id"]
                
            print(f"species: {species}, der_factor_id: {der_factor_id}")
        else:
            species = session["species"]
            der_factor_id = session["der_factor_id"]
            print(f"Non-db species: {species}, der_factor_id: {der_factor_id}") 
            
    else:
        # If a user isn't logged in, grab  variable
        der_factor_id = session["der_factor_id"]
    
    # Return whatever DER factor id variable ends up being found 
    print(f"DER factor ID: {der_factor_id}")
    return der_factor_id


def find_der_low_end():
    """Finds DER low end"""
    
    # Use helpers.py to verify species and check der_factor
    species = login_check_for_species()
    der_factor_id = der_factor()
    
    der_modifier_start_range = 0
    
    # Use DER factor id to lookup DER information by species
    if species == "Canine":
        der_lookup = db.execute(
            "SELECT life_stage, canine_der_factor_range_start FROM canine_der_factors \
                WHERE factor_id = :der_factor_id",
                der_factor_id=der_factor_id)
        print(der_lookup)

        # Find the start and end range of DER modifiers
        der_modifier_start_range = der_lookup[0]["canine_der_factor_range_start"]
        
    elif species == "Feline":
        der_lookup = db.execute(
        "SELECT life_stage, feline_der_factor_range_start \
            FROM feline_der_factors WHERE factor_id = :der_factor_id",
            der_factor_id=der_factor_id)
        print("der")
        print(F"Der lookup: {der_lookup}")

        # Find the starting DER modifier
        der_modifier_start_range = der_lookup[0]["feline_der_factor_range_start"]

    return der_modifier_start_range


def find_der_high_end():
    """Finds DER high end"""
    
    # Use helpers.py to verify species and check der_factor
    species = login_check_for_species()
    der_factor_id = der_factor()
    
    der_modifier_end_range = 0
    # Use DER factor id to lookup DER information by species
    if species == "Canine":
        der_lookup = db.execute(
            "SELECT life_stage, canine_der_factor_range_end \
                FROM canine_der_factors WHERE factor_id = :der_factor_id",
                der_factor_id=der_factor_id)
        print(f"DER lookup: {der_lookup}")

        # Find the ending DER modifier
        der_modifier_end_range = der_lookup[0]["canine_der_factor_range_end"]
        
    elif species == "Feline":
        der_lookup = db.execute(
        "SELECT life_stage, feline_der_factor_range_end \
            FROM feline_der_factors WHERE factor_id = :der_factor_id",
            der_factor_id=der_factor_id)
        print("der")
        print(F"Der lookup: {der_lookup}")

        # Find the start and end range of DER modifiers
        der_modifier_end_range = der_lookup[0]["feline_der_factor_range_end"]
    
    return der_modifier_end_range
            
def find_der_mid_range():
    """Finds DER mid-range"""
    
    # Use helpers.py to verify species and check der_factor
    species = login_check_for_species()
    der_factor_id = der_factor()
    
    # Use DER factor id to lookup DER information by species
    if species == "Canine":
        der_lookup = db.execute(
            "SELECT life_stage, ((canine_der_factor_range_start + canine_der_factor_range_end) / 2) AS mid_range \
                FROM canine_der_factors WHERE factor_id = :der_factor_id",
                der_factor_id=der_factor_id)
        print(der_lookup)


    elif species == "Feline":
        der_lookup = db.execute(
        "SELECT life_stage, ((feline_der_factor_range_start + feline_der_factor_range_end) / 2) AS mid_range \
            FROM feline_der_factors WHERE factor_id = :der_factor_id",
            der_factor_id=der_factor_id)
        print("der")
        print(F"Der lookup: {der_lookup}")

    # Find the middle range of DER modifiers
    der_mid_range = der_lookup[0]["mid_range"]
        
    print(f"Mid range DER Factor {der_mid_range}")
    
    return der_mid_range