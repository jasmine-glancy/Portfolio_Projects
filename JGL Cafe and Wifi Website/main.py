"""A Flask/HTML website that lists cafes with wifi and 
power for remote working"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
app.config["SECRET_KEY"] = os.environ.get("KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    """Shows all of the cafes in the database"""
    
    # TODO: Displays the info of
    ## all of the cafes
        # Name, location, google maps link, hours, 
        # coffee price, wifi price, charging availability,
        # seats
    return render_template("index.html")

# INSERT INTO remote_spaces ("name", 
# 	"img_url",
# 	"map_url",
# 	"location",
#   "website",
#   "open_24_hours",
# 	"seats",
# 	"socket_availability",
# 	"has_toilet",
# 	"has_wifi",
# 	"can_take_calls") 
# TODO: Create add route
# TODO: Create edit route