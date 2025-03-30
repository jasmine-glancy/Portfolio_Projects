from PIL import Image, ImageGrab

def grab_pixel(img, x, y):
    """Function recommeneded by GeeksForGeeks"""
    
    image = img.load()
    
    return image[x, y]


# TODO: Use Pillow to process the pictures to jump over

# TODO: When a pterodactyl or cactus is within range, the t-rex jumps

# TODO: When the t-rex hits the cactus, the game ends