"""Welcome to the Pet Food Calculator!"""

from cs50 import SQL
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from forms import NewSignalment, GetWeight, ReproStatus, LoginForm, RegisterForm, WorkForm
import os, requests
import pandas as pd 
from werkzeug.security import check_password_hash, generate_password_hash


# Stick to 2 font types max, go for similar moods and time eras
# # contrast the serif-ness and weights
# Avoid Kristen, Comic Sans, Curlz, Viner, Papyrus
# Reduce the number of font alignment points

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap5(app)

# Load environmental variables

app.config['SECRET_KEY'] = os.environ.get('KEY')

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///pet_food_calculator.db")

# Image credit to Laurie O'Keefe in partner with PetMD, consulting veterinarian Jennifer Coates, DVM

# TODO: Add login required to applicable routes
@app.route("/")
def home():
    '''Includes welcome and disclaimers along with login/register buttons'''
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    '''Logs an existing user in'''
    form = LoginForm()
    
    # Checks if the user's data is validated 
    if form.validate_on_submit():

        # Check username and hashed password against the database
        user_lookup = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        
        if user_lookup == None:
            flash("Username not found.")
            
        # Ensure username exists and password is correct
        if not check_password_hash(user_lookup[0]["password"], 
                                   request.form.get("password")):
            flash("Invalid password.")

        logged_in = True

        return render_template("index.html", logged_in=logged_in)
        
    
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    '''Registers a new user'''

    form = RegisterForm()
    
    if form.validate_on_submit():
        # Check user against info in the database
        find_user = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        
        # Check if username exists already in the database
        if len(find_user) != 0:
            flash("That username already taken.")
        # Check if the user's password matches the password verification
        elif request.form.get("password") != request.form.get("confirm_password"):
            flash("Passwords must match.")
        else:
            # If all checks pass, hash password and insert info into database
            hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            
            db.execute("INSERT INTO users (username, password) VALUES(?, ?)", request.form.get("username"), hashed_password)
                
            # TODO: Add sessions?
            return redirect(url_for('home'))
    
    return render_template("register.html", form=form)

@app.route("/get-signalment", methods=["GET", "POST"])
def pet_info():
    '''Gets the pet's signalment, i.e. name, age, sex/reproductive status, breed, species'''
    form = NewSignalment()
    repro = ReproStatus()
    
    # AKC Breeds by Size csv courtesy of MeganSorenson of Github 
    # # # https://github.com/MeganSorenson/American-Kennel-Club-Breeds-by-Size-Dataset/blob/main/AmericanKennelClubBreedsBySize.xlsx
    
    # TODO: Access breed data via database
    # breed_data = pd.read_csv('AmericanKennelClubBreedsBySize.csv')['Breed']
    # sorted_breed_data = breed_data.sort_values(ascending=True)
    
    # Breed tuple method suggested by Copilot
    # breed_data_tuples = list(zip(sorted_breed_data, sorted_breed_data))
    
    # This line adapted from Andrew Clark's suggestion on StackOverflow
    # https://stackoverflow.com/questions/67097559/dynamically-populate-the-flask-wtforms-select-field-from-a-csv-file
    # form.patient_breed.choices += breed_data_tuples
    
    # TODO: Get breed data csv for our feline friends!
    ## TODO: add another dynamic WTFForm for cats
    ### TODO: Show only canine or only feline breeds based off of what the user chose as the species
    
    if request.method == "POST":
        species = form.patient_species.data
        patient_sex = form.patient_sex.data
        
        # TODO: Either adapt form dynamically to show repro questions based on WTFForm selection
        ## Or convert this particular form to html-based? (Preference for WTF)
        if patient_sex == "female":
            return redirect(url_for('repro_status', species=species))
        
        # TODO: Add pet to the database if the user is logged in
            # else pass the data to the next function 
        return redirect(url_for('patient_condition', species=species))

    return render_template("get_signalment.html", form=form, repro=repro)

@app.route("/get-weight", methods=["GET", "POST"])
def patient_condition():
    '''Gets the pet's weight and body condition score'''
    
    species = request.args.get('species')
    form = GetWeight() 
    
    # TODO: Add weight and BCS to the database if the user is logged in
            # else pass this data to the next function 
            
    # TODO: Redirect to the next page if info is input successfully
    return render_template("get_weight_and_bcs.html", form=form, species=species)

@app.route("/activity", methods=["GET", "POST"])
def activity():
    '''Gets a patient's activity status/amount'''
    
    work = WorkForm()
    
    return render_template("get_work_level.html", form=work)
    

    # TODO:  If pet is pregnant and canine, ask how many weeks along she is
    
    # TODO: If pet is not pregnant, ask if she is currently nursing a litter
        # TODO: if yes, ask the litter size 
            # TODO: if feline and nursing, ask how many weeks she has been doing so
        # TODO: if no, go to the next step in the questionnaire 
# New pet



# TODO: Calculate RER function
    # TODO: Render page with the pet's info and RER, 

# TODO: Calculate MER function
    # TODO: Render a page with the pet's info, RER, MER factors, and MER range.
    # TODO: Explain the formula and give disclaimers
    # TODO: Give the option to stop here
        # TODO: Render a button to lead to the actual food calculator

# TODO: Calculate food function
    # TODO: Ask the user how many calories per cup their current food is
        # TODO: Allow up to 2 choices.
        # TODO: Include instructions on how to find this information
        # TODO: Ask how many meals/day or include a per-day option
         
    # TODO: Import pet data
        # TODO: use RER and MER  to calculate total daily calories needed
        # # Start in the middle of the range
            # TODO: Use this number to calculate total number of cups per day
            
        # TODO: Return all this info to the user 

# TODO: Create pet database
# possible .schema?
# CREATE TABLE pet(
#   pet_id INT NOT NULL PRIMARY KEY,
#   name VARCHAR(25) NOT NULL,
#   age VARCHAR(25) NOT NULL,
#   species VARCHAR(10) NOT NULL,
# 	breed VARCHAR(25) NOT NULL,
# 	sex VARCHAR(15) NOT NULL,
# 	weight NUMERIC NOT NULL,
# 	units VARCHAR(5) NOT NULL,
# 	pregnant VARCHAR(1),
# 	weeks_gestating INT,
# 	nursing VARCHAR(1),
# 	litter_size INT,
# 	weeks_nursing INT,
# 	rer NUMERIC NOT NULL,
# 	rer_factor NUMERIC NOT NULL,
# 	der NUMERIC NOT NULL
# )

# TODO: Add: exercise status, current food kcal/cup, amount amount of food recommended, date recommended?