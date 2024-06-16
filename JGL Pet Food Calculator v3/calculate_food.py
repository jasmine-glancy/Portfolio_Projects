"""Contains the pet food calculator"""

from cs50 import SQL
from flask import session, flash
from find_info import FindInfo


# Configure CS50 Library to use SQLite database (for login checks)
db = SQL("sqlite:///pet_food_calculator.db")

# TODO: Move RER and DER to a different file v2
class CalculateFood():
    def __init__(self, user_id, pet_id=None):
        """Query the pet's info for calculation"""
        
        self.fi = FindInfo(user_id)
        
        try:
            if user_id != 0 and pet_id != 0:
                # If the user is logged in and there is a pet ID, call data dictionary
                self.pet_data = self.fi.pet_data_dictionary(user_id, pet_id)
            else:
                # If there isn't a pet ID or a user ID greater than 0, call guest
                self.pet_data = self.fi.guest_pet_data_dictionary(user_id, pet_id)

        except Exception as e:
            # Otherwise, raise exception and pass session variables
            flash(f"Unable to lookup pet data. Exception: {e}")
            
        self.calculcate_rer()
        
    def calculcate_rer(self):
        """Calculates the minimum number of calories a pet needs at rest per day"""
            
        print(self.pet_data[0]["weight"], self.pet_data[0]["units"])
            
        # Convert lbs weighs to kgs
        if self.pet_data[0]["units"] == "lbs":
            self.pet_data[0]["weight"] = self.pet_data[0]["weight"] / 2.2
            self.pet_data[0]["units"] = "kgs"
            
        print(self.pet_data[0]["weight"], self.pet_data[0]["units"])
            
        self.rer = int(70 * self.pet_data[0]["weight"]**0.75)
                
        print(self.rer) 
        session["rer"] = self.rer
        
        return self.rer


    def calculcate_der(self, species=None, der_factor_id=None):
        """Calculates daily caloric needs based on life stage"""
        
        # Use DER factor id to lookup DER information by species
        self.der_modifier_start_range = self.fi.find_der_low_end(species, der_factor_id)
        self.der_modifier_end_range = self.fi.find_der_high_end(species, der_factor_id)

        # Start with the mid range if this is the first report
        # TODO: check report date and change modifier choice based on weight changes
        self.der_modifier = self.fi.find_der_mid_range(species, der_factor_id)

        # Calculate DER based on the der modifier and pass variables to tempate
        if species == "Feline" and self.pet_data[0]["is_nursing"] == "y":
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
        if partial_amount == "0":
            self.partial_volumetric = "0"
        elif partial_amount > "0" and partial_amount <= "03":
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
    
