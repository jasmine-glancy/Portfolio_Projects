"""The scoreboard and lives for the python version of 
Space Invaders using Turtle!"""

from turtle import Turtle

class JglScoreBoard(Turtle):
    def __init__(self) -> None:
        """Initializes the score and number of lives"""
        
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.jgl_score = 0
        self.jgl_lives = 3
        self.jgl_update_scoreboard()
        
    def jgl_update_scoreboard(self) -> None:
        """Keeps score and lives updated"""
        
        self.clear()
        self.goto(-460, -365)
        self.write(f"Lives: {self.jgl_lives} | Score: {self.jgl_score}", align="left", font=("Courier", 24, "normal"))
    
    def jgl_increase_score(self, score) -> None:
        """Increases the score and updates the scoreboard"""
        
        self.jgl_score += score
        self.clear()
        self.jgl_update_scoreboard()   
        
# TODO: Game ends immediately if the aliens reach the bottom of the screen
    
# TODO: Create table for the player's score
    # TODO: Create score values for the aliens
    # Bottom invaders–10 points.
    # Middle invaders–20 points.
    # Top invaders–30 points.
    # UFO–50, 100, 150, or 300 points.