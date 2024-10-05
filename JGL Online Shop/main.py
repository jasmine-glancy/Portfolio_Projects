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

@app.template_filter("get_image_alt")
def get_image_alt(product_id):
    """Returns the alt for the image"""
    
    product_or_service = q.find_product_by_id(product_id)
    
    product_service_alt = product_or_service.image_alt
    
    return product_service_alt

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

@app.template_filter("update_unique_items")
def update_unique_items(unique_items, item_key, quantity):
    """Update the unique items dictionary with the summed quantity."""
    if item_key in unique_items:
        unique_items[item_key] += quantity
    else:
        unique_items[item_key] = quantity
    return unique_items

@app.template_filter("display_price")
def display_price(item_id):
    """Finds the rate of a project or service"""
    
    product_or_service = q.find_product_by_id(item_id)
    
    rate = product_or_service.rate
    
    # Format the total price to two decimal places
    formatted_rate = f"{rate:.2f}"
    
    return formatted_rate

@app.template_filter("display_unit")
def display_unit(item_id):
    """Finds the rate unit of a project or service"""
    
    product_or_service = q.find_product_by_id(item_id)
    
    rate_unit = product_or_service.rate_unit
    
    return rate_unit

@app.template_filter("display_leather_notes")
def display_leather_notes(item_id):
    """Finds the rate unit of a project or service"""
    
    product_or_service = q.find_product_by_id(item_id)
    
    notes = product_or_service.notes
    
    return notes
    

# Register the blueprint for routes 
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)