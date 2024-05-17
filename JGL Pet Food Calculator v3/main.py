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

        # Remember which user has logged in
        session["user_id"] = user_lookup[0]["id"]
        
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
            # If all checks pass, hash password
            hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            
            # Insert new info into database
            db.execute("INSERT INTO users (username, password) VALUES(?, ?)", request.form.get("username"), hashed_password)
                
            user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            
            # Remember which user has logged in
            session["user_id"] = user[0]["id"]
            
            logged_in = True
            
            # Redirect to home
            return render_template("index.html", logged_in=logged_in)
    
    return render_template("register.html", form=form)

@app.route("/logout")
def logout():
    """Logs user out"""
    
    # Clears the user_id
    session.clear()
    
    # Redirect to home
    return redirect("/")

@app.route("/get-signalment", methods=["GET", "POST"])
def pet_info():
    '''Gets the pet's signalment, i.e. name, age, sex/reproductive status, breed, species'''
    form = NewSignalment()
    
    if request.method == "POST":
        species = form.pet_species.data
        
        # Show an error message if the user doesn't choose a species
        if species == "default":
            flash("Please choose a species from the dropdown.")
            return render_template("get_signalment.html", form=form)

        # TODO: Add pet to the database if the user is logged in
        
            # else pass the data to the next function 
        return redirect(url_for('pet_info_continued', species=species))

    return render_template("get_signalment.html", form=form)

@app.route("/get-signalment-pt-2", methods=["GET", "POST"])
def pet_info_continued():
    '''Gets the pet's signalment, i.e. name, age, sex/reproductive status, breed, species'''
    form = NewSignalment()

    species = request.args.get("species")
    # AKC Breeds by Size csv courtesy of MeganSorenson of Github 
    # # # https://github.com/MeganSorenson/American-Kennel-Club-Breeds-by-Size-Dataset/blob/main/AmericanKennelClubBreedsBySize.xlsx
    
    # Access breed data via database
    pet_breed = []
    if species == "canine":
        pet_breed += db.execute(
            "SELECT Breed FROM dog_breeds"
        )
    elif species == "feline":
        pet_breed += db.execute(
            "SELECT Breed FROM cat_breeds"
        )
            
    #TODO: Add flash error if default is chosen

    if request.method == "POST":
        pet_sex = form.pet_sex.data
        pet_age_years = form.pet_age.data
        pet_age_months = form.pet_age_months.data     

        species = request.args.get("species")
        print(f"Pet sex: {pet_sex}")
        print(f"Pet age (years): {pet_age_years}")
        print(f"Pet age (months): {pet_age_months}")
        if pet_age_years >= 2 and pet_age_months >= 0:
            # If dog isn't pediatric/is sexually mature, find the best DER factor per lifestage

            if pet_sex == "female":
                # If the pet is an intact female, redirect to pregnancy questions
                    
                return redirect(url_for('repro_status', species=species))
            else:
                return redirect(url_for('pet_condition', species=species))

        # TODO: Add pet to the database if the user is logged in
            # else pass the data to the next function 

    return render_template("get_signalment_part_2.html", form=form, pet_breed=pet_breed, species=species)

@app.route("/pregnancy_status", methods=["GET", "POST"])
def repro_status():
    '''Gets information about the pet's pregnancy status'''
    repro = ReproStatus()
    
    if request.method == "POST":
        pregnancy_status = repro.pregnancy_status.data
        
        # Retrieves species session variable 
        # TODO: replace this with database query if the user is logged in
        species = request.args.get('species')

        
        if pregnancy_status == "y":
            if species == "canine":
                # If pet is pregnant and canine, ask how many weeks along she is
                return redirect(url_for('gestation_duration'))
            
            # If pet is pregnant and feline, DER factor is * 1.6-2.0
            return redirect(url_for('pet_condition', species=species))
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
        
        species = request.args.get('species')
        
        if number_weeks_pregnant <= "6":
            # If pet is pregnant, canine, and within the first 42 days of pregnancy, DER modifier is *~1.8
            # TODO: Add this information to pet's table in the database
            pass
        else:
            # If pet is pregnant, canine, and within the last 21 days of pregnancy, DER modifier is *3
            # TODO: Add this information to pet's table in the database
            pass
        
        return redirect(url_for('pet_condition', species=species))
    
    return render_template("gestation_duration.html", repro=repro)


@app.route("/litter_size", methods=["GET", "POST"])
def litter_size():
    '''Asks for the litter size of pets that have one, then assigns DER modifier'''
    
    repro = ReproStatus()
    
    # Retrieves species session variable 
    # TODO: replace this with database query if the user is logged in
    species = session.get('species')
    
    if request.method == "POST":
        litter_size = repro.litter_size.data
        
        # Stores litter size data in the session
        # TODO: replace this with database query if the user is logged in
        session['litter_size'] = litter_size
        
        if species == "feline":
            # If the pet is a nursing feline, ask for weeks of lactation
            return redirect(url_for('lactation_duration'))
            
        else:
            # If pet is a nursing canine, DER modifier is as follows:
                # 1 puppy: * 3.0
                # 2 puppies: 3.5
                # 3-4 puppies: 4.0
                # 5-6 puppies: 5.0
                # 7-8 puppies: 5.5
                # 9 puppies >= 6.0
                
            # TODO: Add modifier to pet's table in the database
            pass
        return redirect(url_for('pet_condition'))
    
    return render_template("get_litter_size.html", repro=repro, species=species)


@app.route("/lactation_status", methods=["GET", "POST"])
def lactation_status():
    '''Asks if the pet is currently nursing'''
    
    repro = ReproStatus()
    
    if request.method == "POST":
        lactation_status = repro.nursing_status.data

        if lactation_status == "y":
            # If pet is lactating, ask for litter size
            return redirect(url_for('litter_size'))
            
        else:
            # If pet is not lactating, next page is get_weight
            return redirect(url_for('pet_condition'))
    
    return render_template("get_lactation_status.html", repro=repro)
    


@app.route("/lactation_duration", methods=["GET", "POST"])
def lactation_duration():
    '''Asks how many weeks a pregnant queen has been nursing and adds DER modifier'''
    
    repro = ReproStatus()
    
    if request.method == "POST":
        duration_of_nursing = int(repro.weeks_nursing.data)
        
        if duration_of_nursing <= 2:
            # If the queen has been nursing for 2 weeks or less, DER modifier is RER + 30% per kitten
            pass
        
        elif duration_of_nursing == 3:
            # If the queen has been nursing for 3 weeks, DER modifier is RER + 45% per kitten
            pass 
        
        elif duration_of_nursing == 4:
            # If the queen has been nursing for 4 weeks, DER modifier is RER + 55% per kitten
            pass 
        
        elif duration_of_nursing == 5:
            # If the queen has been nursing for 5 weeks, DER modifier is RER + 65% per kitten
            pass 
        
        elif duration_of_nursing == 6:
            # If the queen has been nursing for 6 weeks, DER modifier is RER + 90% per kitten
            pass 

        return redirect(url_for('pet_condition'))
    
    return render_template("lactation_duration.html", repro=repro)


@app.route("/get-weight", methods=["GET", "POST"])
def pet_condition():
    '''Gets the pet's weight and body condition score'''
    
    form = GetWeight() 
    
    # Retrieves species session variable 
    # TODO: replace this with database query if the user is logged in
    species = session.get('species')
    
    # TODO: Add weight and BCS to the database if the user is logged in
            # else pass this data to the next function 
            
    # TODO: Redirect to the next page if info is input successfully
    if request.method == "POST":
        return redirect(url_for('activity'))
    
    return render_template("get_weight_and_bcs.html", form=form, species=species)

@app.route("/activity", methods=["GET", "POST"])
def activity():
    '''Gets a pet's activity status/amount'''
    
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

            
            # # Determine if dog is pediatric
            # if pet_age_years == 0 and pet_age_months < 4:
            #     # Puppies under 4 months old have a DER modifier of * 3.0
            #     print("DER Modifier * 3.0")
                
            # elif pet_age_years < 1 and pet_age_months > 4 :
            #     # Puppies over 4 months old and under have a DER modifier of * 2.0
            #     print("DER Modifier * 2.0")
            # DER factors suggested by https://todaysveterinarynurse.com/wp-content/uploads/sites/3/2018/07/TVN-2018-03_Puppy_Kitten_Nutrition.pdf
            # if pet_age_years == 0:
            #     if pet_age_months < 4:
            #         # Kittens under 4 months old have a DER modifier of * 3.0
            #         print("DER Modifier * 3.0")
            #     elif pet_age_months >= 4 and pet_age_months <= 6:
            #         # Kittens between 4 and 6 months old have a DER modifier of * 2.5
            #         print("DER Modifier * 2.5")
            #     elif pet_age_months >= 9 and pet_age_months <= 12:
            #         # Kittens between 9 and 12 months old have a DER modifier of * 1.8-2.0
            #         print("DER Modifier * 1.8-2.0")
                    
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

