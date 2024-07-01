"""A Flask/HTML website that lists cafes with wifi and 
power for remote working"""

from cs50 import SQL
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

@app.route("/", methods=["GET", "POST"])
def home():
    """Shows all of the cafes in the database"""
    
    cafe_results = db.execute(
        "SELECT * FROM remote_spaces"
    )
    print(cafe_results)
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
# 	"can_take_calls") VALUES ("Chanticleer Cafe & Bakery", 
# 	"https://foodcary.com/wp-content/uploads/2016/06/chanticleer-1491.jpg",
# 	"https://www.google.com/maps/dir//6490+Tryon+Rd,+Cary,+NC+27518",
# 	"Cary, NC",
#     "http://chanticleercafe.com",
#     "no",
# 	5,
# 	3,
# 	0,
# 	3,
# 	3,
# 	1);

# TODO: Add is_chain to database?
# TODO: Create add route
# TODO: Create edit route