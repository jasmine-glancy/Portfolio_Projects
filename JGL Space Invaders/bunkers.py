"""The bunkers for the python version of Space Invaders using Turtle!"""

from turtle import Turtle

class JglBunkers(Turtle):
    """Creates the bunkers"""
    
    def __init__(self):
        super().__init__()
        
        # Create left bunker
        self.jgl_left_bunker = Turtle()
        self.jgl_left_bunker.penup()
        self.jgl_left_bunker.shape("classic")
        self.jgl_left_bunker.setheading(90)
        self.jgl_left_bunker.color("pale green")
        self.jgl_left_bunker.shapesize(stretch_wid=15, stretch_len=10)
        self.jgl_left_bunker.goto(-350, -150)
        
        # Create middle bunker
        self.jgl_middle_bunker = Turtle()
        self.jgl_middle_bunker.penup()
        self.jgl_middle_bunker.shape("classic")
        self.jgl_middle_bunker.setheading(90)
        self.jgl_middle_bunker.color("pale green")
        self.jgl_middle_bunker.shapesize(stretch_wid=15, stretch_len=10)
        self.jgl_middle_bunker.goto(0, -150)
        
        # Create right bunker
        self.jgl_right_bunker = Turtle()
        self.jgl_right_bunker.penup()
        self.jgl_right_bunker.shape("classic")
        self.jgl_right_bunker.setheading(90)
        self.jgl_right_bunker.color("pale green")
        self.jgl_right_bunker.shapesize(stretch_wid=15, stretch_len=10)
        self.jgl_right_bunker.goto(350, -150)
        
        
    
    # TODO: Bunkers are gradually destroyed from the top by the alien lasers
    
    # TODO: If the player fires underneath the bunker, the bottoms get destroyed
    