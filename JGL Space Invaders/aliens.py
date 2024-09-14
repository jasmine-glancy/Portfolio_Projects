"""The aliens for the python version of Space Invaders using Turtle!"""

import turtle
import time
import random

TINIER_MOVE_STEPS = 10

class JglMysteryShip(turtle.Turtle):
    """A special "mystery ship" occasionally moves 
    across the top of the screen"""
        
    def __init__(self) -> None:
        super().__init__()
        self.jgl_surprise_alien = turtle.Turtle()
        self.jgl_surprise_alien.color("BlueViolet")
        self.jgl_surprise_alien.shape("turtle")
        self.jgl_surprise_alien.pensize(2)
        self.jgl_surprise_alien.shapesize(stretch_wid=2, stretch_len=2)
        self.jgl_surprise_alien.penup()
        
        # Set the mystery ships's initial position to the far left
        self.jgl_surprise_alien.goto(500, 345)
        self.jgl_surprise_alien.setheading(180)

    def jgl_fly_mystery_ship(self):
        """Allows the mystery ship to fly across the screen"""
        
        self.jgl_surprise_alien.forward(TINIER_MOVE_STEPS)
            

# Create "aliens" 
class JglAlien(turtle.Turtle):

    def __init__(self, jgl_x_cor, jgl_y_cor, jgl_color) -> None:
        super().__init__()
        self.penup()
        self.shape("turtle")
        self.setheading(270)
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.color(jgl_color)
        self.goto(x=jgl_x_cor, y=jgl_y_cor)
    
class JglRowsOfAliens(turtle.Turtle):
    """Create rows of aliens that move together"""
    
    def __init__(self, screen) -> None:
        super().__init__()
        self.jgl_y_start = 100
        self.jgl_lower_increment = 50
        self.jgl_y_end = 350
        self.movement_speed = TINIER_MOVE_STEPS
        self.jgl_aliens_list = [] 
        self.jgl_alien_quantity = 0
        self.jgl_alien_laser_list = [] 
        self.jgl_colors = [
            "MidnightBlue",
            "Navy",
            "DarkBlue",
            "MediumBlue",
            "Blue"
        ]
        self.screen = screen
        self.jgl_create_all_rows()
        self.moving_left = True
        
    def jgl_create_row(self, jgl_y_cor, jgl_color) -> None:
        """Create a new row of aliens"""
        
        # Number of columns
        num_columns = 11
        
        # Calculate the step size based on the range and number of columns
        start_x = -325
        end_x = 325
        step_size = (end_x - start_x) // (num_columns - 1)
        
        for i in range(num_columns):
            x_cor = start_x + i * step_size
            
            # Builds a new brick in each row
            jgl_alien = JglAlien(x_cor, jgl_y_cor, jgl_color)  
            self.jgl_aliens_list.append(jgl_alien)
            
            print(f"Created alien at ({x_cor}, {jgl_y_cor})")
            
        self.jgl_alien_quantity = len(self.jgl_aliens_list)

        
            
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
                   
        print(f"Total Quantity: {self.jgl_alien_quantity}")
        print(f"Total Aliens Created: {len(self.jgl_aliens_list)}")
       
       
    def get_alien_quantity(self) -> int:
        """Return the current quantity of aliens"""
        return self.jgl_alien_quantity
     
    def jgl_lower_starting_position(self) -> None:
        """lowers the starting position of the aliens 
        after the first wave is defeated"""
        
        self.jgl_y_start -= self.jgl_lower_increment
        
        # Create a fresh set of rows
        self.jgl_create_all_rows()
        
    def jgl_move_aliens(self):
        """Moves aliens left or right as a 
        group based on the current direction"""
            
        if self.moving_left:
            self.jgl_move_aliens_left()
        else:
            self.jgl_move_aliens_right()
            
    def jgl_move_aliens_left(self) -> None:
        """Moves aliens left as a group"""
    
        
        if any(alien.xcor() - self.movement_speed < -425 for alien in self.jgl_aliens_list):
            """Starts moving aliens right if they 
            touch the wall"""
            self.moving_left = False
            self.jgl_move_aliens_down()
        else:
            for alien in self.jgl_aliens_list:
                jgl_new_x_pos = alien.xcor() - self.movement_speed
                alien.goto(jgl_new_x_pos, alien.ycor())
            
    def jgl_move_aliens_right(self) -> None:
        """Moves aliens right as a group"""
        
        if any(alien.xcor() + self.movement_speed > 425 for alien in self.jgl_aliens_list):
            """Starts moving aliens left if they 
            touch the wall"""
            self.moving_left = True
            self.jgl_move_aliens_down()
        else:
            for alien in self.jgl_aliens_list:
                jgl_new_x_pos = alien.xcor() + self.movement_speed
                alien.goto(jgl_new_x_pos, alien.ycor())
    
    def jgl_move_aliens_down(self) -> None:    
        """Aliens move downward toward the shooter 
        each time they touch the edge of the screen"""
    
        for alien in self.jgl_aliens_list:
            jgl_new_y_pos = alien.ycor() - 25
            alien.goto(alien.xcor(), jgl_new_y_pos)
            
    def jgl_alien_lasers(self) -> None:     
        """Aliens fire projectiles toward the player at random"""
        
        # Select a random alien from self.jgl_aliens
        jgl_chosen_alien = random.choice(self.jgl_aliens_list)
        
        # Create a new turtle.Turtle instance for the projectile
        jgl_alien_laser = turtle.Turtle()
        jgl_alien_laser.color("white")
        jgl_alien_laser.shape("circle")
        jgl_alien_laser.pensize(2)
        jgl_alien_laser.shapesize(stretch_len=0.5, stretch_wid=0.5)
        jgl_alien_laser.penup()
        
        # Set the projectile's initial position to the selected alien's position
        jgl_alien_laser.goto(jgl_chosen_alien.xcor(), jgl_chosen_alien.ycor() - 50)
        jgl_alien_laser.setheading(270)
        
        # Add the laser to the list of alien lasers
        self.jgl_alien_laser_list.append(jgl_alien_laser)
        
        # Initialize distance traveled
        jgl_alien_laser_distance = 0
        
        # Distance to move in each step
        jgl_alien_laser_step = 10 
        
        def jgl_move_alien_laser():
            nonlocal jgl_alien_laser_distance
            
            if jgl_alien_laser.ycor() > -300:
                # Moves the projectile downward
                jgl_alien_laser.forward(jgl_alien_laser_step)
                jgl_alien_laser_distance += jgl_alien_laser_step
                
                # Schedule next step after 20ms
                turtle.ontimer(jgl_move_alien_laser, 20)
            else:
                jgl_alien_laser.hideturtle()
                jgl_alien_laser.clear()    
                self.jgl_alien_laser_list.remove(jgl_alien_laser)
            
        jgl_move_alien_laser()
        
    def jgl_get_alien_borders(self) -> dict:
        """Gets the borders of each alien"""
        
        alien_borders = {}
        
        for index, alien in enumerate(self.jgl_aliens_list):
            alien_x = alien.xcor()
            alien_y = alien.ycor()
            
            stretch_height, stretch_len = alien.shapesize()[0], alien.shapesize()[1]
            
            # Default turtle width and height are 20 pixels
            width = stretch_len * 20
            height = stretch_height * 20
            
            alien_borders[index] = {
                "x_range": (alien_x - width / 2, alien_x + width / 2),
                "y_range": (alien_y - height / 2, alien_y + height / 2)
            }
            
        return alien_borders
        
    def jgl_increase_alien_speed(self) -> None:
        """Aliens move a little faster with each one that is hit"""
        
        self.movement_speed *= 0.95
        
    def jgl_stop_movement(self) -> None:
        """Stops the aliens moving if the game is over"""
        
        self.movement_speed = 0
        
        