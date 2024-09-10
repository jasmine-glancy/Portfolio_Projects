"""The aliens for the python version of Space Invaders using Turtle!"""

from turtle import Turtle

TINIER_MOVE_STEPS = 10

# Create "aliens" 
class JglAlien(Turtle):

    def __init__(self, jgl_x_cor, jgl_y_cor, jgl_color) -> None:
        super().__init__()
        self.penup()
        self.shape("turtle")
        self.setheading(270)
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.color(jgl_color)
        self.goto(x=jgl_x_cor, y=jgl_y_cor)
    
class JglRowsOfAliens(Turtle):
    """Create rows of aliens that move together"""
    
    def __init__(self) -> None:
        super().__init__()
        self.jgl_y_start = 100
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
        
        jgl_row_height = 50
        
        # Create 5 rows of 11 "aliens"
        jgl_number_of_rows = 5
        
        for i in range(jgl_number_of_rows):
            jgl_y_cor = self.jgl_y_start + i * jgl_row_height
            
            # Assigns color by row number
            jgl_color = self.jgl_colors[i % len(self.jgl_colors)]
            self.jgl_create_row(jgl_y_cor, jgl_color)
        
    def jgl_move_aliens(self):
        """Moves aliens left or right as a 
        group based on the current direction"""
        
        try:
            
            if self.moving_left:
                self.jgl_move_aliens_left()
            else:
                self.jgl_move_aliens_right()
                
        except AttributeError:
            self.jgl_move_aliens_left()
            
    def jgl_move_aliens_left(self):
        """Moves aliens left as a group"""
        
        for alien in self.jgl_aliens:
            jgl_new_x_pos = alien.xcor() - TINIER_MOVE_STEPS
            alien.goto(jgl_new_x_pos, alien.ycor())
            
        if any(alien.xcor() < -425 for alien in self.jgl_aliens):
            """Starts moving aliens right if they 
            touch the wall"""
            self.moving_left = False
            self.jgl_move_aliens_down()
            
    def jgl_move_aliens_right(self):
        """Moves aliens right as a group"""
        
        for alien in self.jgl_aliens:
            jgl_new_x_pos = alien.xcor() + TINIER_MOVE_STEPS
            alien.goto(jgl_new_x_pos, alien.ycor())
        
        # Check if any alien has touched the right wall
        if any(alien.xcor() > 425 for alien in self.jgl_aliens):
            """Starts moving aliens left if they 
            touch the wall"""
            self.moving_left = True
            self.jgl_move_aliens_down()
    
    def jgl_move_aliens_down(self):    
        """Aliens move downward toward the shooter 
        each time they touch the edge of the screen"""
    
        for alien in self.jgl_aliens:
            jgl_new_y_pos = alien.ycor() - TINIER_MOVE_STEPS
            alien.goto(alien.xcor(), jgl_new_y_pos)
            
            
    # TODO: Aliens fire projectiles toward the player
    
    # TODO: A special "mystery ship" occasionally moves across the top of the screen
        # TODO: This ship rewards bonus points if hit
    
