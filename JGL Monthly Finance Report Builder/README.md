# Assignment 17: Custom Automation

The portfolio project for day 98 of [100 Days of Code: The Complete Python Pro Bootcamp](https://www.udemy.com/course/100-days-of-code). The goal was to automate some aspect of our lives using Python.

I decided to build a text-based program that helps build a report containing the top missed and overcharges found during the daily audits of hospitalized patients at the veterinary hospital where I work.

## Shift Breakdown Tally

![A screen grab of the terminal. It reads "Weekday charges tallying" with the top 5 missed and over-charged items](charge_tally.png)

There are 3 shifts to be analyzed: the weekend, weeknight, and weekday shifts. Each shift will have a similar output to above with the shift it is counting for and the top 5 missed and over-charged items. Items from the monthly charge audit database are matched to any corresponding billing codes. If the billing code does not exist, the notes/description of the monthly charge audit is used instead.

## Charge Breakdown per Shift

![A screen grab of the terminal. It reads "Charge breakdown per shift" with the weekday charge totals with a staff breakdown](charge_report.png)

In addition to tallying the most missed and over-charged items, the report builder will report the amount of charges missed and over-charged in U.S. dollars in addition to the staff members with me most missed or altered charges on their shifts. The goal of this is to know who to follow up with to educate how to charge accurately in the future.

## Databases

Three databases are used, monthly_charges, billing_codes, and charge_reports. The schema are as follows:

### billing_codes.db

Contains several tables:

- BloodAndTransfusion: For all blood and transfusion-related item codes
- ConsultationsAndTransfers: For exam and transfer fee-related item codes
- ControlledDrugs: For all controlled drugs (i.e. Fentanyl, Butorphanol, etc)
- FluidAdditives: For fluid additives that may or may not be associated with a charge
- Food: For canned, dry, and liquid food options
- HospitalizationCodes: For hospitalization charges per shift, including the fluid per 12h charge and overnight fee
- InHouseImaging: For FAST scans and radiographs
- InHouseLabs: For diagnostics completed upstairs in the treatment area
- InjectibleMedications: For medications that can be given intravenously, intramuscularly, or subcutaneously
- Monitoring: For various singular monitoring charges (i.e. blood pressure) and their per-shift equivalents
- Oxygen: For charges associated with oxygen therapy
- SendOut_ReferenceLabs: For labs sent to outside labs (i.e. Antech, Idexx, MSU)
- SpecialtyImaging: For charges associated with imaging such as C.T., MRI, etc.

All tables have item_id as their unique primary key that autoincrements with each new addition.

### monthly_changes.db

Contains three tables based on their corresponding charge logs from inpatient invoice audits of the following shifts:

- WeekdayCharges2024: Contains charge logs from the weekday shift (Tue-Fri 9a-6p)
- WeeknightCharges2024: Contains charge logs from the weeknight shift (Mon-Thu 6p-3a)
- WeekendCharges2024: Contains charge logs from the weekend shift (Fri-Mon 12p-10p)

The schema for the tables is as follows:

- Charge_ID: An integer of unique primary key that autoincrements
- ChargeDate: A string containing the date the charge was "captured"/logged
- PatientID: An integer representing the patient's ID
- PatientName: A string containing the patient's name
- Doctor: A string containing the doctor's initials on the case at the time the charge was logged
- Item: A string containing the "unofficial" name of the charge that was captured
- Notes: A string containing information such as "missed", "didn't transfer", or notes on changes made
- Amount_Subtracted: A float representing the amount subtracted from the invoice in U.S. dollars
- Entered_Code: A string containing the entered billing code that was modified or removed from the invoice
- Amount_Added: A float representing the amount added from the invoice in U.S. dollars
- Correct_Code: A string containing the billing code that was added to the invoice

### staff_initials.db

Contains two tables, Doctors and Staff. The schema is as follows:

- dr_id/staff_id: Contains a unique integer that serves as the primary key
- cs_initials: A string containing the 3-letter initials representing a staff member in Cornerstone
- first_name: A string containing the staff member or doctor's first name
- last_name: A string containing the staff member or doctor's last name
- notes: A string containing notes about the staff member (DVM, RVT, LVT any specialty titles, etc.)

