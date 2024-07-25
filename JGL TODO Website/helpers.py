
from datetime import datetime
from flask import Flask
from flask_login import current_user
from task_tracking import db, Tasks


# Configure application
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks_todo.db"
db.init_app(app)

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

def task_lookup(month, day, year):
    """Look up task information"""
    
    # Pad the date with 0s if it's within the first 10 days of the month
    day_date = f"{year}-{int(month):02d}-{int(day):02d}"
        
    task_lookup = db.session.execute(db.select(Tasks).where((Tasks.user_id == current_user.id) & (Tasks.task_date == day_date)))
    print(task_lookup)
    tasks = task_lookup.scalars().all()
    print(tasks)
    
    return tasks