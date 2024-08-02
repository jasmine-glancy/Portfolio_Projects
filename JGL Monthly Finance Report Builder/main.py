"""A program that scans the excel charge logs for each shift
to build an emailed report of the top focus areas for training"""

# Import databases

import billing_codes
from charge_reports import CHARGE_REPORTS_SESSION, WeekdayCharges2024, WeekendCharges2024, WeeknightCharges2024
from sqlalchemy import desc, func

# Create billing code session for queries
codes_session = billing_codes.BILLING_CODES_SESSION 

# Create charge report session for queries
charge_session = CHARGE_REPORTS_SESSION


# Create billing code iterables
transfusion_codes = codes_session.query(billing_codes.BloodAndTransfusion).all()
consultation_transfer_codes = codes_session.query(billing_codes.ConsultationsAndTransfers).all()
controlled_drug_codes = codes_session.query(billing_codes.ControlledDrugs).all()
fluid_additive_codes = codes_session.query(billing_codes.FluidAdditives).all()
food_codes = codes_session.query(billing_codes.Food).all()
hospitalization_codes = codes_session.query(billing_codes.HospitalizationCodes).all()
ih_imaging_codes = codes_session.query(billing_codes.InHouseImaging).all()
ih_lab_codes = codes_session.query(billing_codes.InHouseLabs).all()
monitoring_codes = codes_session.query(billing_codes.Monitoring).all()
oxygen_codes = codes_session.query(billing_codes.Oxygen).all()
send_out_lab_codes = codes_session.query(billing_codes.SendOut_ReferenceLabs).all()
specialty_imaging_codes = codes_session.query(billing_codes.SpecialtyImaging).all()

code_list = [transfusion_codes, consultation_transfer_codes, controlled_drug_codes,
             fluid_additive_codes, food_codes, hospitalization_codes, ih_imaging_codes,
             ih_lab_codes, monitoring_codes, oxygen_codes, send_out_lab_codes, specialty_imaging_codes]

# Flatten code list, suggested by CoPilot
flattened_code_list = [code for category in code_list for code in category]

# Create shift iterables from charge reports 
weekday_charges = charge_session.query(WeekdayCharges2024).all()
weeknight_charges = charge_session.query(WeeknightCharges2024).all()
weekend_charges = charge_session.query(WeekendCharges2024).all()

# Test code below
# for code in hospitalization_codes:
#     print(f"Item ID: {code.item_id}, Item Code: {code.item_code}, Description: {code.item_description}")

counter = 0
# charge_report = charge_session.query(WeeknightCharges2024).all()

for code in weekday_charges:
        print(f"Code ID: {code.Charge_ID}, Item: {code.Item}, Notes: {code.Notes}",
              f"Amount Subtracted: {code.Amount_Subtracted}, Entered Code: {code.Entered_Code}",
              f"Amount Added: {code.Amount_Added}, Correct Code: {code.Correct_Code}")
        
        counter += 1
        
        if counter == 10:
            break
        
        
# TCount and classify recurring item totals

# Weekday Charges

# Weekend Charges

# Weeknight Charges
over_charged_items = charge_session.query(
    WeeknightCharges2024.Entered_Code, 
    func.count(WeeknightCharges2024.Entered_Code).label("count_overcharged")
).group_by(WeeknightCharges2024.Entered_Code).order_by(desc("count_overcharged")).limit(5)

print("Weeknight charges tallying...")
for i, (code, count_overcharged) in enumerate(over_charged_items, start=1):
    # Enumerate allows you to increment the counted numbers
    
    code_description = None
    
    for item in flattened_code_list:
        # Checks if the code in the top overcharged items 
        ## matches a billing code within a category
        if code == item.item_code:
            code_description = item.item_description
            break
        
    if code_description:
        # If there's a code description, call it
        print(f"{i}. Code: {code_description}, Count: {count_overcharged}")
    else:
        print(f"{i}. Code: {code}, Count: {count_overcharged}")

    
    
    # TODO: Final report should have 5 most missed and/or altered charges
    
# TODO: Include focus categories?

    # TODO: Compare billing code database items with reports

# TODO: Include shift totals

# TODO: Include YTD totals per shift

# TODO: Save report as a PDF

# TODO: Email report?
