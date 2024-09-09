"""The aliens for the python version of Space Invaders using Turtle!"""

from turtle import Turtle


# Create "aliens" 
class JglAlien(Turtle):

    def __init__(self, jgl_x_cor, jgl_y_cor, jgl_color) -> None:
        super().__init__()
        self.penup()
        self.shape("turtle")
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.color(jgl_color)
        self.goto(x=jgl_x_cor, y=jgl_y_cor)
    
class JglRowsOfAliens(Turtle):
    """Create rows of aliens that move together"""
    
    def __init__(self) -> None:
        super().__init__()
        self.jgl_y_start = 150
        self.jgl_y_end = 350
        self.jgl_aliens = [] 
        self.jgl_colors = [
            "MidnightBlue",
            "Navy",
            "DarkBlue",
            "MediumBlue",
            "Blue"
        ]
        self.jgl_create_all_rows()
        
    def jgl_create_row(self, jgl_y_cor, jgl_color) -> None:
        """Create a new row of aliens"""
        
        for i in range(-325, 375, 65):
            # Builds a new brick in each row
            jgl_alien = JglAlien(i, jgl_y_cor, jgl_color)  
            self.jgl_aliens.append(jgl_alien)
            
    def jgl_create_all_rows(self) -> None:
        """Creates all rows"""
        
        jgl_row_height = 40
        
        # Create 5 rows of 11 "aliens"
        jgl_number_of_rows = 5
        
        for i in range(jgl_number_of_rows):
            jgl_y_cor = self.jgl_y_start + i * jgl_row_height
            
            # Assigns color by row number
            jgl_color = self.jgl_colors[i % len(self.jgl_colors)]
            self.jgl_create_row(jgl_y_cor, jgl_color)
        

    
    # TODO: Aliens move left and right as a group
    
    # TODO: Aliens move downward toward the shooter each time they touch the 
    # # edge of the screen
    
    # TODO: Aliens fire projectiles toward the player
    
    # TODO: A special "mystery ship" occasionally moves across the top of the screen
        # TODO: This ship rewards bonus points if hit
    
