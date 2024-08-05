"""A program that scans the excel charge logs for each shift
to build an emailed report of the top focus areas for training"""

# Import databases

import billing_codes
from charge_reports import CHARGE_REPORTS_SESSION, WeekdayCharges2024, \
    WeekendCharges2024, WeeknightCharges2024
from helpers import build_report_over_charges, build_report_under_charges, \
    build_report_over_charge_total, build_report_under_charge_total, charge_difference, \
        find_f_thru_m_over_charges, find_f_thru_m_under_charges, \
            find_t_thru_f_am_over_charges, find_t_thru_f_am_under_charges, \
                find_m_thru_th_pm_over_charges, find_m_thru_th_pm_under_charges

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

weekday_over_charged_items = find_t_thru_f_am_over_charges()
weekday_under_charged_items = find_t_thru_f_am_under_charges()

print("---------------- Weekday charges tallying ----------------\n")

# Weekday under-charges
weekday_under_charge_list = build_report_under_charges(weekday_under_charged_items, flattened_code_list)
print("Missed Item Charges: \n")
print(weekday_under_charge_list)

# Weekday over-charges
weekday_over_charge_list = build_report_over_charges(weekday_over_charged_items, flattened_code_list)
print("Over-charged Items: \n")
print(weekday_over_charge_list)


# ----------------------------- Weeknight Charges ----------------------------- #

weeknight_over_charged_items = find_m_thru_th_pm_over_charges()
weeknight_under_charged_items = find_m_thru_th_pm_under_charges()

print("---------------- Weeknight charges tallying ----------------\n")

# Weeknight under-charges
weeknight_under_charge_list = build_report_under_charges(weeknight_under_charged_items, flattened_code_list)
print("Missed Item Charges: \n")
print(weeknight_under_charge_list)

# Weeknight over-charges
weeknight_over_charge_list = build_report_over_charges(weeknight_over_charged_items, flattened_code_list)
print("Over-charged Items: \n")
print(weeknight_over_charge_list)

# ----------------------------- Weekend Charges ----------------------------- #

weekend_over_charged_items = find_f_thru_m_over_charges()
weekend_under_charged_items = find_f_thru_m_under_charges()

print("---------------- Weekend charges tallying ----------------\n")

# Weeknight under-charges
weekend_under_charge_list = build_report_under_charges(weekend_under_charged_items, flattened_code_list)
print("Missed Item Charges: \n")
print(weekend_under_charge_list)

# Weekend over-charges
weekend_over_charge_list = build_report_over_charges(weekend_over_charged_items, flattened_code_list)
print("Over-charged Items: \n")
print(weekend_over_charge_list)

# ------------------------- Missed charges per shift ------------------------- #
print("------------------------- Charge breakdown per shift -------------------------\n")

print("--- Weekday missed charges ---\n")
weekday_missed_charges = build_report_under_charge_total("weekday")
weekday_over_charges = build_report_over_charge_total("weekday")
weekday_diff = charge_difference("weekday")

print(f"Missed charges: ${weekday_missed_charges}")
print(f"Over charges: ${weekday_over_charges}")
print(f"Difference: {weekday_diff}\n")

print("--- Weeknight missed charges ---\n")
weeknight_missed_charges = build_report_under_charge_total("weeknight")
weeknight_over_charges = build_report_over_charge_total("weeknight")
weeknight_diff = charge_difference("weeknight")

print(f"Missed charges: ${weeknight_missed_charges}")
print(f"Over charges: ${weeknight_over_charges}")
print(f"Difference: {weeknight_diff}\n")

print("--- Weekend missed charges ----\n")
weekend_missed_charges = build_report_under_charge_total("weekend")
weekend_over_charges = build_report_over_charge_total("weekend")
weekend_diff = charge_difference("weekend")

print(f"Missed charges: ${weekend_missed_charges}")
print(f"Over charges: ${weekend_over_charges}")
print(f"Difference: {weekend_diff}\n")

# TODO: Include YTD totals per shift

# TODO: Save report as a PDF

# TODO: Email report?
