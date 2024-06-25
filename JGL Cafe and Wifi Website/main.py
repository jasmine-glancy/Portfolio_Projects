"""A Flask/HTML website that lists cafes with wifi and 
power for remote working"""

from flask import Flask
from flask_bootstrap import Bootstrap5
import os

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap5(app)

# Load in security key
app.config["SECRET_KEY"] = os.environ.get("KEY")

# TODO: Create index route
# TODO: Create cafes route which displays the info of
## all of the cafes
    # Name, location, google maps link, hours, 
    # coffe price, wifi price, charging availability,
    # seats
    
# TODO: Create add route
# TODO: Create edit route