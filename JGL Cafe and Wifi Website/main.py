"""A Flask/HTML website that lists cafes with wifi and 
power for remote working"""

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, \
    render_template, request, session, url_for
from flask_bootstrap import Bootstrap
import os
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash



# --------------------------- App Setup --------------------------- #

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

API_KEY = os.environ.get("KEY")
# Load in security key
app.config["SECRET_KEY"] = API_KEY

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///remote_workspaces.db")

# ----------------- Custom Jinja Template Filters ----------------- #

# A custom filter to convert string to datetime, suggested by CoPilot
@app.template_filter("str_to_datetime")
def str_to_datetime(s, format="%x"):
    date_object = datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    
    return date_object.strftime(format)

@app.template_filter("check_if_chain")
def check_if_chain(chain_value):
    """Returns the kind of chain the cafe is"""
    
    try:
        chain_info = db.execute(
            "SELECT chain_type from chains WHERE chain_id = :chain",
            chain=chain_value
        )
        
        return chain_info[0]["chain_type"]
    except Exception as e:
        print(f"Chain value not found, exception: {e}")
    
# -------------------------- App Routes -------------------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    """Shows all of the cafes in the database"""
    
    cafe_results = db.execute(
        "SELECT * FROM remote_spaces"
    )
    print(cafe_results)
    print(type(cafe_results[0]["last_modified"]))
    
    return render_template("index.html", cafe_results=cafe_results)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs an existing user in"""
        
    # Checks if the user's data is validated 
    if request.method == "POST":

        # Check username and hashed password against the database
        try:
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
                session["user_id"] = user_lookup[0]["user_id"]
                return redirect(url_for("home"))
        except Exception as e:
            flash(f"Can't log in. Exception: {e}")
            return redirect(url_for('login'))
    
        
        
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user"""

    
    if request.method == "POST":
        
        try:
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

            # If all checks pass, hash password
            hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        except Exception as e:
            flash(f"Can't register new user, exception: {e}")
            return redirect(url_for("register"))
        else:
            # Insert data if all checks pass
            try:
                # Insert new info into database
                db.execute("INSERT INTO users (username, password) VALUES(?, ?)", request.form.get("username"), hashed_password)
                    
                user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            except Exception as e:    
                flash(f"Can't insert new user into database, exception: {e}")
                return redirect(url_for("register"))
        
            # Remember which user has logged in
            session["user_id"] = user[0]["user_id"]
            session["logged_in"] = True
            
            logged_in = session["logged_in"]
                
            # Redirect to home
            return render_template("index.html", logged_in=logged_in)
        
    return render_template("register.html")


@app.route("/logout")
def logout():
    """Logs user out"""
    
    # Clears the user_id
    session.clear()
    
    # Redirect to home
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
def add():
    """Adds a new cafe to the database"""

    
    if request.method == "POST":
        cafe_name = request.form.get("name")
        img = request.form.get("img")
        location = request.form.get("location")
        map_url = request.form.get("map_link")
        
        if map_url.startswith("http://") or map_url.startswith("https://"):
            map_url = map_url
        else:
            map_url = f"https://{map_url}"
            
        website = request.form.get("website")
        open_24_hours = request.form.get("all_hours")
        chain = request.form.get("chain")
        seating = request.form.get("seating")
        price = request.form.get("price")
        sockets = request.form.get("sockets")
        bathrooms = request.form.get("bathrooms")
        wifi = request.form.get("wifi")
        calls = request.form.get("calls")
        description = request.form.get("description")
        
        print(cafe_name, img, location, map_url, website)
        print(open_24_hours, chain, seating, price, sockets)
        print(bathrooms, wifi, calls, description)
        
        current_date = datetime.today()
        try:
            db.execute(
                "INSERT INTO remote_spaces \
                    (name, img_url, map_url, location, \
                      website, open_24_hours, seats, price, \
            	      socket_availability, has_toilet, has_wifi, \
            	      can_take_calls, description, is_chain, last_modified) \
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       cafe_name, img, map_url, location, website,
                       open_24_hours, seating, price, sockets, 
                       bathrooms, wifi, calls, description, chain,
                       current_date
            )
        except Exception as e:
            flash(f"Can't insert new cafe. Exception: {e}")
            return redirect(url_for("add"))
        
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit/<workspace_id>", methods=["GET", "POST"])
def edit(workspace_id):
    """Allows a user to edit a cafe's information"""
    
    if request.method == "POST":
        print("POSTING")
        
        cafe_name = request.form.get("name")
        img = request.form.get("img")
        location = request.form.get("location")
        map_url = request.form.get("map_link")
        
        if map_url.startswith("http://") or map_url.startswith("https://"):
            map_url = map_url
        else:
            map_url = f"https://{map_url}"
            
        website = request.form.get("website")
        open_24_hours = request.form.get("all_hours")
        chain = request.form.get("chain")
        seating = request.form.get("seating")
        price = request.form.get("price")
        sockets = request.form.get("sockets")
        bathrooms = request.form.get("bathrooms")
        wifi = request.form.get("wifi")
        calls = request.form.get("calls")
        description = request.form.get("description")
        

        current_date = datetime.today()
        try:
            db.execute(
                "UPDATE remote_spaces set name = :name, \
                    img_url = :img, map_url = :map_url, location = :location, \
                      website = :website, open_24_hours = :open_24_hours, \
                          seats = :seating, price = :price, socket_availability = :sockets, \
                              has_toilet = :bathrooms, has_wifi = :wifi, \
                                  can_take_calls = :calls, description = :description, \
                                      is_chain = :chain, last_modified = :date \
                                          WHERE workspace_id = :workspace_id",
                       name=cafe_name, img=img, map_url=map_url, 
                       location=location, website=website, open_24_hours=open_24_hours, 
                       seating=seating, price=price, sockets=sockets, 
                       bathrooms=bathrooms, wifi=wifi, calls=calls, 
                       description=description, chain=chain, date=current_date,
                       workspace_id=workspace_id
            )
            
            return redirect(url_for("home"))
        except Exception as e:
            print(f"Can't edit cafe. Exception: {e}")
            return redirect(url_for("edit", workspace_id=workspace_id))
        
    # If GET
    try:
        workspace_query = db.execute(
            "SELECT * FROM remote_spaces WHERE workspace_id = :workspace",
            workspace=workspace_id
        )
        
        print(workspace_query)
        
        cafe = workspace_query[0]
        
        print(cafe["open_24_hours"], type(cafe["open_24_hours"]))
        print(cafe["description"])
        return render_template("edit.html", cafe=cafe)
        
    except Exception as e:
        flash(f"Can't find workspace. Exception: {e}")
        
    return render_template("edit.html")


@app.route("/delete_workspace/<int:workspace_id>", methods=["DELETE"])
def delete_workspace(workspace_id):
    
    if request.args.get("api-key") == API_KEY:
        try:
            #TODO: Select cafe based on the api key
            
            db.execute(
                "DELETE FROM remote_workspaces WHERE workspace_id = :id",
                id = workspace_id
            )
            
            return jsonify(response={"success": "Successfully deleted from the database!"}), 200
        except NotFound:
            return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database"}), 404
    else:
        return jsonify(error={"Not Found": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403
