"""A program that scans the excel charge logs for each shift
to build an emailed report of the top focus areas for training"""

# Import databases

from charge_reports import CHARGE_REPORTS_SESSION, WeekdayCharges2024, \
    WeekendCharges2024, WeeknightCharges2024
import helpers

# Create charge report session for queries
charge_session = CHARGE_REPORTS_SESSION

# Create list of billing code queries for searching
flattened_code_list = helpers.create_code_list()

# Create list of staff names for searching
staff_list = helpers.create_staff_list()

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

weekday_over_charged_items = helpers.find_over_charges("weekday")
weekday_under_charged_items = helpers.find_under_charges("weekday")

print("---------------- Weekday charges tallying ----------------\n")

# Weekday under-charges
weekday_under_charge_list = helpers.build_report_under_charges(weekday_under_charged_items, flattened_code_list)
print("Missed Item Charges: \n")
print(weekday_under_charge_list)

# Weekday over-charges
weekday_over_charge_list = helpers.build_report_over_charges(weekday_over_charged_items, flattened_code_list)
print("Over-charged Items: \n")
print(weekday_over_charge_list)


# ----------------------------- Weeknight Charges ----------------------------- #

weeknight_over_charged_items = helpers.find_over_charges("weeknight")
weeknight_under_charged_items = helpers.find_under_charges("weeknight")

print("---------------- Weeknight charges tallying ----------------\n")

# Weeknight under-charges
weeknight_under_charge_list = helpers.build_report_under_charges(weeknight_under_charged_items, flattened_code_list)
print("Missed Item Charges: \n")
print(weeknight_under_charge_list)

# Weeknight over-charges
weeknight_over_charge_list = helpers.build_report_over_charges(weeknight_over_charged_items, flattened_code_list)
print("Over-charged Items: \n")
print(weeknight_over_charge_list)

# ----------------------------- Weekend Charges ----------------------------- #

weekend_over_charged_items = helpers.find_over_charges("weekend")
weekend_under_charged_items = helpers.find_under_charges("weekend")

print("---------------- Weekend charges tallying ----------------\n")

# Weeknight under-charges
weekend_under_charge_list = helpers.build_report_under_charges(weekend_under_charged_items, flattened_code_list)
print("Missed Item Charges: \n")
print(weekend_under_charge_list)

# Weekend over-charges
weekend_over_charge_list = helpers.build_report_over_charges(weekend_over_charged_items, flattened_code_list)
print("Over-charged Items: \n")
print(weekend_over_charge_list)

# ------------------------- Missed charges per shift ------------------------- #
print("------------------------- Charge breakdown per shift -------------------------\n")

print("--- Weekday missed charges ---\n")
weekday_missed_charges = helpers.build_report_under_charge_total("weekday")
weekday_over_charges = helpers.build_report_over_charge_total("weekday")
weekday_diff = helpers.charge_difference("weekday")
weekday_missed_by_dr = helpers.find_charges_missed_by_dr("weekday")
weekday_altered_by_dr = helpers.find_charges_altered_by_dr("weekday")
top_3_missed_weekday_by_dr = helpers.build_report_missed_by_dr(weekday_missed_by_dr, staff_list)
top_3_altered_weekday_by_dr = helpers.build_report_altered_by_dr(weekday_altered_by_dr, staff_list)

# Print weekday reports
print(f"Missed charges: ${weekday_missed_charges}")
print(f"Over charges: ${weekday_over_charges}")
print(f"Difference: {weekday_diff}\n")
print("Charges most missed by staff:")
print(top_3_missed_weekday_by_dr)
print("Charges most altered by staff:")
print(top_3_altered_weekday_by_dr)

print("--- Weeknight missed charges ---\n")
weeknight_missed_charges = helpers.build_report_under_charge_total("weeknight")
weeknight_over_charges = helpers.build_report_over_charge_total("weeknight")
weeknight_diff = helpers.charge_difference("weeknight")
weeknight_missed_by_dr = helpers.find_charges_missed_by_dr("weeknight")
weeknight_altered_by_dr = helpers.find_charges_altered_by_dr("weeknight")
top_3_missed_weeknight_by_dr = helpers.build_report_missed_by_dr(weeknight_missed_by_dr, staff_list)
top_3_altered_weeknight_by_dr = helpers.build_report_altered_by_dr(weeknight_altered_by_dr, staff_list)

# Print weeknight reports
print(f"Missed charges: ${weeknight_missed_charges}")
print(f"Over charges: ${weeknight_over_charges}")
print(f"Difference: {weeknight_diff}\n")
print("Charges most missed by staff:")
print(top_3_missed_weeknight_by_dr)
print("Charges most altered by staff:")
print(top_3_altered_weeknight_by_dr)

print("--- Weekend missed charges ----\n")
weekend_missed_charges = helpers.build_report_under_charge_total("weekend")
weekend_over_charges = helpers.build_report_over_charge_total("weekend")
weekend_diff = helpers.charge_difference("weekend")
weekend_missed_by_dr = helpers.find_charges_missed_by_dr("weekend")
weekend_altered_by_dr = helpers.find_charges_altered_by_dr("weekend")
top_3_missed_weekend_by_dr = helpers.build_report_missed_by_dr(weekend_missed_by_dr, staff_list)
top_3_altered_weekend_by_dr = helpers.build_report_altered_by_dr(weekend_altered_by_dr, staff_list)

# Print weekend reports
print(f"Missed charges: ${weekend_missed_charges}")
print(f"Over charges: ${weekend_over_charges}")
print(f"Difference: {weekend_diff}\n")
print("Charges most missed by staff:")
print(top_3_missed_weekend_by_dr)
print("Charges most altered by staff:")
print(top_3_altered_weekend_by_dr)

