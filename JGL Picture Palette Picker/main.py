"""
A website that picks the top 10 most common colors in an uploaded image
"""

import flask as f
import helpers as h

# Configure application

app = f.Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    
    if f.request.method == "POST":
        
        if "uploaded_file" not in f.request.files:
            f.flash("Can't find file")
            
            return f.redirect(f.url_for("home"))
        
        chosen_file = f.request.files["uploaded_file"]
        
        if chosen_file.filename == "":
            f.flash("Please select a file.")
            
            return f.redirect(f.url_for("home"))
        
        if chosen_file:
            
            # Finds the most common colors in the uploaded image

            top_10_colors = h.most_frequest_colors(chosen_file)
        
            image = f"Your image: {chosen_file}"
            
            print(f"Most common colors: {top_10_colors}")

        return f.render_template("index.html", colors=top_10_colors, chosen_file=chosen_file, image=image)
   
    return f.render_template("index.html")


