"""Creates walls to break for the game Breakout"""

from turtle import Turtle

# Create Walls class with Turtle
class jglBrick(Turtle):
    
    def __init__(self, jgl_x_cor, jgl_y_cor, jgl_color):
        super().__init__()
        self.penup()
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.color(jgl_color)
        self.goto(x=jgl_x_cor, y=jgl_y_cor)
    
    
class jglWalls(Turtle):
    """Creats walls with the bricks, suggested by 
    https://www.geeksforgeeks.org/create-breakout-game-using-python/"""
    
    def __init__(self) -> None:
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
        
    def jgl_create_row(self, jgl_y_cor, jgl_color) -> None:
        """Creates a new row of bricks"""
        for i in range(-325, 375, 65):
            # Builds a new brick in each row
            jgl_brick = jglBrick(i, jgl_y_cor, jgl_color)  
            self.jgl_bricks.append(jgl_brick)
            
            # Define the borders of the bricks
            self.jgl_left_wall = jgl_brick.xcor() - 30
            self.jgl_right_wall = jgl_brick.xcor() + 30
            self.jgl_upper_wall = jgl_brick.ycor() + 30
            self.jgl_lower_wall = jgl_brick.ycor() - 30

        
    def jgl_create_all_rows(self) -> None:
        """Creates all rows, code suggested by CoPilot"""
        
        jgl_row_height = 35
        jgl_number_of_rows = (self.jgl_y_end - self.jgl_y_start) // jgl_row_height
        for i in range(jgl_number_of_rows):
            jgl_y_cor = self.jgl_y_start + i * jgl_row_height
            
            # Assigns color by row number
            jgl_color = self.jgl_colors[i % len(self.jgl_colors)]
            self.jgl_create_row(jgl_y_cor, jgl_color)
        
        self.jgl_quantity = len(self.jgl_bricks)
            
