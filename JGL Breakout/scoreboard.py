"""A Turtle scoreboard for a game such as Breakout!"""

from turtle import Turtle

class jglScoreboard(Turtle):
    
    def __init__(self, jgl_game_on) -> None:
        """Initializes the score and number of lives"""
        
        super().__init__()
        self.jgl_game_on = jgl_game_on
        self.color("white")
        self.penup()
        self.hideturtle()
        self.jgl_score = 0
        self.jgl_lives = 3
        self.jgl_update_scoreboard()
        
    def jgl_increase_score(self) -> None:
        """Increases the score and updates the board"""
        
        self.jgl_score += 1
        self.clear()
        self.jgl_update_scoreboard()
        
    def jgl_update_scoreboard(self) -> None:
        """Keeps score and lives updated"""
        
        self.clear()
        self.goto(0, 321)
        self.write(f"Score: {self.jgl_score} | Lives: {self.jgl_lives}", align="left", font=("Courier", 24, "normal"))
        
    def jgl_remove_life(self) -> None:
        """Increases the score and updates the board"""
        
        self.jgl_lives -= 1
        self.clear()
        self.jgl_update_scoreboard()
        
        
            
    # TODO: Load in lives 
    
    # TODO: Create database for high scores