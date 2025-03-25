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
            
            print(f"Most common colors: {top_10_colors}")
            
            first_five_colors = h.first_5_colors(top_10_colors)
            
            next_five_colors = h.last_5_colors(top_10_colors)
            
            print(f"First 5 colors: {first_five_colors}", f"Next 5 colors: {next_five_colors}")
            
            first_5_rgb = h.individual_rgb_values(first_five_colors)
                        
            next_5_rgb = h.individual_rgb_values(next_five_colors)
            
            # print(first_5_rgb, next_5_rgb)
            
            formatted_first_five_colors = h.format_colors(first_five_colors)
            
            # print(f"Formatted 1st 5 colors: {formatted_first_five_colors}")
            
            formatted_last_five_colors = h.format_colors(next_five_colors)
            
            # print(f"Formatted next 5 colors: {formatted_last_five_colors}")
            

        return f.render_template("index.html",
                                 first_five_colors=first_5_rgb,
                                 next_five_colors=next_5_rgb,
                                 formatted_first_five_colors=formatted_first_five_colors,
                                 formatted_last_five_colors=formatted_last_five_colors,
                                 chosen_file=chosen_file,
                                 zip=zip)
   
    return f.render_template("index.html")


