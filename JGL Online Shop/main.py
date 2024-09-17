"""An online shop using Flask and Python"""

from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
KEY = os.environ.get("security_key")


def current_year():
    """Returns the current year"""
    
    # Convert current date to a string
    jgl_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Grab only the year
    jgl_current_year = jgl_date_str[:4]
    
    return jgl_current_year

JGL_CURRENT_YEAR = current_year()

@app.route("/", methods=["GET", "POST"])
def home():
    """Shows homepage with a current copyright date"""
    
    return render_template("index.html", date=JGL_CURRENT_YEAR)

@app.route("/products", methods=["GET", "POST"])
def products():
    """Showcases a list of products to buy"""
    
    return render_template("onecolumn.html", date=JGL_CURRENT_YEAR)