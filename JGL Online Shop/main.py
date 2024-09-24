"""
An online shop using Flask and Python
"""

from datetime import datetime
from flask import Flask, render_template, request
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
    print(f"Product ID: {product.service_product_id}")
    print(f"Product Name: {product.name}")
    print(f"Product Description: {product.description}")
    print(f"Product Rate: {product.rate}")
    print(f"Product Rate Unit: {product.rate_unit}")
    print(f"Product Notes: {product.notes}")
    print(f"Product Last Updated: {product.last_updated}")
    print(f"Product Image Path: {product.image_path}")
    
    leather_options = None
    leather_colors = None
    metal_colors = None
    sizes = None
    nonfiction = None
    fiction = None 
    software = None
    
    if product_id == 1:
        # Leather options
        
        # Fetch leather goods for dropdown
        leather_options = q.find_leather_goods()
        
        # Fetch leather color for dropdown
        leather_colors = q.look_up_leather_colors()
    
        # Fetch metal color for dropdown
        metal_colors = q.look_up_metal_colors()
        
        # Fetch sizes for dropdown
        sizes = q.find_sizes()  
    elif product_id == 2:
        # For non-fiction written services
        
        # IDs non-fiction services
        nonfiction_service_options = [1, 2, 3, 7]
        nonfiction = q.writing(nonfiction_service_options)
        
        # for option in nonfiction:
        #     print("Non-fiction options:", option)

    elif product_id == 3:
        # For fiction written services
        
        # IDs of fiction services
        fiction_service_options = [4, 5, 6, 7]
        fiction = q.writing(fiction_service_options)
    
        # for option in fiction:
        #     print("Fiction options:", option)

    elif product_id == 4:
        # For software-based services
        
        software = q.software()
        
    print(product)
    
    if request.method == "POST":
        if product_id == 1:
            # For leather goods
            good = request.form.get("leather_product")
            leather_color = request.form.get("leather_color")
            metal_color = request.form.get("metal_color")
            size = request.form.get("size")
            
            print(good, leather_color, leather_color, metal_color, size)
    
    return render_template("product_page.html",
                           date=JGL_CURRENT_YEAR,
                           socials=JGL_SOCIALS,
                           product=product,
                           leather_options=leather_options,
                           leather_colors=leather_colors,
                           metal_colors=metal_colors,
                           sizes=sizes,
                           nonfiction=nonfiction,
                           fiction=fiction,
                           software=software)
    
@app.route("/cart", methods=["GET", "POST"])
def cart():
    """Shows the user's current cart"""
    
    return render_template("cart.html",
                           socials=JGL_SOCIALS,)