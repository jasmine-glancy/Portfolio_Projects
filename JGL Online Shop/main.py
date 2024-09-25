"""
An online shop using Flask and Python
"""

from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
import helpers as h
from online_shop import Users, SHOP_SESSION
import os
import queries as q
from werkzeug.security import check_password_hash, generate_password_hash


# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

# Load in security key
app.secret_key = os.environ.get("security_key")


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
        if "add_to_cart" in request.form:
            if product_id == 1:
                # For leather goods
                good = request.form.get("leather_product")
                leather_color = request.form.get("leather_color")
                metal_color = request.form.get("metal_color")
                size = request.form.get("size")
                
                print(good, leather_color, leather_color, metal_color, size)
            elif product_id == 2 or product_id == 3:
                # For written services
                written_product = request.form.get("writing_options")
                
            elif product_id == 4:
                # For software-based services   
                software_id = request.form.get("software_options") 
        
            # TODO: If there is a shopping session, reference it
            
                # TODO: Add shopping_session created_at
            # TODO: If there isn't a shopping session already, create one
            
            # TODO: Add options to the cart
             
        elif "send_message" in request.form:
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")
            
            # TODO: Make contact work
   
        
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
    
    # TODO: Query database for the user's cart
    # TODO: Add shopping cart total

        # TODO: Query database for prices
        
        # TODO: Add final total of the cart to shopping_session table

    # TODO: If user hits checkout
    
        # TODO: Create a new order_items entry
            # TODO: All items from the same order should be accounted for
            
        # TODO: Create a new order_details entry
        
        # TODO: log payment details
        
        # TODO: Go to successfull checkout page
    return render_template("cart.html",
                           socials=JGL_SOCIALS)
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user"""

    # Store socials in session
    session['socials'] = JGL_SOCIALS
    
    if request.method == "POST":
        
        try:
            # Check user against info in the database
            find_user = q.find_user(request.form.get("username"))
            find_email = q.find_email(request.form.get("email"))
            
            # Check if username exists already in the database
            if find_user is not None:
                flash("That username is already taken.")
                return redirect(url_for("register"))

            # Check if the user's password matches the password verification
            elif request.form.get("password") != request.form.get("confirm_password"):
                flash("Passwords must match.")
                return redirect(url_for("register"))

            # Check if the email address is in the database
            elif find_email is not None:
                flash("That email address is already in use.")
                return redirect(url_for("register"))

            # If all checks pass, hash password
            hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        except Exception as e:
            flash(f"Can't register new user, exception: {e}")
            return redirect(url_for("register"))
        else:
            print("success!")
            username = request.form.get("username")
            email = request.form.get("email")
            print(username, email)
            
            # Insert data if all checks pass
            try:
                # Insert new info into database
                new_user = Users(
                    username=username,
                    password=hashed_password,
                    email=email,
                    created_at=datetime.now(),
                    modified_at=datetime.now()
                )
            
                print(new_user.username,
                      new_user.password,
                      new_user.email,
                      new_user.created_at,
                      new_user.modified_at)
                
                SHOP_SESSION.add(new_user)
                SHOP_SESSION.commit()
                
                session["username"] = new_user.username

            except Exception as e:
                SHOP_SESSION.rollback()
                
                flash(f"Can't insert new user into database, exception: {e}")
                return redirect(url_for("register"))
                
            try:
                # Get the user id and save it to the session
                look_up_id = q.find_user_id(username)
                
                if look_up_id is not None:
                    print(look_up_id["user_id"])
                    
                    # Remember which user has logged in
                    session["user_id"] = look_up_id["user_id"]
                                        
            except Exception as e:
                print("Can't find user ID")
                
            # Redirect to home
            return redirect(url_for("home"))

    return render_template("register.html",
                           socials=JGL_SOCIALS)
    
@app.route("/logout")
def logout():
    """Logs user out"""
    
    # Clears the user_id
    session.clear()
    
    # Redirect to home
    return redirect(url_for("home", socials=JGL_SOCIALS))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs an existing user in"""
        
    # Checks if the user's data is validated 
    if request.method == "POST":

        # Check username and hashed password against the database
        try:
            user_lookup = q.find_user(request.form.get("username"))
            
            if user_lookup == None:
                flash("Username not found.")
                return redirect(url_for("login"))
        
            # Ensure username exists and password is correct
            elif not check_password_hash(user_lookup.password, 
                                    request.form.get("password")):
                flash("Invalid password.")
                return redirect(url_for("login"))
            
            else:
                flash(f"Logged in as {request.form.get("username")}!")
                
                # Remember which user has logged in
                session["user_id"] = user_lookup.user_id
                session["username"] = user_lookup.username
                
                print(session["user_id"], session["username"])
                return redirect(url_for("home"))
        except Exception as e:
            flash(f"Can't log in. Exception: {e}")
            return redirect(url_for("login"))
     
    return render_template("login.html", socials=JGL_SOCIALS)