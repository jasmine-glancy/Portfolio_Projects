from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import os, smtplib


# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap(app)

def jgl_send_email(jgl_contact_name, jgl_contact_email, jgl_message):
    """Uses the smtp module to send an email."""
    JGL_MAIL_ADDRESS = os.environ.get("JGL_SENDING_EMAIL")
    JGL_MAIL_APP_PASS = os.environ.get("JGL_PASSKEY")
    
    try:
        with smtplib.SMTP("smtp.gmail.com") as jgl_connection:
            jgl_connection.starttls()
            jgl_connection.login(user=JGL_MAIL_ADDRESS, password=JGL_MAIL_APP_PASS)
            jgl_connection.sendmail(
                from_addr=JGL_MAIL_ADDRESS,
                to_addrs=os.environ.get("JGL_PERSONAL_EMAIL"),
                msg=f"{jgl_contact_name} wants to contact you!\n\nFrom: {jgl_contact_email} \n\n{jgl_message}"
                )
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate with the SMTP server. Check your username and password.")
    except Exception as e:
        print(f"An error occurred: {e}.") 
    finally:
        jgl_connection.close()

@app.route("/")
def home():
    """Shows portfolio homepage with a current copyright date"""
    
    # Convert current date to a string
    jgl_date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Grab only the year
    jgl_current_year = jgl_date_str[:4]
    return render_template("index.html", date=jgl_current_year)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Makes the contact form work"""
    
    if request.method == "POST":
        jgl_contact_info = request.form
        
        # Uses the function to send the email with the contact form's information
        jgl_send_email(jgl_contact_info["name"], jgl_contact_info["email"], jgl_contact_info["message"])
    return redirect(url_for('home'))
    
