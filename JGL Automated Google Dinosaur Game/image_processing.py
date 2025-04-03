import game_play as gp 
from PIL import ImageGrab

play = gp.gamePlay()


class processImage():

    def __init__(self):
        pass
    
    def screen_setup(self):
        image = ImageGrab.grab().convert("L")
        self.image_data = image.load()
            
    def find_cactus(self):
        """Search the area in front of the t-rex for cacti"""
        
        for i in range(300, 415):
            for j in range(563, 650):
                self.image_data[i, j] <  100 
                play.jump()
            
        
    def find_birds(self):
        """Search the sky for pterodactyl"""
        for i in range(300, 415):
            for j in range (410, 563):
                self.image_data[i, j] < 171
                play.jump()
