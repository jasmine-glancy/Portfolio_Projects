"""Contains the pet food calculator"""

from cs50 import SQL
from flask import session, flash
from find_info import FindInfo


# Configure CS50 Library to use SQLite database (for login checks)
db = SQL("sqlite:///pet_food_calculator.db")


class CalculateFood():
    def __init__(self, user_id, pet_id=None):
        """Query the pet's info for calculation"""
        
        fi = FindInfo(user_id)
        
        try:
            if user_id != 0 and pet_id != 0:
                # If the user is logged in and there is a pet ID, call data dictionary
                self.pet_data = fi.pet_data_dictionary(user_id, pet_id)
            else:
                # If there isn't a pet ID or a user ID greater than 0, call guest
                self.pet_data = fi.guest_pet_data_dictionary(user_id, pet_id)
            #     # If the user is logged in, verify table variables 
            #     self.pet_info = db.execute(
            #     "SELECT name, species, weight, units, is_nursing, litter_size, rer \
            #         FROM pets WHERE owner_id = ? AND name = ?", 
            #     user_id, pet_id
            # )
                
            # print(self.pet_info)
                
            # self.name = self.pet_info[0]["name"]
            # self.species = self.pet_info[0]["species"]
            # self.weight = self.pet_info[0]["weight"]
            # self.units = self.pet_info[0]["units"]
            # self.is_nursing = self.pet_info[0]["is_nursing"]
            # self.rer = self.pet_info[0]["rer"]
        except Exception as e:
            # Otherwise, raise exception and pass session variables
            flash(f"Unable to lookup pet data. Exception: {e}")
            
            # try:
            #     self.name = session["pet_name"]
            #     self.species = session["species"]
            #     self.weight = session["weight"]
            #     self.units = session["units"]
            #     self.rer = session["rer"]
                
            #     if session["lactation_status"] != None:
            #         # If there is a nursing status input, add to session variables
            #         self.is_nursing = session["lactation_status"]
                    
            # except Exception as e:
            #     print(f"Unable to find session variables for RER. Exception: {e}")
            
    def calculcate_rer(self):
        """Calculates the minimum number of calories a pet needs at rest per day"""
        
        # if session["user_id"] != None:
        #     # If the user is logged in, verify table variables 
            
        #     try: 
        #     self.pet_info
        #     print(self.pet_info)
        # else:
        #     # If a user isn't logged in, grab session variables
            
        #     try:
        #         self.weight = session["weight"]
        #         self.units = session["units"]
            
            
        print(self.weight, self.units)
            
        # Convert lbs weighs to kgs
        if self.units == "lbs":
            self.weight = self.weight / 2.2
            self.units = "kgs"
            
        print(self.weight, self.units)
            
        self.rer = int(70 * self.weight**0.75)
                
        print(self.rer) 
        session["rer"] = self.rer
        
        return self.rer


    def calculcate_der(self):
        """Calculates daily caloric needs based on life stage"""
        
        # # Check species and nursing status
        # species = login_check_for_species()
        # is_nursing = check_if_nursing()
        # litter_size = check_litter_size()
        
        # # find pet's RER
        # # If user is logged in, use SQL query
        # if session["user_id"] != None:
        #     try:
        #         print(session["pet_name"])
        #         print(session["user_id"])
                    
        #         pet_data = db.execute(
        #             "SELECT rer FROM pets WHERE owner_id = :user_id AND name = :pet_name",
        #             user_id=session["user_id"], pet_name=session["pet_name"]
        #         )       
                
        #         print(pet_data)
                
        #         if pet_data:  
        #             rer = int(pet_data[0]["rer"])
        #     except Exception as e:
        #         flash(f"Unable to find pet data for RER calculation, Exception: {e}")    
        # else:
        #     # If a user isn't logged in, grab session variables
        #     rer = session["rer"]     
            
        # Use DER factor id to lookup DER information by species
        self.der_modifier_start_range = self.fi.find_der_low_end()
        self.der_modifier_end_range = self.fi.find_der_high_end()

        # Start with the mid range if this is the first report
        # TODO: check report date and change modifier choice based on weight changes
        self.der_modifier = self.fi.find_der_mid_range()

        # Calculate DER based on the der modifier and pass variables to tempate
        if self.species == "Feline" and self.is_nursing == "y":
            self.der = round((self.rer + self.der_modifier * self.litter_size), 2)
        else:
            self.der = round(self.rer * self.der_modifier, 2)
        print(f"DER: {self.der}")
        
        self.der_low_end = self.rer * self.der_modifier_start_range
        self.der_high_end = self.rer * self.der_modifier_end_range
        self.der_low_end, self.der_high_end = int(float(self.der_low_end)), int(float(self.der_high_end))
        
        
        return {"DER": self.der, 
                "DER_low_end": self.der_low_end, 
                "DER_high_end": self.der_high_end,
                "DER_modifier": self.der_modifier}


    def convert_decimal_to_volumetric(self, partial_amount):
        """Convert partial volume amount from decimal to cups"""
        
        # Volume table source: https://amazingribs.com/more-technique-and-science/more-cooking-science/important-weights-measures-conversion-tables/
        
        self.partial_volumetric = ""
        if partial_amount > "0" and partial_amount <= "03":
            self.partial_volumetric = "1/2 tablespoon"
        elif partial_amount > "03" and partial_amount <= "06":
            self.partial_volumetric = "1/16"
        elif partial_amount > "06" and partial_amount <= "13":
            self.partial_volumetric = "1/8"
        elif partial_amount > "13" and partial_amount <= "25":
            self.partial_volumetric = "1/4"
        elif partial_amount > "25" and partial_amount <= "43":
            self.partial_volumetric = "1/3"
        elif partial_amount > "44" and partial_amount <= "60":
            self.partial_volumetric = "1/2"
        elif partial_amount > "60" and partial_amount <= "67":
            self.partial_volumetric = "2/3"
        elif partial_amount > "67" and partial_amount <= "85":
            self.partial_volumetric = "3/4"
        else:
            # If partial volume is more than 0.86 cups, add to whole volume
            self.partial_volumetric = "1"
            
        return self.partial_volumetric