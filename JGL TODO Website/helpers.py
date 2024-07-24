
from datetime import datetime
from flask import Flask

# Configure application
app = Flask(__name__)

# ----------------- Custom Jinja Template Filters ----------------- #

@app.template_filter("str_to_time")
def str_to_time(time_string, format="%I:%M %p"):
    """Custom filter to convert a string to datetime"""
    
    time_object = datetime.strptime(time_string, format)

    return time_object.time()

@app.template_filter("format_time")
def format_time(time):
    formatted_time = time.strftime("%I:%M %p").lstrip("0")
    print(formatted_time)
    
    return formatted_time
