""" 
Automates the Google Dinosaur Game!
"""

import imageProcessing as ip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui as pag
import time

DINO_GAME_URL = "https://elgoog.im/dinosaur-game/"

# Set up Selenium

options = Options()

options.add_experimental_option("detach", True)
options.add_argument("--incognito")

driver = webdriver.Chrome(options=options)

# Open the game

driver.get(DINO_GAME_URL)

time.sleep(3)

driver.maximize_window()
time.sleep(1)

dino_x, dino_y = 0, 102

# Get screen width
screen_width, screen_height =  1920, 872

# Get the image for the t-rex
dinosaur_img = pag.screenshot(region=(dino_x, dino_y, screen_width,screen_height))
dinosaur_img.save("t-rex.jpg")

print(dinosaur_img)
time.sleep(1)

# Set the background color to check for objects
bg_color = ip.grab_pixel(dinosaur_img, 100, 100)
print(bg_color)
time.sleep(1)

# Use PyAutoGUI to control the keyboard

# pag.PAUSE = 8

# # Start the game
# pag.keyDown("space")
# pag.keyUp("space")

# TODO: Allow the t-rex to jump over obstacles

# TODO: Keep track of score

    # TODO: Each milisecond should add 1 to the score
    
