from cs50 import SQL
from flask import request, session, flash

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pet_food_calculator.db")

class FindInfo():
    def __init__(self, user_id, pet_id=None):
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
        
        if user_id == 0:
            # If the user has a "guest" ID, query guest dictionary
            self.pet_data = self.pet_data_dictionary(self.user_id, self.pet_id)
        else:
            self.guest_pet_data = self.pet_data_dictionary(self.user_id, self.pet_id)


    def find_der_high_end(self) -> float:
        """Finds DER high end"""
        
        # Use DER factor id to lookup DER information by species
        species = self.login_check_for_species()
        der_factor_id = self.der_factor()
        
        if species == "Canine":
            der_lookup = db.execute(
                "SELECT life_stage, canine_der_factor_range_end \
                    FROM canine_der_factors WHERE factor_id = :der_factor_id",
                    der_factor_id=der_factor_id)
            print(f"DER lookup: {der_lookup}")

            # Find the ending DER modifier
            self.der_modifier_end_range = der_lookup[0]["canine_der_factor_range_end"]
            
        elif species == "Feline":
            der_lookup = db.execute(
            "SELECT life_stage, feline_der_factor_range_end \
                FROM feline_der_factors WHERE factor_id = :der_factor_id",
                der_factor_id=der_factor_id)
            print("der")
            print(F"Der lookup: {der_lookup}")

            # Find the start and end range of DER modifiers
            self.der_modifier_end_range = der_lookup[0]["feline_der_factor_range_end"]
        
        return self.der_modifier_end_range
                
                
    def find_der_mid_range(self) -> float:
        """Finds DER mid-range"""
        
        species = self.login_check_for_species()
        der_factor_id = self.der_factor()
        
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
        self.der_mid_range = der_lookup[0]["mid_range"]
            
        print(f"Mid range DER Factor {self.der_mid_range}")
        
        return self.der_mid_range


    def find_der_low_end(self) -> float:
        """Finds DER low end"""
        
        # Use helpers.py to verify species and check der_factor
        # species = login_check_for_species()
        # der_factor_id = der_factor()
        
        
        try:
            # Use DER factor id to lookup DER information by species
            
            species = self.login_check_for_species()
            der_factor_id  = self.der_factor()
            
            if species == "Canine":
                der_lookup = db.execute(
                    "SELECT life_stage, canine_der_factor_range_start FROM canine_der_factors \
                        WHERE factor_id = :der_factor_id",
                        der_factor_id=der_factor_id)
                print(der_lookup)

                if "canine_der_factor_range_start" in der_lookup[0]:
                    # Find the start and end range of DER modifiers
                    self.der_modifier_start_range = der_lookup[0]["canine_der_factor_range_start"]
                
            elif species == "Feline":
                der_lookup = db.execute(
                "SELECT life_stage, feline_der_factor_range_start \
                    FROM feline_der_factors WHERE factor_id = :der_factor_id",
                    der_factor_id=der_factor_id)
                print(F"Der lookup: {der_lookup}")

                if "feline_der_factor_range_start" in der_lookup[0]:
                    # Find the starting DER modifier
                    self.der_modifier_start_range = der_lookup[0]["feline_der_factor_range_start"]
        except Exception as e:
            print(f"Can't find DER start range. Exception: {e}")
            
        return self.der_modifier_start_range

    
    def pet_data_dictionary(self, user_id, pet_id) -> dict:
        """Builds a dictionary of the current SQL row if logged in or session
        variables if no user is logged in"""
        
        # If user is logged in and pet ID hasn't been assigned, use SQL query
        if pet_id != 0 and user_id != 0:
            self.pet_data = db.execute(
                "SELECT * FROM pets WHERE owner_id = :user_id AND pet_id = :pet_id",
                user_id=user_id, pet_id=pet_id
            )       
                
            # Check if pet_data is empty
            if self.pet_data == None:
                print("The pet hasn't been added yet.")
            
            # print(self.pet_data)
            
            
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
            if self.pet_data and "pet_id" in self.pet_data[0] \
                or self.guest_pet_data and "pet_id" in self.guest_pet_data[0]:
                self.pet_id = self.pet_data[0]["pet_id"]
                print(f"ID of pet: {self.pet_id}")
            else:
                print("Pet ID not found in pet_data.")
                self.pet_id = 0
        else:
            self.pet_id = 0
        
        return self.pet_id
    
    
    def find_existing_pet(self, user_id, pet_id) -> bool:
        """Returns a True if pet is found in the database""" 
            
        
        print(f"user_id: {user_id}, pet_id: {pet_id}") 

        try:
            # See if the pet is already added
            find_existing_pet = db.execute(
                "SELECT pet_id, name FROM pets WHERE owner_id = :user_id AND pet_id = :pet_id",
                user_id=user_id, pet_id=pet_id
                ) 
            
            if not find_existing_pet:
                print("Pet not found.")
                return False
            
            pet_name = find_existing_pet[0]["name"]
            pet_id = find_existing_pet[0]["pet_id"]
            print(f"Name: {pet_name}", f"Pet ID: {pet_id} found")
            return True 
        
        except Exception as e:
            print(f"Pet not found. Exception: {e}")
            
            return False
        
    
    def find_wip_reports(self, user_id) -> dict:
        """Builds a list of in-progress reports"""
        
        if user_id != None or user_id != 0:
            # If user ID isn't empty or 0 (the "guest" user ID), query database
            try:
                wip_reports = db.execute(
                    "SELECT * FROM pets WHERE owner_id = :user AND date_of_first_report IS NULL",
                    user=user_id
                )
                
                print(wip_reports)
            except Exception as e:
                print(f"Can't find list of unfinished reports. Exception: {e}")
            
        return wip_reports
                
    def find_all_user_pets(self, user_id) -> dict:
        """Finds all pets under a user id"""
        
        if user_id != None or user_id != 0:
            # If user ID isn't empty or 0 (the "guest" user ID), query database
            try:
                pet_list = db.execute(
                    "SELECT * FROM pets WHERE owner_id = :user",
                    user=user_id
                )
            
                print(pet_list)
            except Exception as e:
                flash(f"Couldn't find pet list. Exception: {e}")
        
        return pet_list
        
            
    def login_check_for_species(self) -> str:
        """Checks if user is logged in, then assigns species"""
        
        try:
            if self.pet_data and "species" in self.pet_data[0]:
                self.species = self.pet_data[0]["species"]
                print(f"Class species: {self.species}")
        except Exception as e:
            flash(f"Can't find species ID. Exception: {e}")
                
        else:
            # If a user isn't logged in, grab species variable
            
            if "species" in session and session["species"] is not None:
                # Condition suggested by CoPilot
                self.species = session["species"]
            
            print(f"Session species: {self.species}") 
        
        # Return whatever species variable ends up being found 
        return self.species   


    def find_breed_id(self) -> int:
        """Returns the breed of the pet"""
        
        try:
            species = self.pet_data[0]["species"]
            if species == "Canine":
                breed_id = self.pet_data[0]["canine_breed_id"]
            if species == "Feline":
                breed_id = self.pet_data[0]["feline_breed_id"]
                
            print(f"Breed ID: {breed_id}")

        
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
        
    
    def check_if_pediatric(self) -> str:
        """Checks if the pet is pediatric"""
        
        try:
            if self.pet_data and "is_pediatric" in self.pet_data[0]:
                self.pediatric_status = self.pet_data[0]["is_pediatric"]
                print(f"Class pediatric status: {self.pediatric_status}")
        except Exception as e:
            flash(f"Can't find pediatric status. Exception: {e}")
                
        else:
            # If a user isn't logged in, grab species variable
            
            if "is_pediatric" in session and session["is_pediatric"] is not None:
                # Condition suggested by CoPilot
                self.pediatric_status = session["is_pediatric"]
            
            print(f"Session pediatric status: {self.pediatric_status}") 
        
        # Return whatever pediatric status variable ends up being found 
        return self.pediatric_status   
        # if session["user_id"] != None:
        #     # If user isn logged in, query the database
                
        #     try:
        #         check_peds_status = db.execute(
        #             "SELECT is_pediatric FROM pets WHERE name = :pet_name AND owner_id = :user_id",
        #             pet_name=session["pet_name"], user_id=session["user_id"]
        #         )
        #     except Exception as e:
        #         flash(f"Unable to find pediatric status, Exception: {e}")
        #     else:
        #         is_pediatric = check_peds_status[0]["is_pediatric"]
        # else:
        #     # If the user isn't logged in, grab session variables
        #     is_pediatric = session["is_pediatric"]
                
        # print(f"Is Pediatric? {is_pediatric}")
        
        # return is_pediatric
        
        
    def find_repro_status(self) -> str:
        """Returns the reproductive status of the pet"""
        
        try:
            if self.pet_data and "sex" in self.pet_data[0]:
                # If the user is logged in, verify table variables
                self.pet_sex = self.pet_data[0]["sex"]
                print(f"Pet's sex: {self.pet_sex}")
        except Exception as e:
            flash(f"Can't find pet's sex. Exception: {e}")
                
        else:    
            if "pet_sex" in session and session["pet_sex"] is not None:
                self.pet_sex = session["pet_sex"]
            
            print(f"Session pet's sex: {self.pet_sex}")     
        
        # Return whatever reproductive status variable ends up being found 
        return self.pet_sex
                
        #     if species_result:
        #         pet_sex = species_result[0]["sex"]
        #         print(pet_sex)
        #     else:
        #         pet_sex = session["pet_sex"]
        #         print(f"Non-db repro status: {pet_sex}") 
                
        # else:
        #     # If a user isn't logged in, grab session variable
        #     pet_sex = session["pet_sex"]
            
        #     print(f"Non-db repro status: {pet_sex}") 
        

    def check_if_pregnant(self) -> str:
        """Checks if the pet is pregnant"""
    
        try:
            if self.pet_data and "is_pregnant" in self.pet_data[0]:
                # If the user is logged in, verify table variables
                self.is_pregnant = self.pet_data[0]["is_pregnant"]
                print(f"Pet's pregnancy status: {self.is_pregnant}")
        except Exception as e:
            flash(f"Can't find pet's pregnancy status. Exception: {e}")
                
        else:    
            if "is_pregnant" in session and session["pregnancy_status"] is not None:
                self.is_pregnant = session["pregnancy_status"]
            
            print(f"Session pregnancy status: {self.is_pregnant}") 
    
        # Return whatever pregnancy variable ends up being found 
        return self.is_pregnant  
    
    # if "user_id" in session and session["user_id"] != None:
    #     # If the user is logged in, verify table variables 
    #     print(f"Pregnancy check, User ID: {session["user_id"]}")
    #     print(f"Pregnancy check, Name: {session["pet_name"]}")
        
        
    #     pregnancy_result = db.execute(
    #         "SELECT is_pregnant FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
    #     )
        

    #     if pregnancy_result:
    #         is_pregnant = pregnancy_result[0]["is_pregnant"]
    #         print(is_pregnant)
    #     else:
    #         is_pregnant = session["pregnancy_status"]
    #         print(f"Non-db pregnancy status: {is_pregnant}") 
            
    # else:
    #     # If a user isn't logged in, grab session variable
    #     is_pregnant = session["pregnancy_status"]
        
    #     print(f"Non-db pregnancy status: {is_pregnant}") 
    


    def check_if_nursing(self) -> str:
        """Checks if the pet is nursing"""
        
        try:
            if self.pet_data and "is_nursing" in self.pet_data[0]:
                # If the user is logged in, verify table variables
                self.is_nursing = self.pet_data[0]["is_nursing"]
                print(f"Pet's lactation status: {self.is_nursing}")
        except Exception as e:
            flash(f"Can't find pet's lactation status. Exception: {e}")
                
        else:    
            if "lactation_status" in session and session["lactation_status"] is not None:
                self.is_nursing = session["lactation_status"]
            
            print(f"Session lactation status: {self.is_nursing}") 
            
        # Return whatever nursing status variable ends up being found 
        return self.is_nursing  
       
        # if "user_id" in session and session["user_id"] != None:
        #     # If the user is logged in, verify table variables 
        #     print(f"Nursing check, User ID: {session["user_id"]}")
        #     print(f"Nursing check, Name: {session["pet_name"]}")
            
            
        #     nursing_result = db.execute(
        #         "SELECT is_nursing FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        #     )
            

        #     if nursing_result:
        #         is_nursing = nursing_result[0]["is_nursing"]
        #         print(is_nursing)
        #     else:
        #         is_nursing = session["lactation_status"]
        #         print(f"Non-db nursing status: {is_nursing}") 
                
        # else:
        #     # If a user isn't logged in, grab session variable
        #     is_nursing = session["lactation_status"]
            
        #     print(f"Non-db nursing status: {is_nursing}") 
        
        # # Return whatever nursing status variable ends up being found 
        # return is_nursing  


    def check_litter_size(self) -> int:
        """Checks the pet's litter size"""
        
        try:
            if self.pet_data and "litter_size" in self.pet_data[0]:
                # If the user is logged in, verify table variables
                self.litter_size = self.pet_data[0]["litter_size"]
                print(f"Pet's litter size: {self.litter_size}")
        except Exception as e:
            flash(f"Can't find pet's litter size. Exception: {e}")
                
        else:    
            if "litter_size" in session and session["litter_size"] is not None:
                self.litter_size = session["litter_size"]
            
            print(f"Session litter size: {self.litter_size}") 
            
        # Return whatever litter size variable ends up being found 
        return self.litter_size  
    
        # if "user_id" in session and session["user_id"] != None:
        #     # If the user is logged in, verify table variables 
        #     print(f"Litter size check, User ID: {session["user_id"]}")
        #     print(f"Litter size check, Name: {session["pet_name"]}")
            
            
        #     litter_result = db.execute(
        #         "SELECT litter_size FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        #     )
            

        #     if litter_result:
        #         litter_size = litter_result[0]["litter_size"]
        #         print(litter_size)
        #     else:
        #         litter_size = session["litter_size"]
        #         print(f"Non-db litter size: {litter_size}") 
                
        # else:
        #     # If a user isn't logged in, grab session variable
        #     is_pregnant = session["litter_size"]
            
        #     print(f"Non-db litter size: {litter_size}") 
        
        # # Return whatever litter size variable ends up being found 
        # return litter_size 


    def check_obesity_risk(self):
        """Checks if a pet's breed has a predisposed risk to obesity"""
        
        breed_id = self.find_breed_id()
        species = self.login_check_for_species()
        
        if species == "Canine":
            # Check if pet breed is predisposed to obesity
                breed_obesity_data = db.execute(
                    "SELECT ObeseProneBreed FROM dog_breeds WHERE BreedID = :breed_id",
                    breed_id=breed_id
                )
                
                if breed_obesity_data:
                    self.obese_prone_breed = breed_obesity_data[0]["ObeseProneBreed"]
                    
        elif species == "Feline":
            # Check if pet breed is predisposed to obesity
                breed_obesity_data = db.execute(
                    "SELECT ObeseProneBreed FROM cat_breeds WHERE BreedID = :breed_id",
                    breed_id=breed_id
                )
                
                if breed_obesity_data:
                    self.obese_prone_breed = breed_obesity_data[0]["ObeseProneBreed"]
                    
        return self.obese_prone_breed


    def der_factor(self) -> int:
        """Finds the latest der_factor set, if applicable"""
        
        if "user_id" in session and session["user_id"] != None:
            if self.species == "Canine":
                try:
                    self.der_factor_id = self.pet_data[0]["canine_der_factor_id"]
                    print(f"Class species: {self.species}", f"DER factor ID: {self.der_factor_id}")
                except Exception as e:
                    flash(f"Can't find DER Factor ID. Exception: {e}")
            if self.species == "Feline":
                try:
                    self.der_factor_id = self.pet_data[0]["feline_der_factor_id"]
                    print(f"Class species: {self.species}", f"DER factor ID: {self.der_factor_id}")
                except Exception as e:
                    flash(f"Can't find DER Factor ID. Exception: {e}")       
        else:
            # If a user isn't logged in, grab DER factor ID variable
            self.der_factor_id = session["der_factor_id"]
                    
            print(f"Session DER factor ID: {self.der_factor_id}") 
            
        print(f"DER factor ID: {self.der_factor_id}")
        
        return self.der_factor_id
        # # Condition suggested by CoPilot
        
        #     # If the user is logged in, verify table variables 

        #     self.pet_data
        #     pet_info = db.execute(
        #         "SELECT species, canine_der_factor_id, feline_der_factor_id FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
        #     )
            

        #     if pet_info:
        #         species = pet_info[0]["species"]
        #         if species == "Canine":
        #             der_factor_id = pet_info[0]["canine_der_factor_id"]
        #         elif species == "Feline":
        #             der_factor_id = pet_info[0]["feline_der_factor_id"]
                    
        #         print(f"species: {species}, der_factor_id: {der_factor_id}")
        #     else:
        #         species = session["species"]
        #         der_factor_id = session["der_factor_id"]
        #         print(f"Non-db species: {species}, der_factor_id: {der_factor_id}") 
                
        # else:
        #     # If a user isn't logged in, grab  variable
        #     der_factor_id = session["der_factor_id"]
        
        # # Return whatever DER factor id variable ends up being found 
        # print(f"DER factor ID: {der_factor_id}")
        # return der_factor_id


    def find_svg(self, user_id, pet_id=None) -> str:
        """Find SVG depending on breed and species"""
        
        species = self.login_check_for_species()
        breed_id = self.find_breed_id()
        
        if pet_id != 0 or pet_id != None:
            self.find_all_svgs = db.execute(
                "SELECT * FROM pets WHERE owner_id = :user AND pet_id = :pet_id",
                user=user_id, pet_id=pet_id
            )
        # TODO: Find a way to query guest SVG?
        
        for pet in self.find_all_svgs:
            try:
                if species == "Canine":
                    # If SVG can't be found, use a placeholder
                    self.svg = 'assets/svg/dogs/0_Labrador_Retriever_peeking_dog-4.svg'

                    svg_search = db.execute(
                        "SELECT svg FROM dog_breeds WHERE BreedId = :breed_id",
                        breed_id=breed_id
                        )
                        
                    if svg_search != None:
                        self.svg = 'assets/svg/dogs/' + svg_search[0]["svg"] 

                    print(self.svg)
                        
                elif species == "Feline":
                    # If SVG can't be found, use a placeholder
                    self.svg = 'assets/svg/cats/American_ShortHair0-04.svg'

                    # Search for breed image in database
                    svg_search = db.execute(
                        "SELECT svg FROM cat_breeds WHERE BreedId = :breed_id",
                        breed_id=breed_id
                        )
                        
                    if svg_search:
                        self.svg = 'assets/svg/cats/' + svg_search[0]["svg"] 


                    print(self.svg)
            except Exception as e:
                flash(f"Can't find SVG file. Exception: {e}")
        
        # If found, return SVG
        return self.svg
            
            
    def find_food_form(self) -> str:
        """Find the form of the pet's current diet e.g dry, canned, pouch"""
        
        try:
            if self.pet_data and "current_food_form" in self.pet_data[0]:
                # If the user is logged in, verify table variables
                self.current_food_form = self.pet_data[0]["current_food_form"]
                print(f"Pet's current food form: {self.current_food_form}")
        except Exception as e:
            flash(f"Can't find pet's current food form. Exception: {e}")
                
        else:    
            if "current_food_form" in session and session["current_food_form"] is not None:
                self.current_food_form = session["current_food_form"]
            
            print(f"Session current food form: {self.current_food_form}") 
            
        # Return whatever current food form variable ends up being found 
        return self.current_food_form  
    
        # if "user_id" in session and session["user_id"] != None:
        #     # If the user is logged in, verify table variables 
        #     print(session["user_id"])
        #     print(session["pet_name"])
            
            
        #     food_result = db.execute(
        #         "SELECT current_food_form FROM pets WHERE owner_id = ? AND name = ?", 
        #         session["user_id"], session["pet_name"]
        #     )
            

        #     if food_result:
        #         current_food_form = food_result[0]["current_food_form"]
        #         print(current_food_form)
        #     else:
        #         current_food_form = session["current_food_form"]
        #         print(f"Non-db current_food_form: {current_food_form}") 
                
        # else:
        #     # If a user isn't logged in, grab food form variable
        #     current_food_form = session["current_food_form"]
            
        #     print(f"Non-db current_food_form: {current_food_form}")
        
        # # Return whatever form variable ends up being found 
        # return current_food_form 



# def der_factor(self):
#     """Finds the latest der_factor set, if applicable"""
    
#     if "user_id" in session and session["user_id"] != None:
#         if self.species == "Canine":
#             try:
#                 self.der_factor_id = self.pet_data[0]["canine_der_factor_id"]
#                 print(f"Class species: {self.species}", f"DER factor ID: {self.der_factor_id}")
#             except Exception as e:
#                 flash(f"Can't find DER Factor ID. Exception: {e}")
#         if self.species == "Feline":
#             try:
#                 self.der_factor_id = self.pet_data[0]["feline_der_factor_id"]
#                 print(f"Class species: {self.species}", f"DER factor ID: {self.der_factor_id}")
#             except Exception as e:
#                 flash(f"Can't find DER Factor ID. Exception: {e}")       
#     else:
#         # If a user isn't logged in, grab species variable
#         self.der_factor_id = session["der_factor_id"]
                
#         print(f"Session DER factor ID: {self.der_factor_id}") 
        
#     print(f"DER factor ID: {self.der_factor_id}")
    
#     return self.der_factor_id
    # # Condition suggested by CoPilot
    
    #     # If the user is logged in, verify table variables 

    #     self.pet_data
    #     pet_info = db.execute(
    #         "SELECT species, canine_der_factor_id, feline_der_factor_id FROM pets WHERE owner_id = ? AND name = ?", session["user_id"], session["pet_name"]
    #     )
        

    #     if pet_info:
    #         species = pet_info[0]["species"]
    #         if species == "Canine":
    #             der_factor_id = pet_info[0]["canine_der_factor_id"]
    #         elif species == "Feline":
    #             der_factor_id = pet_info[0]["feline_der_factor_id"]
                
    #         print(f"species: {species}, der_factor_id: {der_factor_id}")
    #     else:
    #         species = session["species"]
    #         der_factor_id = session["der_factor_id"]
    #         print(f"Non-db species: {species}, der_factor_id: {der_factor_id}") 
            
    # else:
    #     # If a user isn't logged in, grab  variable
    #     der_factor_id = session["der_factor_id"]
    
    # # Return whatever DER factor id variable ends up being found 
    # print(f"DER factor ID: {der_factor_id}")
    # return der_factor_id

