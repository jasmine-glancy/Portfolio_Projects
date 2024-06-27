"""A Turtle scoreboard for a game such as Breakout!"""

from cs50 import SQL
from datetime import datetime
from turtle import Turtle

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///high_scores.db")


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
        
        
    def jgl_save_score(self) -> None:
        """Asks user for their name and saves their score"""
    
        # Asks user for their name
        jgl_player_name = self.getscreen().textinput("name", "Please enter your name:")
        
        try:
            # Saves the information to the database
            db.execute(
                "INSERT INTO high_scores (player_name, high_score, score_obtained_on) VALUES (?, ?, CURRENT_TIMESTAMP)",
                jgl_player_name, self.jgl_score
            )
        except Exception as e:
            self.write(f"Couldn't save your score, {e}", align="left", font=("Courier", 24, "normal"))
            self.goto(0, -180)
    
            
    def jgl_top_scores(self) -> None:
        """Shows the top 5 high scores"""
        

        self.clear()
        self.goto(0, 300)
        
        try:
            jgl_top_scores = db.execute(
                "SELECT player_name, high_score, score_obtained_on FROM high_scores ORDER BY high_score DESC LIMIT 10"
            )
            self.goto(0, 250)
            self.write("Top Scores", align="center", font=("Courier", 30, "bold"))
            
            for index, jgl_score in enumerate(jgl_top_scores):
                jgl_date_str = jgl_score["score_obtained_on"].split()[0]
                self.goto(0, 185 - (50 * index))
                self.write(f"{index + 1}. {jgl_score['player_name']}: {jgl_score['high_score']} {jgl_date_str}", align="center", font=("Courier", 18, "normal"))
        except Exception as e:
            self.write(f"Error fetching top scores:", align="center", font=("Courier", 24, "normal"))
            self.goto(0, -180)
            self.write(f"{e}", align="center", font=("Courier", 24, "normal"))
            self.goto(0, -300)

            

