"""Creates walls to break for the game Breakout"""

from turtle import Turtle
import random

# TODO: Create a bank of x and y positions

# Create Walls class with Turtle
class jglBrick(Turtle):
    
    def __init__(self, jgl_x_cor, jgl_y_cor):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.color(self.jgl_colors())
        self.goto(x=jgl_x_cor, y=jgl_y_cor)
           
    # TODO: init should load the blocks with the colors and positions
    # TODO: Randomly generate vs stagnant positions?

    def jgl_colors(self) -> str:
        """Randomly generates a color for coloring the blocks"""
        
        # TODO: Create a bank of colors
        jgl_colors = ["red",
                      "orange",
                      "yellow",
                      "YellowGreen",
                      "green",
                      "blue",
                      "purple4"]
        
        return random.choice(jgl_colors)

    # TODO: Create bust function that destroys the blocks
    
class jglWalls(Turtle):
    """Creats walls with the bricks, suggested by 
    https://www.geeksforgeeks.org/create-breakout-game-using-python/"""
    
    def __init__(self):
        self.jgl_y_start = 0
        self.jgl_y_end = 350
        self.jgl_bricks = []
        self.jgl_create_all_rows()
        
    def jgl_create_row(self, jgl_y_cor):
        for i in range(-375, 375, 65):
            # Builds a new brick in each position of the late
            jgl_brick = jglBrick(i, jgl_y_cor)  
            self.jgl_bricks.append(jgl_brick)
        
    def jgl_create_all_rows(self):
        for i in range(self.jgl_y_start, self.jgl_y_end, 33):
            self.jgl_create_row(i)