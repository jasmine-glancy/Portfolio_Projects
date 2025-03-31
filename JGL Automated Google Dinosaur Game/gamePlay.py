import imageProcessing as ip
import time
import pyautogui as pag

class gamePlay():
    def __init__(self):
        pass
    
    def screen_setup(self):
        screen_x, screen_y = 0, 102

        # Get screen width
        screen_width, screen_height =  1920, 872

        # Get a "screen shot"
        window_img = pag.screenshot(region=(screen_x, screen_y, screen_width, screen_height))
        window_img.save("dinosaur_game.jpg")

        print(window_img)
        time.sleep(1)

        # Set the background color to check for objects
        bg_color = ip.grab_pixel(window_img, 100, 100)
        print(bg_color)
        time.sleep(1)
        
    def start_game(self):

        # Use PyAutoGUI to control the keyboard
        pag.PAUSE = 3

        # Start the game
        pag.keyDown("space")
        pag.keyUp("space")
        
        

# TODO: Allow the t-rex to jump over obstacles

# TODO: Keep track of score

    # TODO: Each milisecond should add 1 to the score
    