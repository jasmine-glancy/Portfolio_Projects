""" 
Automates the Google Dinosaur Game!
"""

import game_play as gp
import image_processing as ip

imageProcessing = ip.processImage()
gamePlay = gp.gamePlay()

game_on = True

# Start the game
gamePlay.add_driver()
gamePlay.start_game()
 
     
while game_on:  
    # Set up the screen
    imageProcessing.screen_setup()
    imageProcessing.find_cactus()
    imageProcessing.find_birds()


  