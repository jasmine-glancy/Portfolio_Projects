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

    def jgl_move_paddle_left(self) -> None:
        jgl_new_x_pos = self.xcor() - MOVE_STEPS
        
        if jgl_new_x_pos < -425:
            """Bounces the paddle back if too far to the left"""
            jgl_new_x_pos = -425
        self.goto(jgl_new_x_pos, self.ycor())        
        self.cannon_top.goto(jgl_new_x_pos, self.cannon_top.ycor()) 

        
    def jgl_move_paddle_right(self) -> None:
        jgl_new_x_pos = self.xcor() + MOVE_STEPS
        
        if jgl_new_x_pos > 425:
            """Bounces the paddle back if too far to the right"""
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

        
        # Initialize distance traveled
        laser_distance = 0  
        
        # Distance to move in each step
        laser_step = 1  
        
        # Total distance to move
        laser_max_distance = 675  

        def move_laser():
            nonlocal laser_distance
            if laser_distance < laser_max_distance:
                laser.forward(laser_step)
                laser_distance += laser_step
                
                # Schedule next step after 5ms
                turtle.ontimer(move_laser, 5)  
            else:
                # Remove the line after a short delay
                # Schedule clearing after 0.5 second
                turtle.ontimer(clear_laser, 500)  

        def clear_laser():
            laser.clear()
            laser.hideturtle()

        move_laser() 