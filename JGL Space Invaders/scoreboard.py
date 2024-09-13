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
        
class JglNotifications(Turtle):
    """Controls the notifications displayed to the player"""
    
    def __init__(self):
        super().__init__()
        self.jgl_game_status = Turtle()
        self.jgl_game_status.hideturtle()
        self.jgl_game_status.penup()
        self.jgl_game_status.color("white")
        
    def jgl_game_over(self):
        """Notifies the player the game has stopped"""
        
        self.jgl_game_status.goto(0, 0)
        self.jgl_game_status.write("GAME OVER!", align="center", font=("Courier", 20, "bold"))