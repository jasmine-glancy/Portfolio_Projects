from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import requests


# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap5(app)

@app.route("/")
def home():
    """Shows portfolio homepage with a current copyright date"""
    
    # Convert current date to a string
    jgl_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Grab only the year
    jgl_current_year = jgl_date_str[:4]
    return render_template("index.html", date=jgl_current_year)
