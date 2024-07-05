"""A Flask/HTML website that lists cafes with wifi and 
power for remote working"""

from cs50 import SQL
from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os

# --------------------------- App Setup --------------------------- #

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
app.config["SECRET_KEY"] = os.environ.get("KEY")

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///remote_workspaces.db")

# ----------------- Custom Jinja Template Filters ----------------- #

# A custom filter to convert string to datetime, suggested by CoPilot
@app.template_filter("str_to_datetime")
def str_to_datetime(s, format="%x"):
    return datetime.strptime(s, "%Y-%m-%d").strftime(format)

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

@app.route("/add", methods=["GET", "POST"])
def add():
    """Adds a new cafe to the database"""
    
    
    return render_template("add.html")

# INSERT INTO remote_spaces ("name", 
# 	"img_url",
# 	"map_url",
# 	"location",
#     "website",
#     "open_24_hours",
# 	"seats",
# 	"price",
# 	"socket_availability",
# 	"has_toilet",
# 	"has_wifi",
# 	"can_take_calls",
# 	"description",
# 	"is_chain",
# 	"last_modified") VALUES ("Brecotea", 
# 	"https://www.carymagazine.com/wp-content/uploads/2020/08/Brecotea-interior2.jpg",
# 	"https://www.google.com/maps/dir//1144+Kildaire+Farm+Rd,+Cary,+NC+27511",
# 	"Cary, NC",
#     "https://cary.brecotea.com/",
#     "no",
# 	"4",
# 	"3",
# 	"1",
# 	"2",
# 	"3",
# 	"1",
# 	"Chic bakeshop with an airy, garden-style interior & a terrace, plus varied sweet & savory bites.",
# 	"2",
# 	CURRENT_DATE);

# TODO: Create add route
# TODO: Create edit route