from datetime import datetime
import flask as f 

bp = f.Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def home():
    
     # Convert current date to a string
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Grab only the year
    current_year = date_str[:4]
    
    return f.render_template("index.html",
                             date=current_year)