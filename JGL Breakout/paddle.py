"""The paddle for the python version of breakout using Turtle!"""

from turtle import Turtle

MOVE_STEPS = 20

class jglPaddle(Turtle):
    """Creates the paddle and allows it to move"""
    
    def __init__(self) -> None:
        """Creates the paddle and moves it to 
        its initial position"""

        super().__init__()
        self.penup()
        self.goto((0, -300))
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=5, stretch_wid=1)
        
    def jgl_move_paddle_left(self) -> None:
        jgl_new_x_pos = self.xcor() - MOVE_STEPS
        self.goto(jgl_new_x_pos, self.ycor())
        
    def jgl_move_paddle_right(self) -> None:
        jgl_new_x_pos = self.xcor() + MOVE_STEPS
        self.goto(jgl_new_x_pos, self.ycor())
        
    def jgl_reset_paddle_position(self) -> None:
        self.goto((0, -300))