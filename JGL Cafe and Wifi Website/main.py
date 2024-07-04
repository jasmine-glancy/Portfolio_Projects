"""A Flask/HTML website that lists cafes with wifi and 
power for remote working"""

from cs50 import SQL
from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
app.config["SECRET_KEY"] = os.environ.get("KEY")

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///remote_workspaces.db")

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
    
@app.route("/", methods=["GET", "POST"])
def home():
    """Shows all of the cafes in the database"""
    
    cafe_results = db.execute(
        "SELECT * FROM remote_spaces"
    )
    print(cafe_results)
    print(type(cafe_results[0]["last_modified"]))
    # TODO: Displays the info of
    ## all of the cafes
        # Name, location, google maps link, hours, 
        # coffee price, wifi price, charging availability,
        # seats
    return render_template("index.html", cafe_results=cafe_results)

# INSERT INTO remote_spaces ("name", 
# 	"img_url",
# 	"map_url",
# 	"location",
#     "website",
#     "open_24_hours",
# 	"seats",
# 	"socket_availability",
# 	"has_toilet",
# 	"has_wifi",
# 	"can_take_calls") VALUES ("Chanticleer Cafe & Bakery", 
# 	"https://foodcary.com/wp-content/uploads/2016/06/chanticleer-1491.jpg",
# 	"https://www.google.com/maps/dir//6490+Tryon+Rd,+Cary,+NC+27518",
# 	"Cary, NC",
#     "http://chanticleercafe.com",
#     "no",
# 	"5",
# 	"0",
# 	"3",
# 	"3",
# 	"1");
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
# 	"last_modified") VALUES ("MILKLAB", 
# 	"https://lh3.googleusercontent.com/p/AF1QipNzyQAb3LNrvpHegClSy7U4D4QnnJRBNB2jPrIh=s680-w680-h510",
# 	"https://www.google.com/maps/dir//6418+Tryon+Rd,+Cary,+NC+27518",
# 	"Cary, NC",
#     "milklabcafe.com",
#     "no",
# 	"3",
# 	"2",
# 	"0",
# 	"2",
# 	"1",
# 	"1",
# 	"Pared-down, contemporary counter serve selling unique Asian-style rolled ice cream & tea drinks.",
# 	CURRENT_DATE);

# TODO: Add is_chain to database?
# TODO: Create add route
# TODO: Create edit route