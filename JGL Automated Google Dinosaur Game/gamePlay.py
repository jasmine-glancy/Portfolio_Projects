import imageProcessing as ip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pyautogui as pag

DINO_GAME_URL = "https://elgoog.im/dinosaur-game/"

class gamePlay():
    def __init__(self):
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


    def start_game(self):

        # Use PyAutoGUI to control the keyboard
        pag.PAUSE = 3
        
        self.jump()

    def jump(self):
        # Start the game
        pag.keyDown("space")
        pag.keyUp("space")
 

# TODO: Allow the t-rex to jump over obstacles

# TODO: Keep track of score

    # TODO: Each milisecond should add 1 to the score
    