""" 
Automates the Google Dinosaur Game!
"""

import gamePlay as gp
import keyboard
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

gamePlay = gp.gamePlay()

game_on = True


while game_on:
    if keyboard.is_pressed("x"):
        game_on = False
        
    # Set up the screen
    gamePlay.screen_setup()


