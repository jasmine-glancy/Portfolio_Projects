"""A program that scans the excel charge logs for each shift
to build an emailed report of the top focus areas for training"""

# Import databases

import billing_codes
from charge_reports import CHARGE_REPORTS_SESSION, WeekdayCharges2024, WeekendCharges2024, WeeknightCharges2024

# Create billing code session for queries
codes_session = billing_codes.BILLING_CODES_SESSION 

# Create charge report session for queries
charge_session = CHARGE_REPORTS_SESSION

billing_codes = codes_session.query(billing_codes.HospitalizationCodes).all()

# Test code below
# for code in billing_codes:
#     print(f"Item ID: {code.item_id}, Item Code: {code.item_code}, Description: {code.item_description}")


# counter = 0
# charge_report = charge_session.query(WeeknightCharges2024).all()

# for code in charge_report:
#         print(f"Code ID: {code.Charge_ID}, Item: {code.Item}, Notes: {code.Notes}",
#               f"Amount Subtracted: {code.Amount_Subtracted}, Entered Code: {code.Entered_Code}",
#               f"Amount Added: {code.Amount_Added}, Correct Code: {code.Correct_Code}")
        
#         counter += 1
        
#         if counter == 10:
#             break

# TODO: Count over- and under- charge columns

    # TODO: Count and classify recurring item totals
    
    # TODO: Final report should have 5 most missed and/or altered charges
    
# TODO: Include focus categories?

    # TODO: Compare billing code database items with reports

# TODO: Include shift totals

# TODO: Include YTD totals per shift

# TODO: Save report as a PDF

# TODO: Email report?
