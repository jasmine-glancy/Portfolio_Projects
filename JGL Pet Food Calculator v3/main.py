"""Welcome to the Pet Food Calculator!"""

from cs50 import SQL
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_bootstrap import Bootstrap5
from forms import NewSignalment, GetWeight, ReproStatus, LoginForm, RegisterForm, WorkForm, FoodForm
from helpers import login_check_for_species, der_factor, check_if_pregnant, calculcate_rer, find_repro_status, \
    find_breed_id, find_pet_id, convert_decimal_to_volumetric, find_food_form, pet_data_dictionary, check_litter_size, \
        check_if_nursing, check_obesity_risk, check_if_pediatric, clear_variable_list
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


@app.route("/calculate_new_pet")
def new_pet_calc():
    """Redirects to the start of the form, while clearing session variables"""
    session["previous_route"] = "new_pet"
    
    # Clear variables (except user ID)
    clear_variable_list()
    
    return redirect(url_for('pet_info'))


@app.route("/recalculate_for_pet")
def recalculate_pet():
    """Redirects to the start of the form, while clearing session variables"""
    session["previous_route"] = "recalculate"
    
    # Clear variables (except user ID)
    clear_variable_list()
    
    return redirect(url_for('finished_reports'))

            
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


@app.route("/get-signalment/", methods=["GET", "POST"])
def pet_info():
    """Gets the pet's signalment, i.e. name, age, sex/reproductive status, breed, species"""
    
    id = None
    try:
        pet_id = request.args.get("id") 
        print(f"pet ID: {pet_id}")
        id = find_pet_id(pet_id) 
    except Exception as e:
        print(f"Couldn't find ID, Exception: {e}")
    else:
        
        print(f"user_id: {session['user_id']}, pet_id: {id}")  # Add this line

        
    form = NewSignalment()
    
    if request.method == "POST":
        
        species = form.pet_species.data
        pet_name = form.pet_name.data.title()
        
        print(type(species))
        print(type(pet_name))
        
        
        # Show an error message if the user doesn't choose a species
        if species == "default":
            flash("Please choose a species from the dropdown.")
            return render_template("get_signalment.html", form=form)

        # Add pet to the database if the user is logged in
        if session["user_id"] != None:
            

            if pet_id is not None:    
                
                
                print(f"user_id: {session['user_id']}, pet_id: {id}")  # Add this line

                # See if the pet is already added
                find_existing_pet = db.execute(
                    "SELECT name FROM pets WHERE owner_id = :user_id AND pet_id = :pet_id",
                    user_id=session["user_id"], pet_id=id
                )
                
                if find_existing_pet:

                    try:
                        db.execute(
                            "UPDATE pets SET name = :updated_name, species = :updated_species WHERE pet_id = :pet_id AND owner_id = :user_id",
                            updated_name=pet_name, updated_species=species, pet_id=id, user_id=session["user_id"]
                        )
                    except Exception as e:
                        flash(f"Unable to update data, Exception: {e}")
                    else:
                        session["species"] = species
                        session["pet_name"] = pet_name
            else:
                # If no pet is found (i.e. new pet in the database), create new session variable and store pet
                # Store session variables
                session["species"] = species
                session["pet_name"] = pet_name
                
                try:
                    db.execute(
                        "INSERT INTO pets (owner_id, name, species) VALUES (?, ?, ?)",
                        session["user_id"], pet_name, species
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
        canine_breed_list = db.execute(
            "SELECT Breed FROM dog_breeds ORDER BY Breed"
        )
        
        if canine_breed_list != None:
            pet_breed += canine_breed_list
            
    if species == "Feline":
        feline_breed_list = db.execute(
            "SELECT Breed FROM cat_breeds ORDER BY Breed"
        )
        if feline_breed_list != None:
            pet_breed += feline_breed_list
        
    
    if request.method == "POST":
        pet_sex = form.pet_sex.data
        pet_age_years = form.pet_age.data
        pet_age_months = form.pet_age_months.data 
        pet_breed = request.form.get("pet_breed")


        # Show an error message if the user doesn't choose a breed or sex
        if pet_breed == None and pet_sex == "default":
            flash("Please choose a breed and your pet's reproductive status from the dropdown menus.")
            return redirect(url_for('pet_info_continued'))
        elif pet_breed == None and pet_sex != "default":
            flash("Please choose a breed from the dropdown menus.")
            return redirect(url_for('pet_info_continued'))
        elif pet_breed != None and pet_sex == "default":
            flash("Please choose your pet's reproductive status from the dropdown menus.")
            return redirect(url_for('pet_info_continued'))    
        else:
            # Create new session variables
            session["pet_sex"] = pet_sex
            session["pet_age_years"] = pet_age_years
            session["pet_age_months"] = pet_age_months
            session["pet_breed"] = pet_breed
            # print(pet_breed)
            
            # print(pet_age_years)
            # print(pet_age_months)
            # print(pet_breed)
            # print(pet_sex)
            # print(session["pet_name"])
            # print(session["user_id"])
            
            # Convert months to years for easier logic reading
            partial_years = float(pet_age_months / 12)
            pet_age = pet_age_years + partial_years    
            
            print(pet_age)   
            
            # Set flags to see if a pet is between pediatric and sexually mature ages
            is_pediatric = "n"
            not_pediatric_not_mature = False
            sexually_mature = False
            # Search for pet breed code in breed database
            if species == "Canine":
                breed_id_result = db.execute(
                    "SELECT BreedID FROM dog_breeds WHERE Breed = ?", pet_breed
                )
                
                breed_id = breed_id_result[0]["BreedID"]
            
                print(f"breed_id: {breed_id}")
                
                # Find breed size category
                breed_size_results = db.execute(
                    "SELECT SizeCategory FROM dog_breeds WHERE BreedID = ?;", breed_id
                )
                
                breed_size = breed_size_results[0]["SizeCategory"]
                
                print(breed_size)
                
                if breed_size == "X-Small" or breed_size == "Small" or breed_size == "Medium":
                    if pet_age < 0.33:
                        # Puppies under 4 months old have a DER modifier of * 3.0 factor_id 13
                        print("DER Modifier * 3.0")
                        der_factor_id = 13
                        is_pediatric = "y"
                    elif pet_age >= 0.33 and pet_age <= 0.66:
                        # Toy/small/medium breed puppies between 4 and 8 months of age have a DER modifier of * 2.5
                        print("DER Modifier * 2.5")
                        der_factor_id = 15
                        is_pediatric = "y"
                    elif pet_age > 0.66 and pet_age <= 1:
                        # Toy/small/medium breed puppies between 8 and 12 months of age have a DER modifier of * 1.8-2.0
                        print("DER Modifier * 1.8-2.0")
                        der_factor_id = 18
                        is_pediatric = "y"
                    elif pet_age > 1 and pet_age < 2:
                        # Toy/small/medium breed dogs that aren't pediatric but aren't sexually matue
                        not_pediatric_not_mature = True
                    else:
                        # Pets over 2 years old
                        sexually_mature = True
                            
                elif breed_size == "Large":
                    if pet_age < 0.33:
                        # Large breed puppies under 4 months old have a DER modifier of * 3.0 factor_id 13
                        print("DER Modifier * 3.0")
                        der_factor_id = 13
                        is_pediatric = "y"
                    elif pet_age > 0.33 and pet_age <= 0.91:
                        # Large breed puppies between 4 and 11 months old have a DER modifier of * 2.5
                        print("DER Modifier * 2.5")
                        der_factor_id = 16
                        is_pediatric = "y"
                    elif pet_age > 0.91 and pet_age <= 1.5:
                        # Large breed puppies between 11 and 18 months old have a DER modifier of * 1.8-2.0
                        print("DER Modifier * 1.8-2.0")
                        der_factor_id = 18
                        is_pediatric = "y"
                    elif pet_age > 1.5 and pet_age < 2:
                        # Large breed dogs that aren't pediatric but aren't sexually matue
                        not_pediatric_not_mature = True
                    else:
                        # Pets over 2 years old
                        sexually_mature = True
                        
                elif breed_size == "X-Large":
                    if pet_age < 0.33:
                        # X-Large breed puppies under 6 months old have a DER modifier of * 3.0 factor_id 13
                        der_factor_id = 13
                        print("DER Modifier * 3.0")
                        is_pediatric = "y"
                    if pet_age > 0.5 and pet_age <= 1:
                        # X-Large breed puppies between 6 and 12 months old have a DER modifier of * 2.5
                        print("DER Modifier * 2.5")
                        der_factor_id = 17
                        is_pediatric = "y"
                    elif pet_age > 1 and pet_age <= 1.5:
                        # X-Large breed puppies between 12 and 18 months old have a DER modifier of * 1.8-2.0
                        print("DER Modifier * 1.8-2.0")
                        der_factor_id = 20
                        is_pediatric = "y"
                    elif pet_age > 1.5 and pet_age < 2:
                        # X-Large breed dogs that aren't pediatric but aren't sexually matue
                        not_pediatric_not_mature = True
                    else:
                        # Pets over 2 years old
                        sexually_mature = True
                        
                        
                # List for condensed conditionals suggested by CoPilot
                if not_pediatric_not_mature or sexually_mature:
                    if pet_sex in ["female_spayed", "male_neutered"]:
                        # Non-pediatric, sexually immature and older dogs that are neutered or spayed
                        print("DER Modifier * 1.4-1.6")
                        der_factor_id = 1
                        
                    elif pet_sex in ["male", "female"]:
                        # Non-pediatric, sexually immature or intact male dogs
                        print("DER Modifier * 1.6-1.8")
                        der_factor_id = 2
                        
                        
                        
                print(breed_size)
                
                # Add pet to the database if the user is logged in
                if session["user_id"] != None:
                    print(session["user_id"])
                    print(session["pet_name"])
                    print(breed_id, der_factor_id, pet_age_years, pet_age_months, pet_breed, pet_sex)

                    try:
                        db.execute(
                            "UPDATE pets SET canine_breed_id = :breed_id, canine_der_factor_id = :der_factor_id, \
                                age_in_years = :y, age_in_months = :m, breed = :breed, sex = :sex, is_pediatric = :pediatric_status \
                                    WHERE name = :pet_name AND owner_id = :user_id",
                                breed_id=breed_id, der_factor_id=der_factor_id, y=pet_age_years, m=pet_age_months, breed=pet_breed, \
                                    sex=pet_sex, pediatric_status=is_pediatric, pet_name=session["pet_name"], user_id=session["user_id"]
                            )
                        
                        
                    except Exception as e:
                        flash(f"Missing pet name or user ID in session. Exception: {e}")
                        return redirect(url_for("pet_info_continued", form=form, pet_breed=pet_breed, species=species))

                        
            if species == "Feline":
                breed_id_result = db.execute(
                    "SELECT BreedID FROM cat_breeds WHERE Breed = ?", pet_breed
                )    
                
                breed_id = breed_id_result[0]["BreedID"]
                print(breed_id)
                

                # DER factors suggested by https://todaysveterinarynurse.com/wp-content/uploads/sites/3/2018/07/TVN-2018-03_Puppy_Kitten_Nutrition.pdf
                # and https://www.veterinary-practice.com/article/feeding-for-optimal-growth
                if pet_age <= 0.33 or pet_age > 0.5 and pet_age <= 0.83:
                    # Kittens under 4 months old or between 7 and 10 months old have a DER modifier of * 2.0
                    print("DER Modifier * 2.0")
                    der_factor_id = 13
                    is_pediatric = "y"
                elif pet_age > 0.33 and pet_age <= 0.5:
                    #Kittens between 5 and 6 months old have a DER modifier of * 2.5
                    print("DER Modifier * 2.5")
                    der_factor_id = 14
                    is_pediatric = "y"
                elif pet_age > 0.83 and pet_age <= 1:
                    # Kittens between 10 and 12 months old have a DER modifier of * 1.8-2.0
                    print("DER Modifier * 1.8-2.0")
                    der_factor_id = 15
                    is_pediatric = "y"
                elif pet_age > 1 and pet_age < 2:
                    # Kittens that aren't pediatric but aren't sexually matue
                    not_pediatric_not_mature = True
                elif pet_age >= 2 and pet_age < 7:
                    # Pets over 2 years old
                    sexually_mature = True
                elif pet_age >= 7 and pet_age <= 11:
                    # Cats between 7 and 11 years of age have a DER modifier of * 1.1-1.4
                    print("DER Modifier * 1.1-1.4")
                    der_factor_id = 4
                elif pet_age >= 11:
                    # Cats older than 11 years have a DER modifier of * 1.1-1.6
                    print("DER Modifier * 1.1-1.6")
                    der_factor_id = 5
                    
                if not_pediatric_not_mature or sexually_mature:
                    if pet_sex in ["female_spayed", "male_neutered"]:
                        # Non-pediatric, sexually immature and older cats that are neutered or spayed
                        print("DER Modifier * 1.2-1.4")
                        der_factor_id = 1
                        
                    elif pet_sex in ["male", "female"]:
                        # Non-pediatric, sexually immature or intact male cats
                        print("DER Modifier * 1.4-1.6")
                        der_factor_id = 2


                
                # Add pet to the database if the user is logged in
                if session["user_id"] != None:
                    print (der_factor_id)
                    
                    try:
                        db.execute(
                            "UPDATE pets SET feline_breed_id = :breed_id, feline_der_factor_id = :der_factor_id, \
                                age_in_years = :y, age_in_months = :m, breed = :breed, sex = :sex, is_pediatric = :pediatric_status \
                                    WHERE name = :pet_name AND owner_id = :user_id",
                                breed_id=breed_id, der_factor_id=der_factor_id, y=pet_age_years, m=pet_age_months, breed=pet_breed, \
                                    sex=pet_sex, pediatric_status=is_pediatric, pet_name=session["pet_name"], user_id=session["user_id"]
                            )
                        
                    except Exception as e:
                        flash(f"Unable to update part 2 of signalment data, Exception: {e}")
                        return redirect(url_for("pet_info_continued", form=form, pet_breed=pet_breed, species=species))
                    
            # Store new info as session variables
            session["der_factor_id"] = der_factor_id
            session["breed_id"] = breed_id
            session["is_pediatric"] = is_pediatric
                
            
            if pet_age >= 2 and pet_sex == "female":
                # If the pet is a mature intact female, redirect to pregnancy questions
                return redirect(url_for('repro_status', species=species))
            else:
                # redirect to pet body condition score questions
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
                flash(f"Unable to insert pregnancy data, Exception: {e}")
            
            
        if pregnancy_status == "y":
            
            if species == "Canine":
                # If pet is pregnant and canine, ask how many weeks along she is
                return redirect(url_for('gestation_duration', species=species))
            else: 
                # If pet is pregnant and feline, DER factor is * 1.6-2.0
                der_factor_id = 7
                
                # Add pet info to the database if the user is logged in
                if session["user_id"] != None:
                    print (der_factor_id)
                    
                    try:
                        db.execute(
                            "UPDATE pets SET feline_der_factor_id = :der_factor_id WHERE name = :pet_name AND owner_id = :user_id",
                                der_factor_id=der_factor_id, pet_name=session["pet_name"], user_id=session["user_id"]
                            )
                        
                    except Exception as e:
                        flash(f"Unable to update feline DER factor id for gestation data, Exception: {e}")
                        
                        return redirect(url_for("repro_status", repro=repro))

            # Update session variable
            session["der_factor_id"] = der_factor_id
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
        

        # Use login check from helpers.py to verify DER factor id     
        der_factor_id = der_factor()
        # print(der_factor_id)    
        
        if number_weeks_pregnant <= "6":
            # If pet is pregnant, canine, and within the first 42 days of pregnancy, DER modifier is *~1.8
            
            if der_factor_id != 5:
                der_factor_id = 5
            
        else:
            # If pet is pregnant, canine, and within the last 21 days of pregnancy, DER modifier is *3
            
            if der_factor_id != 6:
                der_factor_id = 6
            
        print(der_factor_id)


        # Add pet info to the database if the user is logged in
        if session["user_id"] != None:
            try:
                db.execute(
                    "UPDATE pets SET weeks_gestating = :weeks_gestating, canine_der_factor_id = :der_factor_id WHERE name = :pet_name AND owner_id = :user_id",
                    weeks_gestating=number_weeks_pregnant, der_factor_id=der_factor_id, pet_name=session["pet_name"], user_id=session["user_id"]
                )
            except Exception as e:
                flash(f"Unable to update data for gestation length, Exception: {e}")
                return redirect(url_for("gestation_duration", repro=repro, species=species))
        
        # Store new info as session variables
        session["number_weeks_pregnant"] = number_weeks_pregnant
        
        # Update DER factor ID variable
        session["der_factor_id"] = der_factor_id
        
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
                flash(f"Unable to update litter size, Exception: {e}")
        
        # Use login check from helpers.py to check DER factor ID  
        der_factor_id = der_factor()

          
        if species == "Feline":
            # If the pet is a nursing feline, ask for weeks of lactation
            return redirect(url_for('lactation_duration'))
        elif species == "Canine":
            # If pet is a nursing canine, DER modifier changes based on litter size
            if litter_size == 1:
                # 1 puppy: * 3.0
                der_factor_id = 7
            elif litter_size == 2:
                # 2 puppies: 3.5
                der_factor_id = 8
            elif litter_size == 3 or litter_size == 4:
                # 3-4 puppies: 4.0
                der_factor_id = 9
            elif litter_size == 5 or litter_size == 6:
                # 5-6 puppies: 5.0
                der_factor_id = 10
            elif litter_size == 7 or litter_size == 8:
                # 7-8 puppies: 5.5
                der_factor_id = 11
            elif litter_size >= 9:
                # 9+ puppies >= 6.0
                der_factor_id = 12
                
            # Add pet to the database if the user is logged in
            if session["user_id"] != None:
                try:
                    db.execute(
                        "UPDATE pets SET canine_der_factor_id = :der_factor_id WHERE name = :pet_name AND owner_id = :user_id",
                        der_factor_id=der_factor_id, pet_name=session["pet_name"], user_id=session["user_id"]
                    )
                except Exception as e:
                    flash(f"Unable to update canine DER factor ID for litter size, Exception: {e}")
            
        # Update DER factor ID variable
        session["der_factor_id"] = der_factor_id  
            
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
                flash(f"Unable to update lactation status data, Exception: {e}")
          

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
    
    species = login_check_for_species()
    
    if request.method == "POST":
        duration_of_nursing = int(repro.weeks_nursing.data)
         
        if duration_of_nursing <= 2:
            # If the queen has been nursing for 2 weeks or less, DER modifier is RER + 30% per kitten
            der_factor_id = 8
        
        elif duration_of_nursing == 3:
            # If the queen has been nursing for 3 weeks, DER modifier is RER + 45% per kitten
            der_factor_id = 9 
        
        elif duration_of_nursing == 4:
            # If the queen has been nursing for 4 weeks, DER modifier is RER + 55% per kitten
            der_factor_id = 10 
        
        elif duration_of_nursing == 5:
            # If the queen has been nursing for 5 weeks, DER modifier is RER + 65% per kitten
            der_factor_id = 11 
        
        elif duration_of_nursing == 6:
            # If the queen has been nursing for 6 weeks, DER modifier is RER + 90% per kitten
            der_factor_id = 12 
            
        # Add pet info to the database if the user is logged in
        if session["user_id"] != None:
            try:
                db.execute(
                    "UPDATE pets SET weeks_nursing = :duration_of_nursing, feline_der_factor_id = :der_factor_id WHERE name = :pet_name AND owner_id = :user_id",
                        duration_of_nursing=duration_of_nursing, der_factor_id=der_factor_id, pet_name=session["pet_name"], user_id=session["user_id"]
                    )
            except Exception as e:
                flash(f"Unable to update nursing timeframe data, Exception: {e}")
                return redirect(url_for('lactation_duration'))
        
        # Stores nursing duration variable in session
        session["duration_of_nursing"] = duration_of_nursing
        
        # Update session variable
        session["der_factor_id"] = der_factor_id
        
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
        
        if units == "lbs":
            # Convert weight to kilograms 
            converted_weight = round((weight / 2.2), 2)
            converted_weight_units = "kgs"
        elif units == "kgs":
            # Convert weight to lbs
            converted_weight = round((weight * 2.2), 2)
            converted_weight_units = "lbs"

        
        # print(bcs)
        # print(type(bcs))
        # print(weight)
        # print(type(weight))
        # print(units)
        # print(type(units))
        
        # Use login check from helpers.py to verify DER factor ID
        der_factor_id = der_factor()
        check_litter_size()
        
            
        print(f"Weight: {weight}{units}")
        
            
        if bcs != 5:
            # Calculate ideal weight
            weight_proportion = round((100 / (((bcs - 5) * 10) + 100)), 3)
            # print(f"weight_proportion: {weight_proportion}")
            

            if units == "lbs":
                est_ideal_weight_lbs = round((weight_proportion * weight), 2)
                print(est_ideal_weight_lbs)
                
                # Calculate ideal weight in kgs
                est_ideal_weight_kgs = round((est_ideal_weight_lbs / 2.2), 2)
                print(est_ideal_weight_kgs)
                
            elif units == "kgs":
                est_ideal_weight_kgs = round((weight_proportion * weight), 2)
                print(est_ideal_weight_kgs)
                
                # Calculate ideal weight in lbs
                est_ideal_weight_lbs = round((est_ideal_weight_kgs * 2.2), 2)
                print(est_ideal_weight_lbs)

        else:
            # If pet has 5/9 on the BCS scale, set estimated ideal weight as current weight
            if units == "lbs":
                est_ideal_weight_lbs = weight
                est_ideal_weight_kgs = round((est_ideal_weight_lbs / 2.2), 2)
            elif units == "kgs":
                est_ideal_weight_kgs = weight
                est_ideal_weight_lbs = round((est_ideal_weight_kgs * 2.2), 2)
        
        # Store new info as session variables
        session["bcs"] = bcs
        session["weight"] = weight
        session["units"] = units
        session["converted_weight"] = converted_weight
        session["converted_weight_units"] = converted_weight_units
        session["ideal_weight_kgs"] = est_ideal_weight_kgs
        session["ideal_weight_lbs"] = est_ideal_weight_lbs
        
        bcs_to_body_fat = {1: "< 5", 2: "5", 3: "10", 4: "15", 5: "20",
                           6: "25", 7: "30", 8: "35", 9: ">=40"
                           }
        
        # Find body fat percentage
        percent_body_fat = bcs_to_body_fat[bcs]
        print(percent_body_fat)
        print(f"Estimated ideal weight: {est_ideal_weight_kgs} kgs, {est_ideal_weight_lbs} lbs")

        # Check for pregnancy status and nursing status
        pregnancy_status = check_if_pregnant()
        is_nursing = check_if_nursing()
        is_pediatric = check_if_pediatric()
        
        if species == "Canine":
            
            if pregnancy_status != "y" and is_nursing != "y" and is_pediatric != "y":
                # Only update DER factor id if pet isn't nursing or pregnant
                if bcs <= 4:
                    # Change DER factor id to weight gain 
                    der_factor_id = 24
                elif bcs > 5 and bcs <= 6:
                    # Change DER factor id to obese prone 
                    der_factor_id = 3
                elif bcs > 7:
                    # Change DER factor to weight loss
                    der_factor_id = 4 
                
        
            # Check if pet breed is predisposed to obesity
            obese_prone_breed = check_obesity_risk()
                
            print(obese_prone_breed)
            if obese_prone_breed == "y" and pregnancy_status != "y" and is_nursing != "y" and is_pediatric != "y":
                der_factor_id = 3
                
            # Add weight and BCS to the database if the user is logged in
            if session["user_id"] != None:
                try:
                    print(session["pet_name"])
                    print(session["user_id"])

                    db.execute(
                        "UPDATE pets SET canine_der_factor_id = :der_factor_id, bcs = :body_condition_score, \
                            ideal_weight_lbs = :ideal_weight_lbs, ideal_weight_kgs = :ideal_weight_kgs, weight = :weight, \
                                units = :units, converted_weight = :converted_weight, converted_weight_units = :converted_weight_units, \
                                    body_fat_percentage = :percent_body_fat WHERE name = :pet_name AND owner_id = :user_id",
                        der_factor_id=der_factor_id, body_condition_score=bcs, ideal_weight_lbs=est_ideal_weight_lbs, 
                            ideal_weight_kgs=est_ideal_weight_kgs, weight=weight, units=units, converted_weight=converted_weight, 
                            converted_weight_units=converted_weight_units, percent_body_fat=percent_body_fat, pet_name=session["pet_name"], 
                            user_id=session["user_id"]
                    )
                        
                except Exception as e:
                    flash(f"Unable to update canine BCS data, Exception: {e}")
                    return render_template("get_weight_and_bcs.html", form=form, species=species)
                    
                
            # Update DER factor ID variable
            session["der_factor_id"] = der_factor_id  
              
            # Gets a dog's activity level if applicable 
            return redirect(url_for('activity'))  
        
        elif species == "Feline":
             
            if pregnancy_status != "y" and is_nursing != "y" and is_pediatric != "y":
                if bcs <= 4:
                    # Change DER factor id to weight gain 
                    der_factor_id = 16
                elif bcs > 5 and bcs <= 6:
                    # Change DER factor id to obese prone 
                    der_factor_id = 3
                elif bcs > 7:
                    # Change DER factor to weight loss
                    der_factor_id = 6 
                
            # Check if pet breed is predisposed to obesity
            obese_prone_breed = check_obesity_risk()
                
            print(obese_prone_breed)
            if obese_prone_breed == "y" and pregnancy_status != "y" and is_nursing != "y" and is_pediatric != "y":
                der_factor_id = 3
            
            # Add weight and BCS to the database if the user is logged in
            if session["user_id"] != None:
                try:
                    print(session["pet_name"])
                    print(session["user_id"])

                    db.execute(
                        "UPDATE pets SET feline_der_factor_id = :der_factor_id, bcs = :body_condition_score, \
                            ideal_weight_kgs = :ideal_weight_kgs, ideal_weight_lbs = :est_ideal_weight_lbs, \
                                weight = :weight, units = :units, converted_weight = :converted_weight, \
                                    converted_weight_units = :converted_weight_units, body_fat_percentage = :percent_body_fat \
                                        WHERE name = :pet_name AND owner_id = :user_id",
                        der_factor_id=der_factor_id, body_condition_score=bcs, ideal_weight_kgs=est_ideal_weight_kgs, 
                        est_ideal_weight_lbs=est_ideal_weight_lbs, weight=weight, units=units, converted_weight=converted_weight, 
                            converted_weight_units=converted_weight_units, percent_body_fat=percent_body_fat, 
                        pet_name=session["pet_name"], user_id=session["user_id"]
                    )
                        
                except Exception as e:
                    flash(f"Unable to update feline BCS data, Exception: {e}")
                    return render_template("get_weight_and_bcs.html", form=form, species=species)


            # Update DER factor ID variable
            session["der_factor_id"] = der_factor_id  
                
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
        
        print(f'heavy_work_hours: {heavy_work_hours}, light_work_hours: {light_work_hours}')
            
        # Use login check from helpers.py to verify DER factor ID, pregnancy status, and lactation status
        der_factor_id = der_factor()
        pregnancy_status = check_if_pregnant()
        is_nursing = check_if_nursing()
        
        # Check if pet breed is predisposed to obesity
        obese_prone_breed = check_obesity_risk()
        
        
        # Pets that aren't pregnant, aren't nursing, and are obese prone
        not_preg_or_nursing_non_obese = pregnancy_status != "y" and is_nursing != "y" and obese_prone_breed != "y"
        
        # Check if a pet is pediatric
        is_pediatric = check_if_pediatric()
                
        # sources: https://wellbeloved.com/pages/cat-dog-activity-levels
        # https://perfectlyrawsome.com/raw-feeding-knowledgebase/activity-level-canine-calorie-calculations/
        if light_work_hours < 0.5 and heavy_work_hours <= 1:
            # Sedentary: 0-30 minutes of light activity daily
            activity_level = "Sedentary"
            
            if not_preg_or_nursing_non_obese and is_pediatric == "n":
                der_factor_id = 3
        elif light_work_hours >= 0.5 and light_work_hours <= 1 and heavy_work_hours == 0 or \
            light_work_hours >= 0.5 and light_work_hours <= 1 and heavy_work_hours < 1:
            # Low activity: 30 minutes to 1 hour (i.e. walking on lead)
            activity_level = "Low"
            
            if not_preg_or_nursing_non_obese and is_pediatric == "n":
                der_factor_id = 21
        elif light_work_hours >= 1 and light_work_hours <= 2 and heavy_work_hours == 0:
            # Moderate activity: 1-2 hours of low impact activity
            activity_level = "Moderate"
            
            if not_preg_or_nursing_non_obese and is_pediatric == "n":
                der_factor_id = 22
        elif heavy_work_hours >= 1 and heavy_work_hours <= 3 and light_work_hours == 0:
            # Moderate activity: 1-3 hours of high impact activity (i.e. running off-lead, playing ball, playing off-lead with other dogs)
            activity_level = "Moderate"
            
            if not_preg_or_nursing_non_obese and is_pediatric == "n":
                der_factor_id = 22
        elif heavy_work_hours > 3 and light_work_hours == 0:
            # Working and performance: 3+ hours (i.e. working dog)
            activity_level = "Heavy"
            
            if not_preg_or_nursing_non_obese and is_pediatric == "n":
                der_factor_id = 23
                    
        print(activity_level)
        # If user is logged in, add activity level to database
        if session["user_id"] != None:
            try:
                print(session["pet_name"])
                print(session["user_id"])
                print(activity_level)
                db.execute(
                    "UPDATE pets SET canine_der_factor_id = :der_factor_id, activity_level = :activity WHERE name = :pet_name AND owner_id = :user_id",
                    der_factor_id=der_factor_id, activity=activity_level, pet_name=session["pet_name"], user_id=session["user_id"]
                )
                
            except Exception as e:
                    flash(f"Unable to update activity data, Exception: {e}")
        
        else:    
            # Otherwise, create new session variables
            session["activity_level"] = activity_level
        
        # Update DER factor ID variable
        session["der_factor_id"] = der_factor_id  
        
        return redirect(url_for('confirm_data', species=species))
    
    return render_template("get_work_level.html", work=work)


@app.route("/confirm_data", methods=["GET", "POST"])
def confirm_data():
    """Confirms pet's info before taking users to the food calculator"""
    
    # Find data from from helpers.py 
    pet_data = pet_data_dictionary()
    print(pet_data)
    user_id = session["user_id"]
        
    return render_template("confirm_pet_info.html", pet_data=pet_data, user_id=user_id)
    
    
@app.route("/current_food", methods=["GET", "POST"])
def current_food():
    """Asks the user for information on their current food"""
    
    current_food = FoodForm()
    
    if request.method == "POST":
        current_food_kcal = current_food.current_food_kcal.data
        current_food_form = current_food.current_food_form.data
        meals_per_day = current_food.meals_per_day.data
        wants_transition = current_food.food_transition.data
        
        # Ensure user enters at least one meal
        try:
            if meals_per_day < 1:
                flash("Please enter a number equal to or greater than 1.")
                return render_template("current_food.html", current_food=current_food)
        except TypeError as e:
            flash("Please enter a number equal to or greater than 1.")
            return render_template("current_food.html", current_food=current_food)
        
        print(current_food_kcal)
        print(meals_per_day)
        print(wants_transition)
        print(current_food_form)

        if current_food_form == "default" and wants_transition != "default":
            flash("Please choose from the current food form dropdown.")
            return render_template("current_food.html", current_food=current_food)
        elif wants_transition == "default" and current_food_form != "default":
            flash("Please choose whether you want to transition your pet to another diet.")
            return render_template("current_food.html", current_food=current_food)
        elif current_food_form == "default" and wants_transition == "default":
            flash("Please from the current food form dropdown and whether you want to transition your pet to another diet.")
            return render_template("current_food.html", current_food=current_food)
        else:
            # If user is logged in, add current food information to the database
            if session["user_id"] != None:
                try:
                    print(session["pet_name"])
                    print(session["user_id"])
                    
                    db.execute(
                        "UPDATE pets SET meals_per_day = :meals, current_food_kcal = :current_kcal, current_food_form = :current_food_form WHERE name = :pet_name AND owner_id = :user_id",
                        meals=meals_per_day, current_kcal=current_food_kcal, current_food_form=current_food_form, pet_name=session["pet_name"], user_id=session["user_id"]
                    )
                    
                except Exception as e:
                    flash(f"Unable to update data, Exception: {e}")
                        
            
            # Otherwise, create new session variables
            session["meals_per_day"] = meals_per_day
            session["current_food_kcal"] = current_food_kcal
            session["current_food_form"] = current_food_form
                
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
        first_food_form = new_foods.new_food_one_form.data
        second_food_kcal = new_foods.new_food_two_kcal.data
        second_food_form = new_foods.new_food_two_form.data
        
        # If user is logged in, add current food information to the database
        if session["user_id"] != None:
            try:
                print(session["pet_name"])
                print(session["user_id"])
                    
                db.execute(
                    "UPDATE pets SET transitioning_food_one_kcal = :kcal_one, \
                        transitioning_food_one_form = :first_food_form, transitioning_food_two_kcal = :kcal_two, \
                            transitioning_food_two_form = :second_food_form WHERE name = :pet_name AND owner_id = :user_id",
                    kcal_one=first_food_kcal, first_food_form=first_food_form, kcal_two=second_food_kcal, second_food_form=second_food_form, pet_name=session["pet_name"], user_id=session["user_id"]
                )
                    
            except Exception as e:
                    flash(f"Unable to update transition food data, Exception: {e}")
            
        # Otherwise, create new session variables
        session["first_new_food_kcal"] = first_food_kcal
        session["first_new_food_form"] = first_food_form
        session["second_new_food_kcal"] = second_food_kcal 
        session["second_new_food_form"] = second_food_form

           
        # If user doesn't want a transition, calculate RER
        return redirect(url_for('rer'))
           
    return render_template("new_food.html", new_foods=new_foods)


@app.route("/rer", methods=["GET", "POST"])
def rer():
    """Calculates the minimum number of calories a pet needs at rest per day"""

    # Use login check from helpers.py to verify reproductive status
    sex = find_repro_status()
    rer = calculcate_rer()
    obese_prone = check_obesity_risk()
    
    object_pronoun = ""
    possessive_pronoun = ""
    print(rer)
    if sex == "female" or sex == "female_spayed":
        # Subject pronoun is she
        object_pronoun = "her"
    elif sex == "male" or sex == "male_neutered":
        # Subject pronoun is he
        object_pronoun = "him"
        possessive_pronoun = "his"

    print(object_pronoun)

    # Store as a session variable
    session["object_pronoun"] = object_pronoun
    session["possessive_pronoun"] = possessive_pronoun
    
    # Find pet's current weight so the user can know what formula was used to find their pet's RER
    if session["user_id"] != None:
        # If user is logged in, find current rer info

        try:            
            weight_data = db.execute(
                "SELECT weight, units, converted_weight, converted_weight_units \
                    FROM pets WHERE name = ? AND owner_id = ?",
                session["pet_name"], session["user_id"]
            )
            print(weight_data)          
        except Exception as e:
            flash(f"Unable to find data, Exception: {e}")
            return redirect(url_for("rer"))
        else:
            if weight_data:
                weight = weight_data[0]["weight"]
                units = weight_data[0]["units"]
                converted_weight = weight_data[0]["converted_weight"]
                converted_weight_units = weight_data[0]["converted_weight_units"]
    else:        
        # If a user isn't logged in, grab session variables
        weight = session["weight"]
        units = session["units"]
        converted_weight = session["converted_weight"]
        converted_weight_units = session["converted_weight_units"]
    
    print(f"weight: {weight} units: {units}")
    
    rer_formula_med_to_lrg = False
    rer_formula_sm = False
    rer_formula_x_large = False
    if units == "lbs":
        
        # If pet weighs more than 2kg and less than 45kg, use 30 × (BW kg) + 70 = RER
        if converted_weight >= 2 and converted_weight < 45:
            rer_formula_med_to_lrg = True
        # If pet weighs less than 2kg or more than 45kg, use 70 × (BW kg)^0.75 = RER
        elif converted_weight < 2:
            rer_formula_sm = True
        elif converted_weight >= 45:
            rer_formula_x_large = True
            
    elif units == "kgs":
        
        # If pet weighs more than 2kg and less than 45kg, use 30 × (BW kg) + 70 = RER
        if weight >= 2 and weight < 45:
            rer_formula_med_to_lrg = True
        # If pet weighs less than 2kg or more than 45kg, use 70 × (BW kg)^0.75 = RER
        elif weight < 2:
            rer_formula_sm = True
        elif weight >= 45:
            rer_formula_x_large = True
    
    print(f"weight: {weight} units: {units}")
    print(f"RER: {rer}")
    
    if obese_prone == "y":
        # If pet is an obese prone breed, set max treat kcal/day at 8% of RER
        treat_kcals = rer * 0.08
    else:
        # Calculate treat kcals per day (10% of RER)
        treat_kcals = rer * 0.1
        
    print(f"Treat kcal:{treat_kcals}")
    
    # If user is logged in, add current food information to the database
    if session["user_id"] != None:
        try:
                    
            print(session["pet_name"])
            print(session["user_id"])
                
                            
            db.execute(
                "UPDATE pets SET rer = :rer, rec_treat_kcal_per_day = :treat_kcals WHERE name = :pet_name AND owner_id = :user_id",
                rer=rer, pet_name=session["pet_name"], user_id=session["user_id"], treat_kcals=treat_kcals
            )
            print("data updated")
        except Exception as e:
            flash(f"Unable to update data, Exception: {e}")
    
    if request.method == "POST":    
        return redirect(url_for('der'))
    
    return render_template("rer.html",
                           rer=rer,
                           name=session["pet_name"],
                           pronoun=object_pronoun,
                           possessive_pronoun=possessive_pronoun,
                           weight=weight,
                           converted_weight=converted_weight,
                           units=units,
                           converted_weight_units=converted_weight_units,
                           rer_formula_med_to_lrg=rer_formula_med_to_lrg,
                           rer_formula_sm=rer_formula_sm,
                           rer_formula_x_large=rer_formula_x_large)
    
    
@app.route("/der", methods=["GET", "POST"])
def der():
    """Calculates the daily energy rate and total food amount of the current diet to feed"""
    
    # Call session variable for pronouns
    object_pronoun = session["object_pronoun"]
    possessive_pronoun = session["possessive_pronoun"]

    # Use helpers.py to verify species and check der_factor
    species = login_check_for_species()
    
    # If user is logged in, use SQL query
    if session["user_id"] != None:
        try:
            print(session["pet_name"])
            print(session["user_id"])
                
            pet_data = db.execute(
                "SELECT name, species, feline_der_factor_id, canine_der_factor_id, \
                    rer, meals_per_day, current_food_kcal, is_nursing, litter_size, weeks_nursing \
                        FROM pets WHERE owner_id = :user_id AND name = :pet_name",
                user_id=session["user_id"], pet_name=session["pet_name"]
            )       
            
            print(pet_data)
            
            if pet_data:  
                name = pet_data[0]["name"]
                rer = pet_data[0]["rer"]
                meals_per_day = pet_data[0]["meals_per_day"]
                current_food_kcal = pet_data[0]["current_food_kcal"]
                is_nursing = pet_data[0]["is_nursing"]
                litter_size = pet_data[0]["litter_size"]
                weeks_nursing = pet_data[0]["weeks_nursing"]
                
                print(weeks_nursing)
                
            print(name, rer, meals_per_day, current_food_kcal, is_nursing, litter_size)

                
        except Exception as e:
            flash(f"Unable to find pet data for DER calculation, Exception: {e}")    
            return render_template("der.html",
                            rer=rer,
                           name=name,
                           object_pronoun=object_pronoun,
                           possessive_pronoun=possessive_pronoun)
    else:
        # If a user isn't logged in, grab session variables
        name = session["pet_name"]
        rer = float(session["rer"])
        meals_per_day = session["meals_per_day"]
        current_food_kcal = session["current_food_kcal"]
        is_nursing = session["lactation_status"]
        litter_size = session["litter_size"]
        weeks_nursing = session["duration_of_nursing"]
        
        print(name, rer, meals_per_day, current_food_kcal, is_nursing, litter_size)
                
    # Use login check from helpers.py to verify DER factor ID and food form
    der_factor_id = der_factor()
    current_food_form = find_food_form()
    
    print(der_factor_id)
    print(rer, der_factor_id, meals_per_day, current_food_kcal, current_food_form)
    
    der_modifier_start_range = 0
    der_modifier_end_range = 0
    # Use DER factor id to lookup DER information by species
    if species == "Canine":
        der_lookup = db.execute(
            "SELECT life_stage, canine_der_factor_range_start, canine_der_factor_range_end, \
                ((canine_der_factor_range_start + canine_der_factor_range_end) / 2) AS mid_range \
                    FROM canine_der_factors WHERE factor_id = :der_factor_id",
                    der_factor_id=der_factor_id)
        print(der_lookup)

        # Find the start and end range of DER modifiers
        der_modifier_start_range = der_lookup[0]["canine_der_factor_range_start"]
        der_modifier_end_range = der_lookup[0]["canine_der_factor_range_end"]
        
    elif species == "Feline":
        der_lookup = db.execute(
        "SELECT life_stage, feline_der_factor_range_start, feline_der_factor_range_end, \
            ((feline_der_factor_range_start + feline_der_factor_range_end) / 2) AS mid_range \
                FROM feline_der_factors WHERE factor_id = :der_factor_id",
                der_factor_id=der_factor_id)
        print("der")
        print(F"Der lookup: {der_lookup}")

        # Find the start and end range of DER modifiers
        der_modifier_start_range = der_lookup[0]["feline_der_factor_range_start"]
        der_modifier_end_range = der_lookup[0]["feline_der_factor_range_end"]
    

    # Start with the mid range if this is the first report
    # TODO: check report date and change modifier choice based on weight changes
    der_modifier = der_lookup[0]["mid_range"]

    # Calculate DER based on the der modifier and pass variables to tempate
    if species == "Feline" and is_nursing == "y":
        der = round((rer + der_modifier * litter_size), 2)
    else:
        der = round(rer * der_modifier, 2)
    print(der)
    
    der_low_end = rer * der_modifier_start_range
    der_high_end = rer * der_modifier_end_range
    der_low_end, der_high_end = "{:.2f}".format(der_low_end), "{:.2f}".format(der_high_end)
    

    # Calculate the required calories per day
    total_calorie_amount_per_day = round(der / current_food_kcal, 2)
    
    # Breaks the food amount in to whole and partial amounts to convert to volumetric easier    
    daily_whole_cans_or_cups, daily_partial_amount = str(total_calorie_amount_per_day).split(".")[0], str(total_calorie_amount_per_day).split(".")[1]
    print(total_calorie_amount_per_day)
        
    print(f"per day whole: {daily_whole_cans_or_cups}, partial: {daily_partial_amount}")
    
    print(daily_whole_cans_or_cups)
    print(type(daily_whole_cans_or_cups))
        
    daily_partial_volumetric = convert_decimal_to_volumetric(daily_partial_amount)

    if daily_partial_volumetric == "1":
        # If partial volume is more than 0.86 cups, convert whole cup/can volume amount to integer

        daily_whole_cans_or_cups = int(daily_whole_cans_or_cups)
            
        # Then add to whole volume
        daily_whole_cans_or_cups += 1
        daily_partial_volumetric = "0"
        
    food_form = ""
    if current_food_form == "dry":
        food_form = "cup"
    elif current_food_form == "can":
        food_form = "cup"
    elif current_food_form == "pouch":
        food_form = "pouch"
    
    # Shortened conditional variables suggested by CoPilot
    whole_cans_or_cups = int(daily_whole_cans_or_cups)
    is_pouch = current_food_form == "pouch"
    is_half_tablespoon = daily_partial_volumetric == "1/2 tablespoon"
    food_form_plural = f"{food_form}{'es' if is_pouch else 's'}"

    
    if whole_cans_or_cups == 1:
        if is_half_tablespoon and daily_partial_volumetric != "0":
            daily_amount_to_feed = f"{whole_cans_or_cups} {food_form} and {daily_partial_volumetric}"
        elif not is_half_tablespoon and daily_partial_volumetric != "0":
            daily_amount_to_feed = f"{whole_cans_or_cups} and {daily_partial_volumetric} {food_form}"
        else:
            daily_amount_to_feed = f"{whole_cans_or_cups} {food_form}"
    elif whole_cans_or_cups >= 1:
        if is_half_tablespoon and daily_partial_volumetric != "0":
            daily_amount_to_feed = f"{whole_cans_or_cups} {food_form_plural} and {daily_partial_volumetric} per day"
        elif not is_half_tablespoon and daily_partial_volumetric != "0":
            daily_amount_to_feed = f"{whole_cans_or_cups} and {daily_partial_volumetric} {food_form_plural} per day"
        else:
            daily_amount_to_feed = f"{whole_cans_or_cups} {food_form_plural} per day"
    elif whole_cans_or_cups == 0 and daily_partial_volumetric != "0":
        if is_half_tablespoon:
            daily_amount_to_feed = f"{daily_partial_volumetric} per day"
        else:
            daily_amount_to_feed = f"{daily_partial_volumetric} {food_form_plural} per day"
    else:
        # Under 1 whole can or cup amount
        daily_amount_to_feed = f"{daily_partial_volumetric} per day"

    
    # Suggested by CoPilot      
    if daily_amount_to_feed.startswith("0 and "):
        daily_amount_to_feed = total_amount_per_meal.replace("0 and ", "")
    elif daily_amount_to_feed.endswith(" and 0"):
        daily_amount_to_feed = total_amount_per_meal.replace(" and 0", "")
        
    # Calculate the required calories per meal
    total_amount_per_meal = total_calorie_amount_per_day / meals_per_day
    
    print(total_amount_per_meal)
    if meals_per_day > 1:
        # Break down volume per meal if meals per day is more than 1

        # Breaks the food amount in to whole and partial amounts to convert to volumetric easier
        meal_whole_cans_or_cups, meal_partial_amount = str(total_amount_per_meal).split(".")[0], str(total_amount_per_meal).split(".")[1]
        # print(food_amount_per_day)
        
        print(f"whole cups per meal: {meal_whole_cans_or_cups}, partial cups per meal: {meal_partial_amount}")
        
        print(meal_whole_cans_or_cups)
        print(type(meal_whole_cans_or_cups))
        
        # Calculate total volumetric amounts per meal
        meal_partial_volumetric = convert_decimal_to_volumetric(meal_partial_amount)

        print(f"meal_partial_volumetric: {meal_partial_volumetric}")
        if meal_partial_volumetric == "1":
            # If partial volume is more than 0.86 cups, convert whole cup/can volume amount to integer

            meal_whole_cans_or_cups = int(meal_whole_cans_or_cups)
            
            # Then add to whole volume and reset partial volume value
            meal_whole_cans_or_cups += 1
            meal_partial_volumetric = "0"
            
        # Amount recommended depends on volumetric conversion and food form
            
        if whole_cans_or_cups == 1:
            if is_half_tablespoon and meal_partial_volumetric != "0":
                total_amount_per_meal = f"{meal_whole_cans_or_cups} {food_form} and {meal_partial_volumetric}"
            elif not is_half_tablespoon and meal_partial_volumetric != "0":
                total_amount_per_meal = f"{meal_whole_cans_or_cups} and {meal_partial_volumetric} {food_form}"
            else:
                total_amount_per_meal = f"{meal_whole_cans_or_cups} {food_form}"
        elif whole_cans_or_cups >= 1:
            if is_half_tablespoon and meal_partial_volumetric != "0":
                total_amount_per_meal = f"{meal_whole_cans_or_cups} {food_form_plural} and {meal_partial_volumetric}"
            elif not is_half_tablespoon and meal_partial_volumetric != "0":
                total_amount_per_meal = f"{meal_whole_cans_or_cups} and {meal_partial_volumetric} {food_form_plural}"
            else:
                total_amount_per_meal = f"{meal_whole_cans_or_cups} {food_form_plural}"
        elif whole_cans_or_cups == 0 and meal_partial_volumetric != "0":
            if is_half_tablespoon:
                total_amount_per_meal = f"{meal_partial_volumetric}"
            else:
                total_amount_per_meal = f"{meal_partial_volumetric} {food_form_plural}"
        elif whole_cans_or_cups == 0 and meal_partial_volumetric == "0":
            total_amount_per_meal = "0"
        else:
            # Under 1 whole can or cup amount
            total_amount_per_meal = f"{daily_partial_volumetric}"
    else:
        # If the user asks for 1 meal per day amounts, total_amount_per_meal = daily amount
        per_meal = daily_amount_to_feed.split("day")[0]
        total_amount_per_meal = f"{per_meal}meal"
    
    # Suggested by CoPilot    
    if total_amount_per_meal.startswith("0 and "):
        total_amount_per_meal = total_amount_per_meal.replace("0 and ", "")
    elif total_amount_per_meal.endswith(" and 0"):
        total_amount_per_meal = total_amount_per_meal.replace(" and 0", "")
    
    print(total_amount_per_meal)
    
    print(daily_amount_to_feed)
    # Set session variables 
            
    session["der"] = der
    session["der_modifier"] = der_modifier
    session["daily_amount_to_feed_cur_food"] = daily_amount_to_feed
    session["current_food_amt_per_meal"] = total_amount_per_meal
        
    
    # If user is logged in, add current food information to the database
    if session["user_id"] != None:
        try:
                    
            print(session["pet_name"])
            print(session["user_id"])
                                   
            db.execute(
                "UPDATE pets SET der = :der, der_modifier = :der_modifier, current_food_amt_rec = :daily_amount_to_feed, \
                    date_of_first_report = CURRENT_TIMESTAMP, most_recent_report_date = CURRENT_TIMESTAMP, \
                    current_food_amt_per_meal = :total_amount_per_meal WHERE name = :pet_name AND owner_id = :user_id",
                der=der, der_modifier=der_modifier, daily_amount_to_feed=daily_amount_to_feed, total_amount_per_meal=total_amount_per_meal, \
                    pet_name=session["pet_name"], user_id=session["user_id"]
            )
        

        except Exception as e:
            flash(f"Unable to update data, Exception: {e}")

    
    return render_template("der.html",
                           rer=rer,
                           der=der,
                           name=name,
                           meals_per_day=meals_per_day,
                           object_pronoun=object_pronoun,
                           possessive_pronoun=possessive_pronoun,
                           der_low_end=der_low_end,
                           der_high_end=der_high_end,
                           current_food_form=current_food_form,
                           total_amount_per_meal=total_amount_per_meal,
                           daily_amount_to_feed=daily_amount_to_feed,
                           der_modifier=der_modifier,
                           species=species,
                           is_nursing=is_nursing,
                           weeks_nursing=weeks_nursing)


@app.route("/completed_report", methods=["GET", "POST"])
def completed_report():
    """Return's pet's final completed report"""

    pet_data = pet_data_dictionary()
    
    rer = "{:.2f}".format(pet_data[0]["rer"])
    der = "{:.2f}".format(pet_data[0]["der"])
    
    print(der)
    object_pronoun = ""
    subject_pronoun = ""
    possessive_pronoun = ""
    if pet_data[0]["sex"] == "female" or pet_data[0]["sex"] == "female_spayed":
        object_pronoun = "her"
        subject_pronoun = "she"
    elif pet_data[0]["sex"] == "male" or pet_data[0]["sex"] == "male_neutered":
        object_pronoun = "him"
        possessive_pronoun = "his"
        subject_pronoun = "he"
        
    print(object_pronoun)
    
    # Find breed ID
    breed_id = find_breed_id()
    print(breed_id)
    
    if pet_data[0]["species"] == "Canine":
        life_stage_search = db.execute(
            "SELECT life_stage, notes FROM canine_der_factors WHERE factor_id = ?",
            pet_data[0]["canine_der_factor_id"]
        )
        
        svg_search = db.execute(
            "SELECT svg FROM dog_breeds WHERE BreedId = :breed_id",
            breed_id=breed_id
        )
        
        if svg_search[0] != None:
            # TODO: If SVG can't be found, use a placeholder
            svg = 'assets/svg/dogs/' + svg_search[0]["svg"] 
            print(svg)
            
    elif pet_data[0]["species"] == "Feline":
        life_stage_search = db.execute(
            "SELECT life_stage, notes FROM feline_der_factors WHERE factor_id = ?",
            pet_data[0]["feline_der_factor_id"]
        )
        
        # Search for breed image in database
        svg_search = db.execute(
            "SELECT svg FROM cat_breeds WHERE BreedId = :breed_id",
            breed_id=breed_id
        )
        
        if svg_search[0] != None:
            # TODO: If SVG can't be found, use a placeholder
            if pet_data[0]["species"] == "Feline":
                svg = 'assets/svg/cats/' + svg_search[0]["svg"] 
                print(svg)
                
    if life_stage_search[0] != None:
        life_stage = life_stage_search[0]["life_stage"]
        notes = life_stage_search[0]["notes"]
        

        
    if pet_data[0]["meals_per_day"]:
        meals_per_day = pet_data[0]["meals_per_day"]
    
    return render_template("complete_report.html",
                           pet_data=pet_data,
                           rer=rer,
                           der=der,
                           svg=svg,
                           meals_per_day=meals_per_day,
                           life_stage=life_stage,
                           notes=notes,
                           object_pronoun=object_pronoun,
                           subject_pronoun=subject_pronoun,
                           possessive_pronoun=possessive_pronoun)


@app.route("/finished_reports", methods=["GET", "POST"])
def finished_reports():
    """Provides a dropdown list of completed reports"""
    
    if session["user_id"] != None:
        try:
            pet_list = db.execute(
                "SELECT pet_id, name FROM pets WHERE owner_id = :user",
                user=session["user_id"]
            )
        
        except Exception as e:
            flash(f"Couldn't find pet list. Exception: {e}")
            
    # If user doesn't choose from the dropdown, provide error
    if request.method == "POST":
        pet_to_edit = request.form.get("reports")
        
        print(pet_to_edit)
        
        if pet_to_edit == None:
            flash("Please choose a pet to edit their report.")
            return redirect(url_for('finished_reports'))
        
        return redirect(url_for('edit_info', id=pet_to_edit))

    return render_template("finished_reports.html", pet_list=pet_list)

@app.route("/edit_info/", methods=["GET", "POST"])
def edit_info():
    """Allows a user to edit a pet's info and generate a new report"""
    
    pet_id = request.args.get("id")
    
    print(pet_id)
    try:
        pet_data = db.execute(
            "SELECT * FROM pets WHERE owner_id = :user_id and pet_id = :pet_id",
            user_id=session["user_id"], pet_id=pet_id
        )
    except Exception as e:
        flash(f"Unable to find pet info. Exception: {e}")
        return render_template("edit_report.html")
        
    if request.method == "POST":
        print(pet_id)
    
    return render_template("edit_report.html", pet_data=pet_data, pet_id=pet_id)
