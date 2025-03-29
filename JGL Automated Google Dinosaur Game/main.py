""" 
Automates the Google Dinosaur Game!
"""

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

# Use PyAutoGUI to control the mouse/keyboard

pag.PAUSE = 1

# Start the game
pag.keyDown("space")
pag.keyUp("space")



# TODO: Use Pillow to process the pictures to jump over

# TODO: When a pterodactyl or cactus is within range, the t-rex jumps

# TODO: When the t-rex hits the cactus, the game ends

# TODO: Keep track of score

    # TODO: Each milisecond should add 1 to the score
    
