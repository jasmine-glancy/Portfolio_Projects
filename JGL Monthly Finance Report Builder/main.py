"""A program that scans the excel charge logs for each shift
to build an emailed report of the top focus areas for training"""

# Import databases

import billing_codes
from charge_reports import CHARGE_REPORTS_SESSION, WeekdayCharges2024, WeekendCharges2024, WeeknightCharges2024
from helpers import build_report_overcharges, find_f_thru_m_overcharges, find_t_thru_f_am_overcharges, find_m_thru_th_pm_overcharges
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

# Create shift iterables from charge reports 
weekday_charges = charge_session.query(WeekdayCharges2024).all()
weeknight_charges = charge_session.query(WeeknightCharges2024).all()
weekend_charges = charge_session.query(WeekendCharges2024).all()

# Test code below
# for code in inj_med_codes:
#     print(f"Item ID: {code.item_id}, Item Code: {code.item_code}, Description: {code.item_description}")

# counter = 0
# # charge_report = charge_session.query(WeeknightCharges2024).all()

# for code in weekday_charges:
#         print(f"Code ID: {code.Charge_ID}, Item: {code.Item}, Notes: {code.Notes}",
#               f"Amount Subtracted: {code.Amount_Subtracted}, Entered Code: {code.Entered_Code}",
#               f"Amount Added: {code.Amount_Added}, Correct Code: {code.Correct_Code}")
        
#         counter += 1
        
#         if counter == 10:
#             break
        
        
# Count and classify recurring item totals

# ----------------------------- Weekday Charges ----------------------------- #

weekday_over_charged_items = find_t_thru_f_am_overcharges()

print("Weekday charges tallying...")

# Weekday over-charges
weekday_over_charge_list = build_report_overcharges(weekday_over_charged_items, flattened_code_list)
print(weekday_over_charge_list)

# ----------------------------- Weeknight Charges ----------------------------- #

weeknight_over_charged_items = find_m_thru_th_pm_overcharges()

print("Weeknight charges tallying...")

# Weeknight over-charges
weeknight_over_charge_list = build_report_overcharges(weeknight_over_charged_items, flattened_code_list)
print(weeknight_over_charge_list)

# ----------------------------- Weekend Charges ----------------------------- #

weekend_over_charged_items = find_f_thru_m_overcharges()

print("Weekend charges tallying...")

# Weekend over-charges
weekend_over_charge_list = build_report_overcharges(weekend_over_charged_items, flattened_code_list)
print(weekend_over_charge_list)

    
    # TODO: Final report should have 5 most missed and/or altered charges
    
# TODO: Include focus categories?

    # TODO: Compare billing code database items with reports

# TODO: Include shift totals

# TODO: Include YTD totals per shift

# TODO: Save report as a PDF

# TODO: Email report?
