"""The paddle for the python version of breakout using Turtle!"""

from turtle import Turtle

MOVE_STEPS = 20

class jglPaddle(Turtle):
    """Creates the paddle and allows it to move"""
    
    def __init__(self, position):
        """Creates the paddle and moves it to its position"""

        super().__init__()
        self.penup()
        self.goto(position)
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_len=5, stretch_wid=1)
    # TODO: Create function to move paddle left

    # TODO: Create function to move paddle right