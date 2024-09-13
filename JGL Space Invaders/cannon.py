"""The cannon for the python version of Space Invaders using Turtle!"""

import time
import turtle

MOVE_STEPS = 20

class JglCannon(turtle.Turtle):
    """Creates the cannon and allows it to move"""
    
    def __init__(self) -> None:
        """Creates the laser cannon"""
        
        super().__init__()
        self.penup()
        self.goto((0, -300))
        self.shape("square")
        self.color("lime")
        self.shapesize(stretch_len=4, stretch_wid=2)
        self.penup()
        
        self.cannon_top = turtle.Turtle()
        self.cannon_top.penup()
        self.cannon_top.goto((0, -275))
        self.cannon_top.shape("square")
        self.cannon_top.color("lime")
        self.cannon_top.shapesize(stretch_len=1.5, stretch_wid=2)
        
        self.lasers = []
        
    def jgl_cannon_top(self) -> float:
        """Gets the top border of the cannon"""
        
        cannon_gun_height = self.shapesize()[1] * 20
        
        top_border = self.cannon_top.ycor() + cannon_gun_height 
        
        return top_border

    def jgl_move_cannon_left(self) -> None:
        jgl_new_x_pos = self.xcor() - MOVE_STEPS
        
        if jgl_new_x_pos < -425:
            """Bounces the cannon back if too far to the left"""
            jgl_new_x_pos = -425
            
        self.goto(jgl_new_x_pos, self.ycor())        
        self.cannon_top.goto(jgl_new_x_pos, self.cannon_top.ycor()) 

        
    def jgl_move_cannon_right(self) -> None:
        jgl_new_x_pos = self.xcor() + MOVE_STEPS
        
        if jgl_new_x_pos > 425:
            """Bounces the cannon back if too far to the right"""
            jgl_new_x_pos = 425
            
        self.goto(jgl_new_x_pos, self.ycor())
        self.cannon_top.goto(jgl_new_x_pos, self.cannon_top.ycor())
    
    def jgl_shoot_cannon(self) -> None:
        # Enable laser to shoot out of the cannon when space bar is pressed

        laser = turtle.Turtle()
        laser.color("yellow")
        laser.pensize(2)
        laser.penup()
        laser.goto(self.xcor(), self.ycor() + 50)
        laser.setheading(90)
        self.lasers.append(laser) 
        self.jgl_move_laser(laser)
        
    
    # Creates a new laser instance and manages it independently
    # # Suggested by CoPilot
    def jgl_move_laser(self, laser):
        
        # Distance to move in each step
        laser_step = 10 
        
        # Total distance to move
        laser_max_distance = 675  
        
        def move():
            if laser.ycor() < laser_max_distance:
                laser.forward(laser_step)
                
                # Schedule next step after 20ms
                turtle.ontimer(move, 20)  
            else:
                # Remove the line after a short delay
                self.clear_laser(laser)
        
        move() 
        
    def clear_laser(self, laser):
        if laser in self.lasers:
            laser.clear()
            laser.hideturtle()
            self.lasers.remove(laser)
        else:
            print("Laser is not in the list.")
        