"""Welcome to the Pet Food Calculator!"""

from cs50 import SQL
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap5
from forms import NewSignalment, GetWeight, ReproStatus, LoginForm, RegisterForm, WorkForm, FoodForm
from helpers import login_check_for_species
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
    """Includes welcome and disclaimers along with login/register buttons"""
    
    user_id = session.get("user_id")
    if user_id:
        user = db.execute(
            "SELECT username FROM users WHERE id = :user_id",
            user_id=session["user_id"]
        )
        
        username = user[0]["username"]
        
        return render_template("index.html", user=username)
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs an existing user in"""
    form = LoginForm()
    
    # Checks if the user's data is validated 
    if form.validate_on_submit():

        # Check username and hashed password against the database
        user_lookup = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        
        if user_lookup == None:
            flash("Username not found.")
            return redirect(url_for('login'))
        
        # Ensure username exists and password is correct
        elif not check_password_hash(user_lookup[0]["password"], 
                                   request.form.get("password")):
            flash("Invalid password.")
            return redirect(url_for('login'))
        
        else:
            flash(f"Logged in as {request.form.get("username")}!")
            
            # Remember which user has logged in
            session["user_id"] = user_lookup[0]["id"]
    
        return render_template("index.html")
        
    
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user"""

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
    """Gets the pet's signalment, i.e. name, age, sex/reproductive status, breed, species"""
    
    form = NewSignalment()
    
    if request.method == "POST":
        species = form.pet_species.data
        pet_name = form.pet_name.data.title()
        
        print(type(species))
        print(type(pet_name))
        
        # Store session variables
        session["species"] = species
        session["pet_name"] = pet_name
        
        # Show an error message if the user doesn't choose a species
        if species == "default":
            flash("Please choose a species from the dropdown.")
            return render_template("get_signalment.html", form=form)

        # Add pet to the database if the user is logged in
        if session["user_id"] != None:
            
            # See if the pet is already added 
            find_existing_pet = db.execute(
                "SELECT name FROM pets WHERE owner_id = :user_id AND name = :name",
                user_id=session["user_id"], name=pet_name
            )
            
            existing_pet = None
            for input_pet in find_existing_pet:
                # Condition suggested by CoPilot
                if pet_name in input_pet.values():
                    # If the pet was found, update the information instead of adding a duplicate pet
                    existing_pet = input_pet
                    break
                
            if existing_pet:
                try:
                    db.execute(
                        "UPDATE pets SET name = :updated_name, species = :updated_species WHERE name = :pet_name AND owner_id = :user_id",
                        updated_name=pet_name, updated_species=species, user_id=session["user_id"]
                    )
                except Exception as e:
                    flash(f"Unable to update data, Exception: {e}")
            else:
                # If no pet is found (i.e. new pet in the database), insert pet
                    
                try:
                    db.execute(
                        "INSERT INTO pets (owner_id, name, species) VALUES (?, ?, ?)",
                        session["user_id"], form.pet_name.data, species
                    )
                except Exception as e:
                    flash(f"Unable to insert new data, Exception: {e}")
                
        # else pass the data to the next function via session variables
        return redirect(url_for('pet_info_continued', species=species, pet_name=pet_name))

    return render_template("get_signalment.html", form=form)


@app.route("/get-signalment-pt-2", methods=["GET", "POST"])
def pet_info_continued():
    """Gets the rest of pet's signalment, 
    i.e. name, age, sex/reproductive status, breed, species"""
    
    form = NewSignalment()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()

        
    # AKC Breeds by Size csv courtesy of MeganSorenson of Github 
    # # # https://github.com/MeganSorenson/American-Kennel-Club-Breeds-by-Size-Dataset/blob/main/AmericanKennelClubBreedsBySize.xlsx
    
    # Access breed data via database
    pet_breed = []
    if species == "Canine":
        pet_breed += db.execute(
            "SELECT Breed FROM dog_breeds"
        )
    if species == "Feline":
        pet_breed += db.execute(
            "SELECT Breed FROM cat_breeds"
        )
        
    
    if request.method == "POST":
        
        pet_sex = form.pet_sex.data
        pet_age_years = form.pet_age.data
        pet_age_months = form.pet_age_months.data     

        pet_breed = request.form.get("pet_breed")
        
        # print(pet_breed)

        # Show an error message if the user doesn't choose a breed
        if pet_breed == None:
            flash("Please choose a breed from the dropdown.")
        else:
            # Store new info as session variables
            session["pet_sex"] = pet_sex
            session["pet_age_years"] = pet_age_years
            session["pet_age_months"] = pet_age_months
            session["pet_breed"] = pet_breed
            
            # print(pet_age_years)
            # print(pet_age_months)
            # print(pet_breed)
            # print(pet_sex)
            # print(session["pet_name"])
            # print(session["user_id"])
            
            # Add pet to the database if the user is logged in
            if session["user_id"] != None:
                try:
                    db.execute(
                        "UPDATE pets SET age_in_years = :y, age_in_months = :m, breed = :breed, sex = :sex WHERE name = :pet_name AND owner_id = :user_id",
                            y=pet_age_years, m=pet_age_months, breed=pet_breed, sex=pet_sex, pet_name=session["pet_name"], user_id=session["user_id"]
                        )
                except Exception as e:
                    flash(f"Unable to insert data, Exception: {e}")
            
            if pet_age_years >= 2 and pet_age_months >= 0:

                if pet_sex == "female":
                    # If the pet is an intact female redirect to pregnancy questions
                    
                    return redirect(url_for('repro_status', species=species))
                else:
                    # Else redirect to pet body condition score questions
                    return redirect(url_for('pet_condition', species=species))



    return render_template("get_signalment_part_2.html", form=form, pet_breed=pet_breed, species=species)


@app.route("/pregnancy_status", methods=["GET", "POST"])
def repro_status():
    """Gets information about the pet's pregnancy status"""
    repro = ReproStatus()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()   
     
    if request.method == "POST":
        pregnancy_status = repro.pregnancy_status.data
        
        # Store new info as session variables
        session["pregnancy_status"] = pregnancy_status
        
        print(pregnancy_status)
        
        # Add pet to the database if the user is logged in
        if session["user_id"] != None:
            try:
                db.execute(
                    "UPDATE pets SET is_pregnant = :is_pregnant WHERE name = :pet_name AND owner_id = :user_id",
                    is_pregnant=pregnancy_status, pet_name=session["pet_name"], user_id=session["user_id"]
                )
            except Exception as e:
                flash(f"Unable to insert data, Exception: {e}")
            
            
        if pregnancy_status == "y":
            
            if species == "Canine":

                # If pet is pregnant and canine, ask how many weeks along she is
                return redirect(url_for('gestation_duration', species=species))
            
            # If pet is pregnant and feline, DER factor is * 1.6-2.0
            return redirect(url_for('pet_condition', species=species))
        else:
            # If pet is not pregnant, ask if she is currently nursing a litter
            return redirect(url_for('lactation_status'))
    
    return render_template("get_reproductive_status.html", repro=repro)


@app.route("/gestation_duration", methods=["GET", "POST"])
def gestation_duration():
    """Asks for how long the pet has been pregnant for if they are canine 
    and assigns DER factor"""
    
    repro = ReproStatus()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    if request.method == "POST":
        number_weeks_pregnant = repro.weeks_gestation.data
        
        # Store new info as session variables
        session["number_weeks_pregnant"] = number_weeks_pregnant
        
        if session["user_id"] != None:
            try:
                db.execute(
                    "UPDATE pets SET weeks_gestating = :weeks_gestating WHERE name = :pet_name AND owner_id = :user_id",
                    weeks_gestating=number_weeks_pregnant, pet_name=session["pet_name"], user_id=session["user_id"]
                )
            except Exception as e:
                flash(f"Unable to insert data, Exception: {e}")
            
        
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
    """Asks for the litter size of pets that have one, then assigns DER modifier"""
    
    repro = ReproStatus()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    if request.method == "POST":
        litter_size = repro.litter_size.data
        
        # Stores litter size data in the session
        session["litter_size"] = litter_size
        
        # Add pet to the database if the user is logged in
        if session["user_id"] != None:
            try:
                db.execute(
                    "UPDATE pets SET litter_size = :size WHERE name = :pet_name AND owner_id = :user_id",
                    size=litter_size, pet_name=session["pet_name"], user_id=session["user_id"]
                )
            except Exception as e:
                flash(f"Unable to insert data, Exception: {e}")
          
        if species == "Feline":
            # If the pet is a nursing feline, ask for weeks of lactation
            return redirect(url_for('lactation_duration'))
            

        # If pet is a nursing canine, DER modifier is as follows:
                # 1 puppy: * 3.0
                # 2 puppies: 3.5
                # 3-4 puppies: 4.0
                # 5-6 puppies: 5.0
                # 7-8 puppies: 5.5
                # 9 puppies >= 6.0
                
        # TODO: Add modifier to pet's table in the database
        return redirect(url_for('pet_condition', species=species))
    
    return render_template("get_litter_size.html", repro=repro, species=species)


@app.route("/lactation_status", methods=["GET", "POST"])
def lactation_status():
    """Asks if the pet is currently nursing"""
    
    repro = ReproStatus()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    if request.method == "POST":
        lactation_status = repro.nursing_status.data
        
        # Stores lactation status variable in session
        session["lactation_status"] = lactation_status
        
        print(lactation_status)
        
        # Add pet to the database if the user is logged in
        if session["user_id"] != None:
            try:
                db.execute(
                    "UPDATE pets SET is_nursing = :lactation_status WHERE name = :pet_name AND owner_id = :user_id",
                    lactation_status=lactation_status, pet_name=session["pet_name"], user_id=session["user_id"]
                )
            except Exception as e:
                flash(f"Unable to insert data, Exception: {e}")
          

        if lactation_status == "y":
            # If pet is lactating, ask for litter size
            return redirect(url_for('litter_size'))
            
        else:
            # If pet is not lactating, next page is get_weight
            return redirect(url_for('pet_condition', species=species))
    
    return render_template("get_lactation_status.html", repro=repro)
    

@app.route("/lactation_duration", methods=["GET", "POST"])
def lactation_duration():
    """Asks how many weeks a pregnant queen has been nursing and adds DER modifier"""
    
    repro = ReproStatus()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    if request.method == "POST":
        duration_of_nursing = int(repro.weeks_nursing.data)
        
        # Stores nursing duration variable in session
        session["duration_of_nursing"] = duration_of_nursing
        
        # Add pet to the database if the user is logged in
        if session["user_id"] != None:
            try:
                db.execute(
                    "UPDATE pets SET weeks_nursing = :duration_of_nursing WHERE name = :pet_name AND owner_id = :user_id",
                        duration_of_nursing=duration_of_nursing, pet_name=session["pet_name"], user_id=session["user_id"]
                    )
            except Exception as e:
                flash(f"Unable to insert data, Exception: {e}")
                    
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

        return redirect(url_for('pet_condition', species=species))
    
    return render_template("lactation_duration.html", repro=repro)


@app.route("/get-weight", methods=["GET", "POST"])
def pet_condition():
    """Gets the pet's weight and body condition score"""
    
    form = GetWeight() 
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    if request.method == "POST":
        bcs = int(form.pet_bcs.data)
        weight = float(form.pet_weight.data)
        units = form.pet_units.data
        
        # Store new info as session variables
        session["bcs"] = bcs
        session["weight"] = weight
        session["units"] = units
        
        # print(bcs)
        # print(type(bcs))
        # print(weight)
        # print(type(weight))
        # print(units)
        # print(type(units))
        
        # Use login check from helpers.py to verify species
        species = login_check_for_species()
    
        # Add weight and BCS to the database if the user is logged in
        if session["user_id"] != None:
            try:
                print(session["pet_name"])
                print(session["user_id"])

                db.execute(
                    "UPDATE pets SET bcs = :body_condition_score, weight = :weight, units = :units WHERE name = :pet_name AND owner_id = :user_id",
                    body_condition_score=bcs, weight=weight, units=units, pet_name=session["pet_name"], user_id=session["user_id"]
                )
                    
            except Exception as e:
                    flash(f"Unable to insert data, Exception: {e}")
            
        # Redirect to the next page if info is input successfully
        if species == "Canine":
            # Gets a dog's activity level if applicable 
            return redirect(url_for('activity'))
        
        if species == "Feline":
            # Take cat owners to the pre-confirmation page
            return redirect(url_for('confirm_data', species=species))
    
    return render_template("get_weight_and_bcs.html", form=form, species=species)


@app.route("/activity", methods=["GET", "POST"])
def activity():
    """Gets a pet's activity status/amount"""
    
    work = WorkForm()
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    if request.method == "POST":
        light_work_minutes = work.light_work_minutes.data
        light_work_hours = work.light_work_hours.data
        heavy_work_minutes = work.heavy_work_minutes.data
        heavy_work_hours = work.heavy_work_hours.data
        
        
        # Convert time for easier logic tracking
        light_work_hours += (light_work_minutes / 60)
        heavy_work_hours += (heavy_work_minutes / 60)
        

        # sources: https://wellbeloved.com/pages/cat-dog-activity-levels
        # https://perfectlyrawsome.com/raw-feeding-knowledgebase/activity-level-canine-calorie-calculations/
        if light_work_hours < 0.5 and heavy_work_hours == 0:
            # Sedentary: 0-30 minutes of light activity daily
            activity_level = "Sedentary"
        elif light_work_hours >= 0.5 and light_work_hours <= 1 and heavy_work_hours == 0:
            # Low activity: 30 minutes to 1 hour (i.e. walking on lead)
            activity_level = "Low"
        elif light_work_hours >= 1 and light_work_hours <= 2 and heavy_work_hours == 0:
            # Moderate activity: 1-2 hours of low impact activity
            activity_level = "Moderate"
        elif heavy_work_hours >= 1 and heavy_work_hours <= 3 and light_work_hours == 0:
            # Moderate activity: 1-3 hours of high impact activity (i.e. running off-lead, playing ball, playing off-lead with other dogs)
            activity_level = "Moderate"
        elif heavy_work_hours > 3 and light_work_hours == 0:
            # Working and performance: 3+ hours (i.e. working dog)
            activity_level = "Heavy"
                    
        
        print(activity_level)
        # If user is logged in, add activity level to database
        if session["user_id"] != None:
            try:
                print(session["pet_name"])
                print(session["user_id"])
                
                db.execute(
                    "UPDATE pets SET activity_level = :activity WHERE name = :pet_name AND owner_id = :user_id",
                    activity=activity_level, pet_name=session["pet_name"], user_id=session["user_id"]
                )
                
            except Exception as e:
                    flash(f"Unable to insert data, Exception: {e}")
        
        else:    
            # Otherwise, create new session variables
            session["activity_level"] = activity_level
        
        return redirect(url_for('confirm_data', species=species))
    
    return render_template("get_work_level.html", work=work)


@app.route("/confirm_data", methods=["GET", "POST"])
def confirm_data():
    """Confirms pet's info before taking users to the food calculator"""
    
    # Use login check from helpers.py to verify species
    species = login_check_for_species()
    
    # If user is logged in, use SQL query
    if session["user_id"] != None:
        try:
            print(session["pet_name"])
            print(session["user_id"])
                
            pet_data = db.execute(
                "SELECT name, age_in_years, age_in_months, species, breed, sex, bcs, weight, units, activity_level, is_pregnant, weeks_gestating, is_nursing, litter_size, weeks_nursing FROM pets WHERE owner_id = :user_id AND name = :pet_name",
                user_id=session["user_id"], pet_name=session["pet_name"]
            )       
            
            print(pet_data)
        except Exception as e:
            flash(f"Unable to insert data, Exception: {e}")
        else:
            return render_template("confirm_pet_info.html", pet_data=pet_data, user_id=session["user_id"])
        
    # Otherwise, pass session variables
    else:
        pet_data = [{'name': session["pet_name"],
                     'age_in_years': session["pet_age_years"],
                     'age_in_months': session["age_in_months"],
                     'species': session["species"],
                     'breed': session["breed"],
                     'sex': session["pet_sex"],
                     'bcs': session["bcs"],
                     'weight': session["weight"],
                     'units': session["units"],
                     'activity_level': session["activity_level"],
                     'is_pregnant': None,
                     'weeks_gestating': None,
                     'is_nursing': None,
                     'litter_size': None,
                     'weeks_nursing': None}]
        
        if session["pregnancy_status"] != None:
            pet_data[0]['is_pregnant'] = session["pregnancy_status"]
        elif session["number_weeks_pregnant"] != None:
            pet_data[0]["weeks_gestating"] = session["number_weeks_pregnant"]
        elif session["lactation_status"] != None:
            pet_data[0]['is_nursing'] = session["lactation_status"]
        elif session['litter_size'] != None:
            pet_data[0]['litter_size'] = session['litter_size']
        elif session["duration_of_nursing"] != None:
            pet_data[0]['weeks_nursing'] = session["duration_of_nursing"]
        
        return render_template("confirm_pet_info.html", species=species)
    
    
@app.route("/current_food", methods=["GET", "POST"])
def current_food():
    """Asks the user for information on their current food"""
    
    current_food = FoodForm()
    
    if request.method == "POST":
        current_food_kcal = current_food.current_food_kcal.data
        meals_per_day = current_food.meals_per_day.data
        wants_transition = current_food.food_transition.data
        
        print(current_food_kcal)
        print(meals_per_day)
        print(wants_transition)
        
        # If user is logged in, add current food information to the database
        if session["user_id"] != None:
            try:
                print(session["pet_name"])
                print(session["user_id"])
                
                db.execute(
                    "UPDATE pets SET meals_per_day = :meals, current_food_kcal = :current_kcal WHERE name = :pet_name AND owner_id = :user_id",
                    meals=meals_per_day, current_kcal=current_food_kcal, pet_name=session["pet_name"], user_id=session["user_id"]
                )
                
            except Exception as e:
                    flash(f"Unable to insert data, Exception: {e}")
        
        else:    
            # Otherwise, create new session variables
            session["meals_per_day"] = meals_per_day
            session["current_food_kcal"] = current_food_kcal
            
        if wants_transition == "y":
            # If the user wants to transition their pet to a new food, redirect them
                # to the next form
            return redirect(url_for('new_food'))
        
        # If user doesn't want a transition, calculate RER
        return redirect(url_for('rer'))
        
    return render_template("current_food.html", current_food=current_food)
    
    
@app.route("/new_food", methods=["GET", "POST"])
def new_food():
    """Asks the user for calorie information on up to 2 new foods"""
    
    new_foods = FoodForm()
    
    if request.method == "POST":
        first_food_kcal = new_foods.new_food_one_kcal.data
        second_food_kcal = new_foods.new_food_two_kcal.data
        
        # If user is logged in, add current food information to the database
        if session["user_id"] != None:
            try:
                print(session["pet_name"])
                print(session["user_id"])
                    
                db.execute(
                    "UPDATE pets SET transitioning_food_one_kcal = :kcal_one, transitioning_food_two_kcal = :kcal_two WHERE name = :pet_name AND owner_id = :user_id",
                    kcal_one=first_food_kcal, kcal_two=second_food_kcal, pet_name=session["pet_name"], user_id=session["user_id"]
                )
                    
            except Exception as e:
                    flash(f"Unable to insert data, Exception: {e}")
            
        else:    
            # Otherwise, create new session variables
            session["first_food_kcal"] = first_food_kcal
            session["second_food_kcal"] = second_food_kcal 
           
        # If user doesn't want a transition, calculate RER
        return redirect(url_for('rer'))
           
    return render_template("new_food.html", new_foods=new_foods)

    # TODO:  If pet is pregnant and canine, ask how many weeks along she is
    
    # TODO: If pet is not pregnant, ask if she is currently nursing a litter
        # TODO: if yes, ask the litter size 
            # TODO: if feline and nursing, ask how many weeks she has been doing so
        # TODO: if no, go to the next step in the questionnaire 

@app.route("/rer", methods=["GET", "POST"])
def rer():
    """Calculates the minimum number of calories a pet needs at rest per day"""

    if session["user_id"] != None:
        # If the user is logged in, verify table variables 
        pet_info = db.execute(
            "SELECT name, age_in_years, age_in_months, species, sex, bcs, weight, units, \
                is_pregnant, weeks_gestating, is_nursing, litter_size, weeks_nursing, \
                    activity_level, meals_per_day, current_food_kcal, transitioning_food_one_kcal, \
                        transitioning_food_two_kcal FROM pets WHERE owner_id = ? AND name = ?", 
                    session["user_id"], session["pet_name"]
        )
        
        print(pet_info)
        
        name = pet_info[0]["name"]
        pet_age_years = pet_info[0]["age_in_years"]
        pet_age_months = pet_info[0]["age_in_months"]
        species = pet_info[0]["species"]
        sex = pet_info[0]["sex"]
        bcs = pet_info[0]["bcs"]
        weight = pet_info[0]["weight"]
        units = pet_info[0]["units"]
        is_pregnant = pet_info[0]["is_pregnant"]
        weeks_gestating = pet_info[0]["weeks_gestating"]
        litter_size = pet_info[0]["litter_size"]
        is_nursing = pet_info[0]["is_nursing"]
        weeks_nursing = pet_info[0]["weeks_nursing"]
        activity_level = pet_info[0]["activity_level"]
        first_new_food_kcal = pet_info[0]["transitioning_food_one_kcal"]
        second_new_food_kcal = pet_info[0]["transitioning_food_two_kcal"]
    else:
        # If a user isn't logged in, grab session variables
        name = session["pet_name"]
        pet_age_years = session["pet_age_years"]
        pet_age_months = session["pet_age_months"]
        species = session["species"]
        sex = session["pet_sex"]
        bcs = session["bcs"]
        weight = session["weight"]
        units = session["units"]
        is_pregnant = session["pregnancy_status"]
        weeks_gestating = session["number_weeks_pregnant"]
        litter_size = session["litter_size"]
        is_nursing = session["lactation_status"]
        weeks_nursing = session["duration_of_nursing"]
        activity_level = session["activity_level"]
        
        first_new_food_kcal = session["first_food_kcal"]
        second_new_food_kcal = session["second_food_kcal"]
    
    print(weight, units)
    
    # Convert lbs weighs to kgs
    if units == "lbs":
        weight = weight / 2.2
        units = "kgs"
    
    print(weight, units)
    
    # If pet weighs more than 2kg and less than 45kg, use 30 × (BW kg) + 70 = RER
    if weight >= 2 and weight <= 45:
        rer = round((30 * weight) + 70, 2)
    
    print(rer)
    
    # If pet weighs less than 2kg or more than 45kg, use 70 × (BW kg)^0.75 = RER
    if weight < 2 or weight > 45:
        rer = round(70 * weight**0.75, 2)
        
        # If user is logged in, add current food information to the database
    if session["user_id"] != None:
        try:
            print(session["pet_name"])
            print(session["user_id"])
                
            db.execute(
                "UPDATE pets SET rer = :rer WHERE name = :pet_name AND owner_id = :user_id",
                rer=rer, pet_name=session["pet_name"], user_id=session["user_id"]
            )
                    
        except Exception as e:
                flash(f"Unable to insert data, Exception: {e}")
            
    else:    
        # Otherwise, create new session variables
        session["rer"] = rer

    if request.method == "POST":
        return redirect()
    return render_template("rer.html", rer=rer, name=name)
    
@app.route("/der", methods=["GET", "POST"])
def der():
    """Calculates the daily energy rate and total food amount of the current diet to feed"""
    
    # If user is logged in, use SQL query
    if session["user_id"] != None:
        try:
            print(session["pet_name"])
            print(session["user_id"])
                
            pet_data = db.execute(
                "SELECT name, rer, meals_per_day, current_food_kcal, FROM pets WHERE owner_id = :user_id AND name = :pet_name",
                user_id=session["user_id"], pet_name=session["pet_name"]
            )       
            
            print(pet_data)
            
            name = pet_data[0]["name"]
            rer = pet_data[0]["rer"]
            meals_per_day = pet_data[0]["meals_per_day"]
            current_food_kcal = pet_data[0]["current_food_kcal"]
        except Exception as e:
            flash(f"Unable to insert data, Exception: {e}")    
    else:
        # If a user isn't logged in, grab session variables
        name = session["pet_name"]
        rer = session["rer"]
        meals_per_day = session["meals_per_day"]
        current_food_kcal = session["current_food_kcal"]
        
    food_amount_per_day = round(rer / current_food_kcal, 2)
    
    # Breaks the food amount in to whole and partial amounts to convert to volumetric easier
    whole_cans_or_cups, partial_amount = str(food_amount_per_day).split(".")[0], str(food_amount_per_day).split(".")[1]
    # print(food_amount_per_day)
    print(f"whole: {whole_cans_or_cups}, partial: {partial_amount}")
    
    # print(whole_cans_or_cups)
    # print(type(whole_cans_or_cups))
    
    # Convert partial volume amount from decimal to cups
    # Volume table source: https://amazingribs.com/more-technique-and-science/more-cooking-science/important-weights-measures-conversion-tables/
    partial_volumetric = ""
    if partial_amount > "0" and partial_amount <= "03":
        partial_volumetric = "1/2 tablespoon"
    elif partial_amount > "03" and partial_amount <= "06":
        partial_volumetric = "1/16 cup"
    elif partial_amount > "06" and partial_amount <= "13":
        partial_volumetric = "1/8 cup"
    elif partial_amount > "13" and partial_amount <= "25":
        partial_volumetric = "1/4 cup"
    elif partial_amount > "25" and partial_amount <= "40":
        partial_volumetric = "1/3 cup"
    elif partial_amount > "40" and partial_amount <= "55":
        partial_volumetric = "1/2 cup"
    elif partial_amount > "55" and partial_amount <= "67":
        partial_volumetric = "2/3 cup"
    elif partial_amount > "67" and partial_amount <= "85":
        partial_volumetric = "3/4 cup"
    else:
        # If partial volume is more than 0.86 cups, add to whole volume
        # Convert whole cup/can volume amount to integer
        whole_cans_or_cups = int(whole_cans_or_cups)
        whole_cans_or_cups += 1
        

   
    print(f"{whole_cans_or_cups} {partial_volumetric}")
    return render_template("der.html", rer=rer, current_food_per_day=food_amount_per_day, name=name)

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

