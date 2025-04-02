from PIL import Image, ImageGrab


class processImage():

    def __init__(self):
        pass
    
    def screen_setup(self):
        self.image = ImageGrab.grab().convert("L")
        self.image_data = self.image.load()
            
    def find_cactus(self):
        """Search the area in front of the t-rex for cacti"""
        
        for i in range(530, 610):
            for j in range(130, 160):
                self.image_data[i, j] = 0

        self.image.show()
        
    def find_birds(self):
        """Search the sky for pterodactyl"""
        for i in range(530, 560):
            for j in range (100, 125):
                self.image_data[i, j] = 171
        
        

    # TODO: Use Pillow to process the pictures to jump over

    # TODO: When a pterodactyl or cactus is within range, the t-rex jumps

    # TODO: When the t-rex hits the cactus, the game ends