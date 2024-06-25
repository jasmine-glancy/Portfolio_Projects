"""Creates walls to break for the game Breakout"""

from turtle import Turtle
import random

# TODO: Create a bank of x and y positions

# Create Walls class with Turtle
class jglBrick(Turtle):
    
    def __init__(self, jgl_x_cor, jgl_y_cor, jgl_color):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.color(jgl_color)
        self.goto(x=jgl_x_cor, y=jgl_y_cor)
           
    # TODO: init should load the blocks with the colors and positions
    # TODO: Randomly generate vs stagnant positions?

    def jgl_colors(self) -> str:
        """Randomly generates a color for coloring the blocks"""
        
        # TODO: Create a bank of colors
        jgl_colors = ["red",
                      "orange",
                      "OrangeRed",
                      "yellow",
                      "YellowGreen",
                      "SpringGreen",
                      "green",
                      "blue",
                      "DarkSlateBlue",
                      "purple4"]
        
        return random.choice(jgl_colors)

    # TODO: Create bust function that destroys the blocks
    
class jglWalls(Turtle):
    """Creats walls with the bricks, suggested by 
    https://www.geeksforgeeks.org/create-breakout-game-using-python/"""
    
    def __init__(self):
        self.jgl_y_start = 10
        self.jgl_y_end = 350
        self.jgl_bricks = []
        self.jgl_colors = ["red",
                      "OrangeRed",
                      "orange",
                      "yellow",
                      "YellowGreen",
                      "green",
                      "blue",
                      "DarkSlateBlue",
                      "purple4"]
        self.jgl_create_all_rows()
        
    def jgl_create_row(self, jgl_y_cor, jgl_color):
        for i in range(-325, 375, 65):
            # Builds a new brick in each position of the late
            jgl_brick = jglBrick(i, jgl_y_cor, jgl_color)  
            self.jgl_bricks.append(jgl_brick)
        
    def jgl_create_all_rows(self):
        jgl_row_height = 35
        jgl_number_of_rows = (self.jgl_y_end - self.jgl_y_start) // jgl_row_height
        for i in range(jgl_number_of_rows):
            jgl_y_cor = self.jgl_y_start + i * jgl_row_height
            jgl_color = self.jgl_colors[i % len(self.jgl_colors)]
            self.jgl_create_row(jgl_y_cor, jgl_color)