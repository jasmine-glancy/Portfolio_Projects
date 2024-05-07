# PET FOOD CALCULATOR

#### Video Demo: <URL HERE>

#### Description:

Welcome to the Pet Food Calculator! This is a Flask web application that allows you to input your pet's information and get recommended feeding amounts. In addition, it will even instruct you how much to feed if you are transitioning your dog or cat to a different diet!

When changing your pet from one food to another, it is important to do a slow transition over 5-14 days (the actual time depends on how sensitive your pet's stomach is, though generally, the transition period is 5-7 days).

### File Description:

#### main.py 

Contains all of the routes and Python code for the website. Imports:

- werkzeug.security for password hashing/hash generating
- CS50's SQL
- Flask's functions (Flask, render_template, redirect, url_for, request, flash)
  - Flash for error messages, which are passed to the applicable HTML pages below.
- os for retrieving environmental variables
- forms from forms.py

Features the following routes:

- Index
  - Includes a welcome message, disclaimers, and login/registration/use as guest buttons via index.html
    - If the user is logged in, these buttons change to "Calculate for an Existing Pet" and "Calculate for a New Pet"
- Login
  - Allows an existing user to log in with a Flask form (LoginForm) via login.html
  - Use SQL queries to search the "users" table in pet_food_calculator.db for existing users
  - Provides error messages via Flash when a user is not found or if the password is invalid
  - If login is successful, redirects to index
- Register
  - Allows an existing user to register with a Flask form (RegisterForm) via register.html
  - Use SQL queries to search the "users" table in pet_food_calculator.db for existing users before allowing a user to register with a username
  - Provides error messages via Flash when a username is taken or if the chosen password doesn't match the password confirmation
  - Inserts the new user into the "users" table of pet_food_calculator.db
  - If registration is successful, redirects to index
- Get-signalment
  - Loads 2 Flask forms via get_signalment.html:
    - NewSignalment and RepoStatus
    - Shows different questions in RepoStatus based on different conditions via JavaScript
  - Includes a button that takes you to the "get-weight" page
- Get-weight
  - Loads in a Flask WTF form (GetWeight) that asks for the pet's weight and body condition score via get_weight_and_bcs.html
  
#### forms.py

Contains all the Flask WTF Form Classes for:

- NewSignalment asks for the pet's signalment (Name, age, sex, reproductive status, species, breed)
- GetWeight asks for the pet's body condition score, patient weight, and the unit of the weight (in pounds or kilograms)
- ReproStatus asks for pregnancy, nursing, and litter size information based on what the user inputs for their pet information
  - Pregnancy questions only show up if the pet is an intact female
  - If the pet is pregnant and canine, ask how many weeks along she is
  - If the pet is not pregnant and is an intact female, ask if she is nursing a litter
  - If the pet is nursing a litter, ask for the litter size
  - If the pet is nursing and feline, ask how many weeks she has been lactating
- LoginForm asks for username and password and provides a submit button
- RegisterForm asks for a username, password, and for the user to confirm a password. Also provides a submit button
- WorkForm asks for the pet's activity level per day in both minutes and hours.

#### base.html

This file is a static HTML file that loads common items across all pages. These items include:

- Bootstrap CSS
- Stylesheet
- Google fonts
- Favicon
- Header image
- Navigation bar (Bootstrap)

#### get_signalment.html

This file is a static HTML file that features:

- A progress bar indicating step 1/5
- Flask WTF form for asking for user input about patient signalment (name, age, sex, reproductive status, species, breed)
- JavaScript that dynamically shows Flask WTF form features depending on:
  - Whether or not the pet is an intact female
- Whether or not the pet is pregnant or nursing

#### get_weight_and_bcs.html

This file is a static HTML file that features:

- A progress bar indicating step 2/5
- Information about body condition scores and their importance
- Accordion dropdown from Bootstrap that shows canine or feline body condition scores depending on species
- Flask WTF form for asking for user input about patient weight and body condition score
- Buttons that return the user to get_signalment and get_work_level

#### get_work_level.html

This file is a static HTML file that features:

- A progress bar indicating step 3/5
- Flask WTF form for asking for user input about how much activity their pet gets per day
- Buttons that return the user to get_weight_and_bcs and current_food