"""A Todo List website that helps the user keep track of tasks
they need to get done throughout the week"""

import calendar
from datetime import date
from flask import Flask, flash, redirect, render_template, \
    request, session, url_for
from flask_bootstrap import Bootstrap
import os

# --------------------------- App Setup --------------------------- #

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
app.config["SECRET_KEY"] = os.environ.get("KEY")

# -------------------------- App Routes --------------------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    """Loads in the calendar for the current month"""
    
    c = calendar.HTMLCalendar()
    
    # Get the calendar for the current month
    today = date.today()
    
    calendar_html = c.formatmonth(today.year, today.month, withyear=True)
    
    return render_template("index.html", calendar=calendar_html)
# TODO: Load index page with the calendar
    # TODO: The calendar should have buttons to add a new task

    # TODO: If the user is logged in and the user has tasks
        # TODO: Load in bars to represent each TODO of the day
            # TODO: allow colors to overlap
            
    # TODO: Allow the user to "zoom" in on a day and week
    
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
# TODO: Create registration page

# TODO: Create login page

# TODO: Create task submission page
    # TODO: Allow the user to choose task color on the calendar
    # TODO: Name the task
    # TODO: Ask for time started and task duration
    


