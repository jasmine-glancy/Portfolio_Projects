"""In charge of querying the database"""

from charge_reports import CHARGE_REPORTS_SESSION, WeekdayCharges2024, WeekendCharges2024, WeeknightCharges2024
from sqlalchemy import desc, func


# Create charge report session for queries
charge_session = CHARGE_REPORTS_SESSION

def find_t_thru_f_am_over_charges():
    """Finds the most commonly occurring 
    over-charged items on the weekdays"""
    
    over_charged_items = charge_session.query(
        WeekdayCharges2024.Entered_Code,
        WeekdayCharges2024.Item, 
        func.count(WeekdayCharges2024.Entered_Code).label("count_overcharged")
    ).group_by(WeekdayCharges2024.Entered_Code,
            WeekdayCharges2024.Item
            ).order_by(desc("count_overcharged")).limit(5)
    
    return over_charged_items

def find_t_thru_f_am_under_charges():
    """Finds the most commonly occurring 
    under-charged items on the weekdays"""
    
    under_charged_items = charge_session.query(
        WeekdayCharges2024.Correct_Code,
        WeekdayCharges2024.Item, 
        func.count(WeekdayCharges2024.Correct_Code).label("count_under_charged")
    ).group_by(WeekdayCharges2024.Correct_Code,
            WeekdayCharges2024.Item
            ).order_by(desc("count_under_charged")).limit(5)
    
    return under_charged_items

def find_m_thru_th_pm_over_charges():
    """Finds the most commonly occurring 
    over-charged items on the weeknights"""
    
    over_charged_items = charge_session.query(
        WeeknightCharges2024.Entered_Code,
        WeeknightCharges2024.Item, 
        func.count(WeeknightCharges2024.Entered_Code).label("count_overcharged")
    ).group_by(WeeknightCharges2024.Entered_Code,
            WeeknightCharges2024.Item
            ).order_by(desc("count_overcharged")).limit(5)
    
    return over_charged_items

def find_m_thru_th_pm_under_charges():
    """Finds the most commonly occurring 
    under-charged items on the weeknights"""
    
    under_charged_items = charge_session.query(
        WeeknightCharges2024.Correct_Code,
        WeeknightCharges2024.Item, 
        func.count(WeeknightCharges2024.Correct_Code).label("count_under_charged")
    ).group_by(WeeknightCharges2024.Correct_Code,
            WeeknightCharges2024.Item
            ).order_by(desc("count_under_charged")).limit(5)
    
    return under_charged_items

def find_f_thru_m_over_charges():
    """Finds the most commonly occurring 
    over-charged items on the weekends"""
    
    over_charged_items = charge_session.query(
        WeekendCharges2024.Entered_Code,
        WeekendCharges2024.Item, 
        func.count(WeekendCharges2024.Entered_Code).label("count_overcharged")
    ).group_by(WeekendCharges2024.Entered_Code,
            WeekendCharges2024.Item
            ).order_by(desc("count_overcharged")).limit(5)
    
    return over_charged_items

def find_f_thru_m_under_charges():
    """Finds the most commonly occurring 
    under-charged items on the weekends"""
    
    under_charged_items = charge_session.query(
        WeekendCharges2024.Correct_Code,
        WeekendCharges2024.Item, 
        func.count(WeekendCharges2024.Correct_Code).label("count_under_charged")
    ).group_by(WeekendCharges2024.Correct_Code,
            WeekendCharges2024.Item
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