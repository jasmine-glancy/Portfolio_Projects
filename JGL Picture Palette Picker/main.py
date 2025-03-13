"""
A website that picks the top 10 most common colors in an uploaded image
"""

import flask as f

# Configure application

app = f.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    
    if f.request.method == "POST":
        chosen_file = f.request.form.get("submit")
        image = f"Your image: {chosen_file}"
        
        return f.render_template("index.html", image=image)
        
        
    # If posted... 
        # TODO: Handle the file upload
        
        # TODO: Use NumPy to find the most common colors in the uploaded image
        
    return f.render_template("index.html")


