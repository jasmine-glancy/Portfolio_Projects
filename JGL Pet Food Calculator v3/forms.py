from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, SelectField, IntegerField
from wtforms.validators import DataRequired


# Create a Flask Form for the patient's signalment
class NewSignalment(FlaskForm):
    patient_name = StringField("Pet's Name:", validators=[DataRequired()])
    patient_age = FloatField("Patient's Age in Years:", validators=[DataRequired()])
    patient_age_months = FloatField("Patient's Age in Months:", validators=[DataRequired()])
    patient_species = SelectField(u"Patient's Species:",
                                  choices=[("default", "Please make a selection"),
                                            ("canine", "Canine"),
                                            ("feline", "Feline")],
                                  validators=[DataRequired()],
                                  render_kw={"option": {"default": {"disabled": ""}},
                                             "id": "species"})
    patient_breed = SelectField(u"Patient's Breed:",
                                  choices=[("default", "Please make a selection")],
                                  validators=[DataRequired()],
                                  render_kw={"option": {"default": {"disabled": ""}},
                                            "id": "breed"})
    patient_sex = SelectField(u"Patient's Sex:",
                              choices=[("default", "Please make a selection"),
                              ("female", "Female (Intact)"),
                              ("female_spayed", "Female (Spayed)"),
                              ("male", "Male (Intact)"),
                              ("male_neutered", "Male (Neutered)")],
                              validators=[DataRequired()],
                              render_kw={"option": {"default": {"disabled": ""}},
                                         "id": "sex"})

# Obtain patient weight and BCS
class GetWeight(FlaskForm):
    patient_bcs = SelectField(u"Please Select Pet's Body Condition Score:", 
                                choices=[("default", "Please make a selection"),
                                         ("1", "BCS 1"),                            
                                         ("2", "BCS 2"),
                                         ("3", "BCS 3"),
                                         ("4", "BCS 4"),
                                         ("5", "BCS 5"),
                                         ("6", "BCS 6"),
                                         ("7", "BCS 7"),
                                         ("8", "BCS 8"),
                                         ("9", "BCS 9")],
                                validators=[DataRequired()],
                                render_kw={"default": {"disabled": ""}})
    patient_weight = StringField("Pet's Weight:", validators=[DataRequired()])
    patient_units = SelectField(u"Is the weight you entered in pounds (lb) or kilograms (kg)?", 
                                choices=[("default", "Please make a selection"),
                                         ("lbs", "Pounds"),                            
                                         ("kgs", "Kilograms")],
                                validators=[DataRequired()],
                                render_kw={"default": {"disabled": ""}})

# Obtain breeding and nursing status
class ReproStatus(FlaskForm):
    pregnancy_status = SelectField(u"Is Your Pet Currently Pregnant?:",
                                  choices=[("default", "Please make a selection"),
                                            ("y", "Yes"),
                                            ("n", "No")],
                                  validators=[DataRequired()],
                                  render_kw={"default": {"disabled": ""},
                                             "id": "pregnancy_status"})
    weeks_gestation = SelectField(u"How Many Weeks Has Your Pet Been Pregnant?:",
                                  choices=[("default", "Please make a selection"),
                                            ("0", "0"),
                                            ("1", "1"),
                                            ("2", "2"),
                                            ("3", "3"),
                                            ("4", "4"),
                                            ("5", "5"),
                                            ("6", "6"),
                                            ("7", "7"),
                                            ("8", "8"),
                                            ("9", "9"),
                                            ("10", "10")],
                                  render_kw={"default": {"disabled": ""},
                                             "id": "gestating"})
    nursing_status = SelectField(u"Is Your Pet Currently Nursing?:",
                                  choices=[("default", "Please make a selection"),
                                            ("y", "Yes"),
                                            ("n", "No")],
                                  render_kw={"default": {"disabled": ""},
                                             "id": "nursing_status"})
    litter_size = IntegerField(u"Please Enter the Litter Size:",
                                  render_kw={"id": "litter_size"})
    weeks_nursing = SelectField(u"How Many Weeks Has Your Pet Been Nursing?:",
                                  choices=[("default", "Please make a selection"),
                                            ("0", "1"),
                                            ("1", "2"),
                                            ("2", "3"),
                                            ("3", "4"),
                                            ("4", "5"),
                                            ("5", "6")],
                                  render_kw={"default": {"disabled": ""},
                                             "id": "weeks_nursing"})

# Obtain login info
class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = StringField("Password:", validators=[DataRequired()])
    submit = SubmitField("Log in")

# Obtain registration info
class RegisterForm(FlaskForm):
    username = StringField("Please Choose a Username:", validators=[DataRequired()])
    password = StringField("Please Choose a Password:", validators=[DataRequired()])
    confirm_password = StringField("Please Confirm Your Password:", validators=[DataRequired()])
    submit = SubmitField("Sign Up")
    
# Obtain activity info
class WorkForm(FlaskForm):
    work_minutes = FloatField(
        "Approximately how many minutes of exercise does your pet get per day? Please enter 0 if none: ",
        validators=[DataRequired()])
    work_hours = FloatField(
        "Approximately how many hours of exercise does your pet get per day? Please enter 0 if none: ",
        validators=[DataRequired()])
    
