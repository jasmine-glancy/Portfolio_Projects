"""
A website that picks the top 10 most common colors in an uploaded image
"""

import flask as f

# Configure application

app = f.Flask(__name__)

@app.route("/")
def home():
    
    # TODO: Handle the file upload
    
    return f.render_template("index.html")


# TODO: Use NumPy to find the most common colors in the uploaded image