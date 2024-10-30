from datetime import datetime
from flask import Blueprint, flash, render_template, session, \
    redirect, request, url_for
from online_shop import CartItems, Users, SHOP_SESSION, SavedItems, ShoppingSessions
import queries as q
import helpers as h
from werkzeug.security import check_password_hash, generate_password_hash



bp = Blueprint("main", __name__)

JGL_CURRENT_YEAR = h.current_year()
JGL_SOCIALS = h.social_links()


# ----------------------- Routes ----------------------- #

@bp.route("/", methods=["GET", "POST"])
def home():
    """Shows homepage with a current copyright date"""
    
    # Convert current date to a string
    jgl_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Grab only the year
    jgl_current_year = jgl_date_str[:4]
    return render_template("index.html",
                           date=jgl_current_year,
                           socials=JGL_SOCIALS)

@bp.route("/products", methods=["GET", "POST"])
def products():
    """Showcases a list of products and services to buy"""
    
    products_services = q.find_product_list()
    print(products_services)
    
    return render_template("products.html", 
                           date=JGL_CURRENT_YEAR,
                           socials=JGL_SOCIALS,
                           products_services=products_services)

@bp.route("/products/<int:product_id>", methods=["GET", "POST"])
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
    
    if product:
        id = product.service_product_id
        print(f"ID: {id}")
        
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
        print("posted")
        if "add_to_cart" in request.form:
            
            try: 
                
                item_quantity = int(request.form.get("quantity"))
                
                print(item_quantity, type(item_quantity))
            except ValueError:
                flash("Please enter a quantity between 1 and 10.", "selection_error")
                return redirect(url_for("main.for_sale_info", product_id=product_id))
            
            print("Add to Cart button clicked")
            
            # Calculate price
            price = q.find_product_price(id)
            
            print(f"Item Price: {price} type: {type(price)}")
            
            order_notes = None 
            
            # If there is a shopping session, reference it
            if "shopping_session" in session and session.get("shopping_session"):
                print("Shopping session found!")
                
                if session.get("user_id") and price:
                    # Find existing shopping session total
                    shopping_session = q.shopping_session_search(session["shopping_session"])
                    session_total = shopping_session.total
                    
                    # Modify price by quantity
                    item_price = price * item_quantity
                    print(f"Item Price {item_price}")
                    
                    # Update the total
                    new_price = session_total + item_price
                    shopping_session.total = new_price
                    shopping_session.modified_at = datetime.now()
                    
                    order_notes = request.form.get("order_notes")
            
                    try:
                        print(f"Updated total: {new_price} type: {type(new_price)}")
                        SHOP_SESSION.commit()
                        
                    except Exception as e:
                        SHOP_SESSION.rollback()
                        flash(f"Unable to update shopping session. Exception: {e}")
                        return redirect(url_for("main.for_sale_info", product_id=product_id))
            else:
                
                # If there isn't a shopping session already, create one if the user is logged in
                if session.get("user_id") and price:
                    
                    try:
                        new_shopping_session = ShoppingSessions(
                            user_id=session["user_id"],
                            total=price,
                            created_at=datetime.now(),
                            modified_at=datetime.now()
                        )
                        
                        print(new_shopping_session.session_id,
                            new_shopping_session.total,
                            new_shopping_session.user_id)
                        
                        SHOP_SESSION.add(new_shopping_session)
                        SHOP_SESSION.commit()
                        
                        # Update the shopping session
                        session["shopping_session"] = new_shopping_session.session_id
                        
                        print(f"Shopping session: {session["shopping_session"]}")
                        
                    except Exception as e:
                        SHOP_SESSION.rollback()
                        
                        flash(f"Unable to add shopping session. Exception: {e}", "selection_error")
                    
                        return redirect(url_for("main.for_sale_info", product_id=product_id))
                else:
                    flash("Please log in to add items to your cart.")
                    
                    return redirect(url_for("main.login"))

            # Add options to the cart
            new_cart_item = CartItems(
                session_id=session["shopping_session"],
                product_id=id,
                quantity=item_quantity,
                created_at=datetime.now(),
                modified_at=datetime.now(),
                product_order_notes=order_notes
            )        
            
            if id == 1:
                # For leather goods
                good = request.form.get("leather_product")
                leather_color = request.form.get("leather_color")
                metal_color = request.form.get("metal_color")
                size = request.form.get("size")
                
                if good == "default" or leather_color == "default" \
                    or metal_color == "default" or size == "default":
                        flash("Please make a selection", "selection_error")

                print(f"Leather Product: {good}, Leather Color: {leather_color}, Metal Color: {metal_color}, Size: {size}")
                
                # Add options to the cart
                new_cart_item.leather_good_id = good
                new_cart_item.leather_color_id = leather_color
                new_cart_item.metal_color_id = metal_color
                new_cart_item.leather_goods_size_id = size
                
            elif id == 2 or id == 3:
                # For written services
                written_product = request.form.get("writing_options")
                print(f"Written Product: {written_product}")
                
                if written_product == "default":
                    flash("Please make a selection", "selection_error")
                    
                # Add options to the cart
                new_cart_item.writing_option_id = written_product
                
            elif id == 4:
                # For software-based services   
                software_id = request.form.get("software_options") 
        
                print(f"Software ID: {software_id}")
                
                if software_id == "default":
                    flash("Please make a selection", "selection_error")
                    
                # Add options to the cart
                new_cart_item.software_id = software_id
            
            try:
                SHOP_SESSION.add(new_cart_item)
                SHOP_SESSION.commit()
                flash("Added to cart!", "successful_add")
                
            except Exception as e:
                SHOP_SESSION.rollback()
                flash(f"Unable to update cart. Exception: {e}", "selection_error")
                
            session["cart_contains_items"] = True
                
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
    
@bp.route("/cart", methods=["GET", "POST"])
def cart():
    """Shows the user's current cart"""
    
    
    cart_items = None
    saved_items = None
    
    if "shopping_session" in session and session["shopping_session"]:
        # Query database for the user's cart
        cart_items = q.find_cart(session["shopping_session"])
        
        # Query database for the user's saved items
        saved_items = q.find_all_saved_items(session["shopping_session"])
        
        saved_item_ids = [item.id for item in saved_items]
    
        return render_template("cart.html",
                        socials=JGL_SOCIALS,
                        cart_items=cart_items,
                        saved_items=saved_items,
                        saved_item_ids=saved_item_ids)
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
                           socials=JGL_SOCIALS,
                           cart_items=cart_items,
                           saved_items=saved_items)
    

@bp.route("/register", methods=["GET", "POST"])
def register():
    """Registers a new user"""

    # Store socials in session
    session["socials"] = JGL_SOCIALS
    
    if request.method == "POST":
        
        try:
            # Check user against info in the database
            find_user = q.find_user(request.form.get("username"))
            find_email = q.find_email(request.form.get("email"))
            
            # Check if username exists already in the database
            if find_user is not None:
                flash("That username is already taken.")
                return redirect(url_for("main.register"))

            # Check if the user's password matches the password verification
            elif request.form.get("password") != request.form.get("confirm_password"):
                flash("Passwords must match.")
                return redirect(url_for("main.register"))

            # Check if the email address is in the database
            elif find_email is not None:
                flash("That email address is already in use.")
                return redirect(url_for("main.register"))

            # If all checks pass, hash password
            hashed_password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        except Exception as e:
            flash(f"Can't register new user, exception: {e}")
            return redirect(url_for("main.register"))
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
                return redirect(url_for("main.register"))
                
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
            return redirect(url_for("main.home"))

    return render_template("register.html",
                           socials=JGL_SOCIALS)
    
@bp.route("/logout")
def logout():
    """Logs user out"""
    
    # Clears the session variables
    session.clear()
    
    # Redirect to home
    return redirect(url_for("main.home", socials=JGL_SOCIALS))

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Logs an existing user in"""
        
    # Checks if the user's data is validated 
    if request.method == "POST":

        # Check username and hashed password against the database
        try:
            user_lookup = q.find_user(request.form.get("username"))
            
            if user_lookup == None:
                flash("Username not found.")
                return redirect(url_for("main.login"))
        
            # Ensure username exists and password is correct
            elif not check_password_hash(user_lookup.password, 
                                    request.form.get("password")):
                flash("Invalid password.")
                return redirect(url_for("main.login"))
            
            else:
                flash(f"Logged in as {request.form.get("username")}!")
                
                # Remember which user has logged in
                session["user_id"] = user_lookup.user_id
                session["username"] = user_lookup.username
                
                print(session["user_id"], session["username"])
                return redirect(url_for("main.home"))
        except Exception as e:
            flash(f"Can't log in. Exception: {e}")
            return redirect(url_for("main.login"))
     
    return render_template("login.html", socials=JGL_SOCIALS)

@bp.route("/save", methods=["GET", "POST"])
def save_for_later():
    """Saves the item preferences so the user 
    can buy it later"""
    
    cart_item_id = request.args.get("cart_item_id")
    if cart_item_id:
        # Store the cart_item_id in the session
        session["cart_item_id"] = cart_item_id
    
        item = q.find_cart_item(cart_item_id)
        
        print(f"Item: {item.product_id} quantity: {item.quantity}")
        
        saved_item = q.find_saved_item(item.id)
        
        if saved_item is not None:
            # TODO: Add an additional quantity to the existing saved item
            pass
        else:
            print("Saved item not found")
            
            # If the saved item isn't already in the database add to SavedItems
            
            new_saved_item = SavedItems(
                id=item.id,
                session_id=item.session_id,
                product_id=item.product_id,
                quantity=item.quantity,
                created_at=item.created_at,
                modified_at=item.modified_at,
                leather_good_id=item.leather_good_id,
                leather_color_id=item.leather_color_id,
                metal_color_id=item.metal_color_id,
                leather_goods_size_id=item.leather_goods_size_id,
                writing_option_id=item.writing_option_id,
                software_id=item.software_id
            )
            
            try:
                SHOP_SESSION.add(new_saved_item)
                SHOP_SESSION.commit()
                print("Added saved item!")
                
            except Exception as e:
                SHOP_SESSION.rollback()
                print(f"Couldn't save the item, exception: {e}")
                
        # TODO: Adjust session price
        
        # Find the product ID of the cart item id
        cart_item = q.find_cart_item(cart_item_id)
        
        try:
            cart_item_product_id = cart_item.product_id
            print(f"Cart Item Product ID: {cart_item_product_id}")
            
            # Call the price by item ID
            item_price = q.find_product_price(cart_item_product_id)
            print(f"Item Price: {item_price}")
            
            # Find the current shopping session total
            shopping_session = q.shopping_session_search(session["shopping_session"])
            session_total = shopping_session.total
            
            # Change shopping session total
            # Update the total
            new_price = session_total - item_price
            shopping_session.total = new_price
            shopping_session.modified_at = datetime.now()
        except Exception as e:
            print(f"Unable to update session total. Exception: {e}")
            
        
    else:
        print("Unable to find cart item ID")
            
    return redirect(url_for("main.cart"))

@bp.route("/edit", methods=["GET", "POST"])
def edit():
    """Allows the user to edit their cart item"""
    
    cart_item_id = request.args.get("cart_item_id")
    
    print("editing!")
    
    return redirect(url_for("main.cart"))

@bp.route("/remove/<int:cart_item_id>", methods=["POST"])
def remove_cart_item(cart_item_id):
    """Deletes an item from the cart"""
    
    print("deleting!")
    
    return redirect(url_for("main.cart"))