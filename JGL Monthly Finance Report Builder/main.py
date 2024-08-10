"""A program that scans the excel charge logs for each shift
to build an emailed report of the top focus areas for training"""

import helpers

# Create list of billing code queries for searching
flattened_code_list = helpers.create_code_list()

# Create list of staff names for searching
staff_list = helpers.create_staff_list()

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

print("--- Weekday charge total ---\n")
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


print("--- Weekday charge breakdown by staff ---\n")
print("Charges most missed by staff:")
print(top_3_missed_weekday_by_dr)
print("Charges most altered by staff:")
print(top_3_altered_weekday_by_dr)

print("--- Weeknight charge total ---\n")
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

print("--- Weeknight charge breakdown by staff ---\n")
print("Charges most missed by staff:")
print(top_3_missed_weeknight_by_dr)
print("Charges most altered by staff:")
print(top_3_altered_weeknight_by_dr)


print("--- Weekend charge total ---\n")
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

print("--- Weekend charge breakdown by staff ---\n")
print("Charges most missed by staff:")
print(top_3_missed_weekend_by_dr)
print("Charges most altered by staff:")
print(top_3_altered_weekend_by_dr)
