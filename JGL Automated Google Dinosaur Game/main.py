""" 
Automates the Google Dinosaur Game!
"""

import gamePlay as gp
import imageProcessing as ip


gamePlay = gp.gamePlay()
imageProcessing = ip.processImage()

game_on = True


while game_on:
    # Set up the screen
    imageProcessing.screen_setup()
    
    # Start the game
    gamePlay.start_game()
    imageProcessing.find_cactus()


