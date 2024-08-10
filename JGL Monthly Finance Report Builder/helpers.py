"""In charge of querying the database"""

import billing_codes
from charge_reports import CHARGE_REPORTS_SESSION, WeekdayCharges2024, WeekendCharges2024, WeeknightCharges2024
from sqlalchemy import desc, func
import staff_initals
from tabulate import tabulate

# Create billing code session for queries
codes_session = billing_codes.BILLING_CODES_SESSION 

# Create staff initial session for queries
staff_session = staff_initals.STAFF_INITIALS_SESSION

# Create charge report session for queries
charge_session = CHARGE_REPORTS_SESSION

def find_over_charges(shift):
    """Finds the most commonly occurring 
    over-charged items"""
    
    # Return the table for the respective shift
    shift_db = return_database(shift)
    
    over_charged_items = charge_session.query(
        shift_db.Entered_Code,
        shift_db.Item, 
        func.count(shift_db.Entered_Code).label("count_overcharged")
    ).group_by(shift_db.Entered_Code,
            shift_db.Item
            ).order_by(desc("count_overcharged")).limit(5)
    
    return over_charged_items

def find_under_charges(shift):
    """Finds the most commonly occurring 
    missed items not charged for"""
    
    # Return the table for the respective shift
    shift_db = return_database(shift)
    
    under_charged_items = charge_session.query(
        shift_db.Correct_Code,
        shift_db.Item, 
        func.count(shift_db.Correct_Code).label("count_under_charged")
    ).group_by(shift_db.Correct_Code,
            shift_db.Item
            ).order_by(desc("count_under_charged")).limit(5)
    
    return under_charged_items
 

def build_report_over_charges(shift, code_list):
    """Builds a report of the most commonly occurring over-charges"""
    
    over_charge_report = ""
    
    for i, (code, notes, count_overcharged) in enumerate(shift, start=1):
    # Enumerate allows you to increment the counted numbers
        
        code_description = None
        
        for item in code_list:
            # Checks if the code in the top overcharged items 
            ## matches a billing code within a category
            if code == item.item_code:
                code_description = item.item_description
                break
            
        # TODO: If nursing code matches hospitalization code, only count them once
        
        if code_description:
            # If there's a code description, call it
            over_charge_report += f"{i}. Code: {code_description}, Count: {count_overcharged}\n"
        else:
            over_charge_report += f"{i}. Code: {notes}, Count: {count_overcharged}\n"

    return over_charge_report

def build_report_under_charges(shift, code_list):
    """Builds a report of the most commonly occurring over-charges"""
    
    under_charge_report = ""
    
    for i, (code, notes, count_under_charged) in enumerate(shift, start=1):
    # Enumerate allows you to increment the counted numbers
        
        code_description = None
        
        for item in code_list:
            # Checks if the code in the top overcharged items 
            ## matches a billing code within a category
            if code == item.item_code:
                code_description = item.item_description
                break
            
        if code_description:
            # If there's a code description, call it
            under_charge_report += f"{i}. Code: {code_description}, Count: {count_under_charged}\n"
        else:
            under_charge_report += f"{i}. Code: {notes}, Count: {count_under_charged}\n"

    return under_charge_report

def build_report_over_charge_total(shift):
    """Reports the total amount over charged"""
    
    # Return the table for the respective shift
    shift_db = return_database(shift)
        
    records = charge_session.query(shift_db).all()
    over_charges = 0
    
    for record in records:
        try:
            if record.Amount_Subtracted:  
                over_charges += record.Amount_Subtracted
        except Exception:
            amt_subtr = record.Amount_Subtracted.replace("$", "").replace(",", "").replace("-", "").replace("--", "")
            if amt_subtr:  
                over_charges += float(amt_subtr)
    over_charges = round(over_charges, 2)  
    formatted_over_charges = f"{over_charges:,.2f}"
    
    return formatted_over_charges


def build_report_under_charge_total(shift):
    """Reports the total amount of missed charges"""
    
    # Return the table for the respective shift
    shift_db = return_database(shift)

    records = charge_session.query(shift_db).all()
    missed_charges = 0
    
    for record in records:
        try:
            if record.Amount_Added:  
                missed_charges += record.Amount_Added
        except Exception:
            amt_added = record.Amount_Added.replace("$", "").replace(",", "").replace("-", "").replace("--", "")
            
            if amt_added:
                missed_charges += float(amt_added)  
            
    missed_charges = round(missed_charges, 2)  
    formatted_missed_charges = f"{missed_charges:,.2f}"
    
    return formatted_missed_charges

def charge_difference(shift):
    """Finds the difference between missed and over charges"""
    
    over_charge_total = build_report_over_charge_total(shift).replace(",", "")
    under_charge_total = build_report_under_charge_total(shift).replace(",", "")
    
    difference = float(over_charge_total) - float(under_charge_total)
    
    if difference < 0:
        formatted_difference = f"(-${abs(difference):,.2f})"
    else:
        formatted_difference = f"${difference:,.2f}"
    
    return formatted_difference

def find_charges_missed_by_dr(shift):
    
    # Return the table for the respective shift
    shift_db = return_database(shift)
    
        # Debug: Print some sample data from the shift_db table
    charge_log = charge_session.query(shift_db).all()

    most_missed_by_dr = {}
    
    for charge in charge_log:

        if charge.Correct_Code and charge.Entered_Code != "---" or charge.Correct_Code and not charge.Entered_Code:
            if charge.Doctor in most_missed_by_dr:
                # If the doctor is in the dictionary already, add a count to the tally
                most_missed_by_dr[charge.Doctor] += 1
            else:
                # Otherwise, add them to the dictionary for the first time
                most_missed_by_dr[charge.Doctor] = 1
    
    
    # Sort the dictionary by missed charges count in descending order
    sorted_missed_charges = sorted(most_missed_by_dr.items(), key=lambda x: x[1], reverse=True)
    
    # Select the top 3 doctors with the most missed charges
    top_3_missed_charges = sorted_missed_charges[:3]
    
    return top_3_missed_charges

def build_report_missed_by_dr(shift, staff_list):
    """Builds a report of the top 3 most missed 
    charges by staff member"""
    
    top_3_staff_w_missed_charges = ""
    
    for i, (initials, count_missed) in enumerate(shift, start=1):
        staff_name = None
        
        for name in staff_list:
            # Checks the staff column of the charge report
            ## database against the staff database to find their full name
            
            if name.cs_initials == initials:
                if name.notes:
                    staff_name = f"{name.first_name} {name.last_name}, {name.notes}"
                else: 
                    staff_name = f"{name.first_name} {name.last_name}"
                break
            
        if staff_name:
            # If the name is in the staff database, 
            # # call the full name
            
            top_3_staff_w_missed_charges += f"{i}. Staff Member: {staff_name}, Count: {count_missed} \n"
            
        else:
            # Otherwise count the initials
            top_3_staff_w_missed_charges += f"{i}. Staff Member: {initials}, Count: {count_missed} \n"
        
    return top_3_staff_w_missed_charges

def find_charges_altered_by_dr(shift):
    
    # Return the table for the respective shift
    shift_db = return_database(shift)
    
        # Debug: Print some sample data from the shift_db table
    charge_log = charge_session.query(shift_db).all()

    most_altered_by_dr = {}
    
    for charge in charge_log:

        if charge.Correct_Code and charge.Entered_Code:
            if charge.Doctor in most_altered_by_dr:
                # If the doctor is in the dictionary already, add a count to the tally
                most_altered_by_dr[charge.Doctor] += 1
            else:
                # Otherwise, add them to the dictionary for the first time
                most_altered_by_dr[charge.Doctor] = 1
    
    
    # Sort the dictionary by missed charges count in descending order
    sorted_altered_charges = sorted(most_altered_by_dr.items(), key=lambda x: x[1], reverse=True)
    
    # Select the top 3 doctors with the most missed charges
    top_3_altered_charges = sorted_altered_charges[:3]
    
    return top_3_altered_charges

def build_report_altered_by_dr(shift, staff_list):
    """Builds a report of the top 3 most altered 
    charges by staff member"""
    
    top_3_staff_w_altered_charges = ""
    
    for i, (initials, count_altered) in enumerate(shift, start=1):
        staff_name = None
        
        for name in staff_list:
            # Checks the staff column of the charge report
            ## database against the staff database to find their full name
            
            if name.cs_initials == initials:
                if name.notes:
                    staff_name = f"{name.first_name} {name.last_name}, {name.notes}"
                else: 
                    staff_name = f"{name.first_name} {name.last_name}"
                break
            
        if staff_name:
            # If the name is in the staff database, 
            # # call the full name
            
            top_3_staff_w_altered_charges += f"{i}. Staff Member: {staff_name}, Count: {count_altered} \n"
            
        else:
            # Otherwise count the initials
            top_3_staff_w_altered_charges += f"{i}. Staff Member: {initials}, Count: {count_altered} \n"
        
    return top_3_staff_w_altered_charges

def return_database(shift):
    """Returns the table name for each shift"""
    
    if shift == "weekend":
        db = WeekendCharges2024
    elif shift == "weekday":
        db = WeekdayCharges2024
    elif shift == "weeknight":
        db = WeeknightCharges2024
        
    return db


def create_code_list():
    """Create a flattened list of all billing codes
    by category"""
    # Create billing code iterables
    transfusion_codes = codes_session.query(billing_codes.BloodAndTransfusion).all()
    consultation_transfer_codes = codes_session.query(billing_codes.ConsultationsAndTransfers).all()
    controlled_drug_codes = codes_session.query(billing_codes.ControlledDrugs).all()
    fluid_additive_codes = codes_session.query(billing_codes.FluidAdditives).all()
    food_codes = codes_session.query(billing_codes.Food).all()
    hospitalization_codes = codes_session.query(billing_codes.HospitalizationCodes).all()
    ih_imaging_codes = codes_session.query(billing_codes.InHouseImaging).all()
    ih_lab_codes = codes_session.query(billing_codes.InHouseLabs).all()
    inj_med_codes = codes_session.query(billing_codes.InjectibleMedications).all()
    monitoring_codes = codes_session.query(billing_codes.Monitoring).all()
    oxygen_codes = codes_session.query(billing_codes.Oxygen).all()
    send_out_lab_codes = codes_session.query(billing_codes.SendOut_ReferenceLabs).all()
    specialty_imaging_codes = codes_session.query(billing_codes.SpecialtyImaging).all()

    code_list = [transfusion_codes, consultation_transfer_codes, controlled_drug_codes,
                fluid_additive_codes, food_codes, hospitalization_codes, ih_imaging_codes,
                ih_lab_codes, inj_med_codes, monitoring_codes, oxygen_codes, send_out_lab_codes, 
                specialty_imaging_codes]

    # Flatten code list, suggested by CoPilot
    flattened_code_list = [code for category in code_list for code in category]
    
    return flattened_code_list

def create_staff_list():
    """Create a flattened list of all staff members"""
    
    # Create staff initial iterables
    dvm_codes = staff_session.query(staff_initals.Doctors).all()
    staff_codes = staff_session.query(staff_initals.Staff).all()
    
    staff_list = [dvm_codes, staff_codes]
    
    # Iterate over each staff member in each category in staff list
    flattened_staff_list = [staff_member for rank in staff_list for staff_member in rank]

    return flattened_staff_list