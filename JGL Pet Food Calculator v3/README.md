# PET FOOD CALCULATOR

#### Video Demo: <URL HERE>

#### Description:

Welcome to the Pet Food Calculator! This is a Flask web application that allows you to input your pet's information and get recommended feeding amounts. In addition, it will even instruct you how much to feed if you are transitioning your dog or cat to a different diet!

When changing your pet from one food to another, it is important to do a slow transition over 5-14 days (the actual time depends on how sensitive your pet's stomach is, though generally, the transition period is 5-7 days).

### File Description:

## base.html

This file is a static HTML file that loads common items across all pages. These items include:

- Bootstrap CSS
- Stylesheet
- Google fonts
- Favicon
- Header image
- Navigation bar (Bootstrap)

## get_signalment.html

This file is a static HTML file that features:

- A progress bar indicating step 1/5
- Flask WTF forms for asking for user input about patient signalment (name, age, sex, reproductive status, species, breed).
- JavaScript that dynamically shows Flask WTF form features depending on:
  - Whether or not the pet is an intact female
- whether or not the pet is pregnant or nursing
