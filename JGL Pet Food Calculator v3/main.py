"""Welcome to the Pet Food Calculator!"""

from cs50 import SQL
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap5
from forms import NewSignalment, GetWeight, ReproStatus, LoginForm, RegisterForm, WorkForm
import os
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
        
        # Stores species data in the session, suggested by CoPilot
        session['species'] = species
        
        if patient_sex == "female":
            return redirect(url_for('repro_status', species=species))
        
        # TODO: Add pet to the database if the user is logged in
            # else pass the data to the next function 
        return redirect(url_for('patient_condition', species=species))

    return render_template("get_signalment.html", form=form)


@app.route("/pregnancy_status", methods=["GET", "POST"])
def repro_status():
    '''Gets information about the pet's pregnancy status'''
    repro = ReproStatus()
    form = NewSignalment()
    
    if request.method == "POST":
        pregnancy_status = repro.pregnancy_status.data
        
        # Retrieves species session variable 
        # TODO: replace this with database query if the user is logged in
        species = session.get('species')

        
        if pregnancy_status == "y" and species == "canine":
            # If pet is pregnant and canine, ask how many weeks along she is
            return redirect(url_for('gestation_duration'))
            
        else:
            # If pet is not pregnant, ask if she is currently nursing a litter
            return redirect(url_for('lactation_status'))
    
    return render_template("get_reproductive_status.html", repro=repro)


@app.route("/gestation_duration", methods=["GET", "POST"])
def gestation_duration():
    '''Asks for how long the pet has been pregnant for if they are canine 
    and assigns DER factor'''
    
    repro = ReproStatus()
    
    if request.method == "POST":
        number_weeks_pregnant = repro.weeks_gestation.data
        
        if number_weeks_pregnant <= "6":
            # If pet is pregnant, canine, and within the first 42 days of pregnancy, DER modifier is *~1.8
            # TODO: Add this information to pet's table in the database
            pass
        else:
            # If pet is pregnant, canine, and within the last 21 days of pregnancy, DER modifier is *3
            # TODO: Add this information to pet's table in the database
            pass
    
    return render_template("gestation_duration.html", repro=repro)


@app.route("/litter_size", methods=["GET", "POST"])
def litter_size():
    '''Asks for the litter size of pets that have one, then assigns DER modifier'''
    
    repro = ReproStatus()
    
    if request.method == "POST":
        litter_size = repro.litter_size.data
        
        # Retrieves species session variable 
        # TODO: replace this with database query if the user is logged in
        species = session.get('species')
        
        # Stores litter size data in the session
        # TODO: replace this with database query if the user is logged in
        session['litter_size'] = litter_size
        
        if species == "feline":
            # If the pet is a cat, ask for weeks of lactation
            return redirect(url_for('gestation_duration'))
            
        else:
            # If pet is not pregnant, ask if she is currently nursing a litter
            pass
    
    return render_template("get_litter_size.html", repro=repro)


@app.route("/lactation_status", methods=["GET", "POST"])
def lactation_status():
    '''Asks if the pet is currently nursing'''
    
    repro = ReproStatus()
    
    if request.method == "POST":
        lactation_status = repro.nursing_status.data
        
        # Retrieves species session variable 
        # TODO: replace this with database query if the user is logged in
        species = session.get('species')

        
        if lactation_status == "y" and species == "feline":
            # If nursing and feline, ask how many weeks she has been lactating
            return redirect(url_for('gestation_duration'))
            
        else:
            # If pet is not pregnant, ask if she is currently nursing a litter
            return redirect(url_for('lactation_status'))
    
    return render_template("get_lactation_status.html", repro=repro)
    

@app.route("/get-weight", methods=["GET", "POST"])
def patient_condition():
    '''Gets the pet's weight and body condition score'''
    
    species = request.args.get('species')
    form = GetWeight() 
    
    # TODO: Add weight and BCS to the database if the user is logged in
            # else pass this data to the next function 
            
    # TODO: Redirect to the next page if info is input successfully
    if request.method == "POST":
        return redirect(url_for('activity'))
    
    return render_template("get_weight_and_bcs.html", form=form, species=species)

@app.route("/activity", methods=["GET", "POST"])
def activity():
    '''Gets a patient's activity status/amount'''
    
    # TODO: Add activity intensity table to database
    # sources: https://wellbeloved.com/pages/cat-dog-activity-levels
    # https://perfectlyrawsome.com/raw-feeding-knowledgebase/activity-level-canine-calorie-calculations/
        # Sedentary: 0-30 minutes of light activity daily
        # Low activity: 30 minutes to 1 hour (i.e. walking on lead)
        # Moderate activity: 1-2 hours of low impact activity 
            # Or 1-3 hours of high impact activity (i.e. running off-lead, playing ball, playing off-lead with other dogs)
        # High activity: 2-3 hours of daily activity (i.e. working dog)
        # Working and performance: 3+ hours (i.e. working dog)
            # Or high impact activity under extreme conditions (i.e. racing sled dog)
    
    work = WorkForm()
    
    return render_template("get_work_level.html", work=work)
    

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
# 	weight FLOAT NOT NULL,
# 	units VARCHAR(5) NOT NULL,
# 	pregnant VARCHAR(1),
# 	weeks_gestating INT,
# 	nursing VARCHAR(1),
# 	litter_size INT,
# 	weeks_nursing INT,
#   activity_level VARCHAR(25),
# 	rer FLOAT,
# 	rer_factor FLOAT,
# 	der FLOAT,
#   current_food_kcal FLOAT,
#   current_food_amt_rec VARCHAR(15),
#   date_of_first_report DATETIME,
#   most_recent_report_date DATETIME,
# )

# TODO: Add: exercise status, current food kcal/cup, amount amount of food recommended, date recommended?