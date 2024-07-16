"""A Todo List website that helps the user keep track of tasks
they need to get done throughout the week"""

import calendar
from datetime import date
from flask import Flask, flash, redirect, render_template, \
    request, session, url_for
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user
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

# ---------------------- Configure Database ----------------------- #

# Create Database
class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks_todo.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure Tables
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
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
    return render_template("index.html", calendar=calendar_html)

            

# TODO: Create week view page
    # TODO: Allow the user to choose what day their week starts from
        # TODO: Allow the user to edit their previous choice of starting day
    
# TODO: Create day view page
@app.route("/today", methods=["GET", "POST"])
def today():
    """Loads in the view of the current day"""
    
    today_date = date.today()
    today_date_full = today_date.strftime("%x")
    
    print(today_date_full)
    print(today_date.day)
    return render_template("today.html", date=today_date_full,
                           day=today_date.day)
    

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
                return redirect(url_for('login'))
            
            else:
                flash(f"Logged in as {username}!")
                
                # Remember which user has logged in
                session["user_id"] = user.id
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
            find_user = db.session.execute(db.select(Users).where(Users.username == request.form.get("username")))
            user = find_user.scalar()
            
            # Check if username exists already in the database
            if len(user) != 0:
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
                add_user = Users(
                    username=request.form.get("username"),
                    password=hashed_password
                )
                
                db.session.add(add_user)
                db.session.commit()  
                
                # Remember which user has logged in
                login_user(add_user)
                                    
            except Exception as e:    
                flash(f"Can't insert new user into database, exception: {e}")
                return redirect(url_for("register"))
        
            session["user_id"] = user[0]["user_id"]
                
            # TODO: Upon registering, redirect the user to the calendar settings page
    
        
    return render_template("register.html")


@app.route("/logout")
def logout():
    """Logs user out"""
    
    # Clears the user_id
    session.clear()
    
    # Redirect to home
    return redirect("/")


# TODO: Create task submission page
    # TODO: Allow the user to choose task color on the calendar
    # TODO: Name the task
    # TODO: Ask for time started and task duration
    


