"""In charge of querying the database"""

from charge_reports import CHARGE_REPORTS_SESSION, WeekdayCharges2024, WeekendCharges2024, WeeknightCharges2024
from sqlalchemy import desc, func
from tabulate import tabulate


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
    
    most_missed_by_dr = charge_session.query(
        shift_db.Doctor, 
        func.count(shift_db.Doctor).label("count_missed")
    ).filter(
        # Only add to the count if there is data in Correct_Code
        ## and not in Entered_Code
        shift_db.Correct_Code.isnot(None),
        shift_db.Correct_Code != "",
        (shift_db.Entered_Code.is_(None) | (shift_db.Entered_Code == ""))
    ).group_by(
            shift_db.Doctor
    ).order_by(
        desc("count_missed")
        ).limit(3)
    
        # Debug: Print the generated SQL query
    print(f"Generated SQL query: {most_missed_by_dr}")
    
    result = most_missed_by_dr.all()
    missed_drs = ""
    
    for i, (doctor, count_missed) in enumerate(result, start=1):
        # Enumerate allows you to increment the counted numbers
        missed_drs += f"{i}. Doctor: {doctor}, Count: {count_missed}\n"

    # Print the results in a formatted way
    table_data = [(correct_code, count_missed) for correct_code, count_missed in result]
    headers = ["Doctor", "Missed Charges"]
    
    
    print(tabulate(table_data, headers, tablefmt="grid"))
    
    return missed_drs
   
def return_database(shift):
    """Returns the table name for each shift"""
    
    if shift == "weekend":
        db = WeekendCharges2024
    elif shift == "weekday":
        db = WeekdayCharges2024
    elif shift == "weeknight":
        db = WeeknightCharges2024
        
    return db