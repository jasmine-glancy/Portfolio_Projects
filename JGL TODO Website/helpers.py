
from datetime import datetime
from flask import Flask
from flask_login import current_user
from sqlalchemy import and_
from task_tracking import db, Tasks


# Configure application
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks_todo.db"
db.init_app(app)

# ----------------- Custom Jinja Template Filters ----------------- #

@app.template_filter("str_to_time")
def str_to_time(time_string, format="%I:%M %p"):
    """Custom filter to convert a string to datetime"""
    
    try:
        time_object = datetime.strptime(time_string, format)
    except ValueError:
        # If time isn't in correct format, reformat to 24-hour
        time_object = datetime.strptime(time_string, "%H:%M")

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
        
    task_lookup = db.session.execute(
        db.select(Tasks).where(
            and_(
                Tasks.user_id == current_user.id),
                Tasks.task_date == day_date))
    tasks = task_lookup.scalars().all()
    
    return tasks

def load_priorities(month, day, year):
    """Look up priorities in order from most to least urgent"""
    
    # Pad the date with 0s if it's within the first 10 days of the month
    day_date = f"{year}-{int(month):02d}-{int(day):02d}"
    
    priority_lookup = db.session.execute(
        db.select(Tasks).where(
            and_(
                Tasks.user_id == current_user.id,
                Tasks.task_date == day_date,
                Tasks.priority_level >= 1,
            )
        ).order_by(Tasks.priority_level.desc())
    )
    priorities = priority_lookup.scalars().all()
    
    return priorities