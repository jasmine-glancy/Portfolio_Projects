"""
An online shop using Flask and Python
"""

from flask import Flask
from flask_bootstrap import Bootstrap
import os
import queries as q
from routes import bp as main_bp 

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
app.secret_key = os.environ.get("security_key")


# ------------------ Template filters ------------------ #

@app.template_filter("datetime_format")
def datetime_format(s, format="%x"):   
    """Formats the datetime""" 
    return s.strftime(format)

@app.template_filter("get_product_name")
def get_product_name(product_id):
    """Returns the name of the product"""
    
    product_or_service = q.find_product_by_id(product_id)
    
    product_service_title = product_or_service.name
    
    return product_service_title

@app.template_filter("image")
def image(product_id):
    """Returns the path for the image"""
    
    product_or_service = q.find_product_by_id(product_id)
    
    product_service_img = product_or_service.image_path
    
    return product_service_img

@app.template_filter("cart_price")
def cart_price(session_id):
    """Finds the price of the cart as a whole"""
    cart_items = q.cart_price(session_id)
    
    cart_total = cart_items.total
    
    # Format the total price to two decimal places
    formatted_total = f"{cart_total:.2f}"
    
    return formatted_total

@app.template_filter("get_option_text")
def get_option_text(product_id, option_id):
    """Returns the option text for a product"""
    
    options = q.find_option_text(product_id=product_id, option_id=option_id)

    if not options:
        return None
    
    return options

@app.template_filter("get_leather_color")
def get_leather_color(color_id):
    """Finds the color string"""
    
    leather_color = q.find_leather_color(color_id)
    
    if not leather_color:
        return None
    
    return leather_color

@app.template_filter("get_metal_color")
def get_metal_color(color_id):
    """Finds the chosen metal color"""
    
    metal_color = q.find_metal_color(color_id)
    
    if not metal_color:
        return None
    
    return metal_color

@app.template_filter("display_size")
def display_size(size_id):
    """Finds the chosen size of leather project"""
    
    size = q.get_size(size_id)
    
    if not size:
        return None
    
    return size

# Register the blueprint for routes 
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)