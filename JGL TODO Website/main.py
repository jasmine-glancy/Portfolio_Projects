"""A Todo List website that helps the user keep track of tasks
they need to get done throughout the week"""

import calendar
from datetime import date
from flask import Flask, flash, redirect, \
    render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_login import current_user, UserMixin, login_user, LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
import os
from werkzeug.security import check_password_hash, generate_password_hash


# --------------------------- App Setup --------------------------- #

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
app.config["SECRET_KEY"] = os.environ.get("KEY")

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------------- Configure Database ----------------------- #

# Create Database
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks_todo.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

# Configure Tables
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    pref_starting_day: Mapped[str] = mapped_column(String(250), nullable=True)
    tasks = relationship("Tasks", backref="user")
    
class Tasks(db.Model):
    __tablename__ = "tasks"
    task_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    task_name: Mapped[str] = mapped_column(String(250), nullable=False)
    task_date: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    priority_level: Mapped[int] = mapped_column(Integer, nullable=False)
    task_color: Mapped[str] = mapped_column(String(10), nullable=False)
    
with app.app_context():
    db.create_all()
    
# User loader function
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# -------------------------- App Routes --------------------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    """Loads in the calendar for the current month"""
    
    c = calendar.HTMLCalendar()
    
    # Get the calendar for the current month
    today = date.today()
    
    calendar_html = c.formatmonth(today.year, today.month, withyear=True)
    
    # TODO: The calendar should have buttons to add a new task

    # TODO: If the user is logged in and the user has tasks
        # TODO: Load in bars to represent each TODO of the day
            # TODO: allow colors to overlap
            
    # TODO: Allow the user to "zoom" in on a day and week
    return render_template("index.html", calendar=calendar_html, current_user=current_user)

            

# TODO: Create week view page
    # TODO: Allow the user to choose what day their week starts from
        # TODO: Allow the user to edit their previous choice of starting day
    

@app.route("/today", methods=["GET", "POST"])
def today():
    """Loads in the view of the current day"""
    
    today_date = date.today()
    today_date_full = today_date.strftime("%x")
    
    print(today_date_full)
    print(today_date.day)
    return render_template("today.html", date=today_date_full,
                           day=today_date.day,
                           current_user=current_user)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs an existing user in"""
        
    # Checks if the user's data is validated 
    if request.method == "POST":

        # Check username and hashed password against the database
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            
            user_lookup = db.session.execute(db.select(Users).where(Users.username == username))
            user = user_lookup.scalar()
            
            if user == None:
                flash("Username not found.")
                return redirect(url_for('login'))
        
            # Ensure username exists and password is correct
            elif not check_password_hash(user.password, password):
                flash("Invalid password.")
                return redirect(url_for('login', current_user=current_user))
            
            else:
                flash(f"Logged in as {username}!")
                
                # Remember which user has logged in
                login_user(user)
                return redirect(url_for("home"))
        except Exception as e:
            flash(f"Can't log in. Exception: {e}")
            return redirect(url_for('login', current_user=current_user))
     
    return render_template("login.html", current_user=current_user)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user"""
    
    if request.method == "POST":
        
        try:
            # Check user against info in the database
            find_user = db.session.execute(db.select(Users).where(Users.username == request.form.get("username")))
            user = find_user.scalar()
            
            print(f"User: {user}")
            # Check if username exists already in the database
            if user is not None:
                flash("That username already taken.")
                return redirect(url_for("register", current_user=current_user))
            # Check if the user's password matches the password verification
            elif request.form.get("password") != request.form.get("confirm_password"):
                flash("Passwords must match.")
                return redirect(url_for("register", current_user=current_user))

            # If all checks pass, hash password
            hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        except Exception as e:
            flash(f"Can't register new user, exception: {e}")
            return redirect(url_for("register", current_user=current_user))
        else:
            # Insert data if all checks pass
            try:
                print(f"Username: {request.form.get("username")}", f"Password: {hashed_password}")
                # Insert new info into database
                add_user = Users(
                    username=request.form.get("username"),
                    password=hashed_password
                )
                
                db.session.add(add_user)
                db.session.commit()  
                
                # Remember which user has logged in
                login_user(add_user)
                                    
                # Upon registering, redirect the user to the calendar settings page
                return redirect(url_for("preferences", current_user=current_user, user_id=add_user.id))
        
            except Exception as e:    
                flash(f"Can't insert new user into database, exception: {e}")
                return redirect(url_for("register", current_user=current_user))
                

    return render_template("register.html", current_user=current_user)


@app.route("/logout")
def logout():
    """Logs user out"""
    
    # Clears the user_id
    session.clear()
    
    # Redirect to home
    return redirect(url_for("home", current_user=current_user))


@app.route("/preferences/<int:user_id>", methods=["GET", "POST"])
def preferences(user_id):
    """Set week view preferences"""
    
    if request.method == "POST":
        starting_day = request.form.get("start_day")
        
        print(f"Starting day: {starting_day}")
        try:
            # Find user in the database
            found_user = Users.query.get(user_id)
            
            if found_user:
                # Update preferred starting day
                found_user.pref_starting_day = starting_day
                
                # Update the database
                db.session.commit()
            
                print("Preferred starting day updated")
            else:
                flash("User not found")
                
            return redirect(url_for("home", current_user=current_user))
        except Exception as e:
            # Revert if there is an error
            db.session.rollback()
            flash(f"Can't update starting day, exception: {e}")
        
    return render_template("user_preferences.html", current_user=current_user)
# TODO: Create task submission page
    # TODO: Allow the user to choose task color on the calendar
    # TODO: Name the task
    # TODO: Ask for time started and task duration
    


