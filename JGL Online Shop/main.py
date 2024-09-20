"""An online shop using Flask and Python"""

from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import helpers as h
import os
import queries as q

# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
KEY = os.environ.get("security_key")

JGL_CURRENT_YEAR = h.current_year()
JGL_SOCIALS = h.social_links()


@app.template_filter("datetime_format")
def datetime_format(s, format="%x"):    
    return s.strftime(format)

@app.route("/", methods=["GET", "POST"])
def home():
    """Shows homepage with a current copyright date"""
    

    
    return render_template("index.html",
                           date=JGL_CURRENT_YEAR,
                           socials=JGL_SOCIALS)

@app.route("/products", methods=["GET", "POST"])
def products():
    """Showcases a list of products and services to buy"""
    
    products_services = q.find_product_list()
    print(products_services)
    
    return render_template("products.html", 
                           date=JGL_CURRENT_YEAR,
                           socials=JGL_SOCIALS,
                           products_services=products_services)

@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def for_sale_info(product_id):
    """Provides more info on each product"""
    
    # Fetch product information based on product_id
    product = q.find_product_by_id(product_id)
    
    # Fetch leather goods for dropdown
    leather_options = q.find_leather_goods()
        
    # Fetch leather color for dropdown
    leather_colors = q.look_up_leather_colors()
    
    # Fetch metal color for dropdown
    metal_colors = q.look_up_metal_colors()
        
    # Fetch sizes for dropdown
    sizes = q.find_sizes()
    
    # TODO: If writing service
    
        # TODO: Fetch services for dropdown
    print(product)
    
    return render_template("product_page.html",
                           date=JGL_CURRENT_YEAR,
                           socials=JGL_SOCIALS,
                           product=product,
                           leather_options=leather_options,
                           leather_colors=leather_colors,
                           metal_colors=metal_colors,
                           sizes=sizes)