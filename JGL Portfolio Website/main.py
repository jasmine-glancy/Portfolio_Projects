from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import requests


# Configure application
app = Flask(__name__)

# Add in Bootstrap
Bootstrap5(app)

@app.route("/")
def home():
    return render_template("index.html")
