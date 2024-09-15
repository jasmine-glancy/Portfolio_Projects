"""The scoreboard and lives for the python version of 
Space Invaders using Turtle!"""

from database import SPACE_INVADERS_SESSION, HighScores
from datetime import datetime
from turtle import Turtle
import queries as q

# Create database session for queries
si_session = SPACE_INVADERS_SESSION

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
        
    def jgl_remove_life(self) -> None:
        """Increases the score and updates the board"""
        
        self.jgl_lives -= 1
        self.clear()
        self.jgl_update_scoreboard()
        
class JglNotifications(Turtle):
    """Controls the notifications displayed to the player"""
    
    def __init__(self, scoreboard: JglScoreBoard):
        super().__init__()
        self.jgl_game_status = Turtle()
        self.jgl_game_status.hideturtle()
        self.jgl_game_status.penup()
        self.jgl_game_status.color("white")
        self.jgl_scoreboard = scoreboard 
        
    def jgl_game_over(self) -> None:
        """Notifies the player the game has stopped"""
        
        self.jgl_game_status.goto(0, 0)
        self.jgl_game_status.write("GAME OVER!", align="center", font=("Courier", 20, "bold"))
        

    def jgl_save_score(self) -> None:
        """Asks user for their name and saves their score"""
    
        # Asks user for their name
        jgl_player_name = self.getscreen().textinput("Game over! Save score:", "Please enter your name:")
        
        # Debug: Print the player name and score
        print(f"Player Name: {jgl_player_name}")
        print(f"Scoreboard Instance: {self.jgl_scoreboard}")
        print(f"Score: {self.jgl_scoreboard.jgl_score}")
        print(f"Date: {datetime}.now()")
    
        try:
            # Saves the information to the database
            new_high_score = HighScores(
                player_name=jgl_player_name, 
                score=self.jgl_scoreboard.jgl_score,
                score_obtained_on=datetime.now()
            )
            
            # Add the record to the session
            SPACE_INVADERS_SESSION.add(new_high_score)
            
            # Commit the record to the database
            SPACE_INVADERS_SESSION.commit()
            
        except Exception as e:
            SPACE_INVADERS_SESSION.rollback()
            self.write(f"Couldn't save your score, {e}", align="left", font=("Courier", 24, "normal"))
            self.goto(0, -180)
    
        finally:
            # Close the session    
            SPACE_INVADERS_SESSION.close()
            
            
    def jgl_top_scores(self) -> None:
        """Shows the top 5 high scores"""
        

        self.clear()
        self.goto(0, 300)
        
        try:
            jgl_top_scores = q.jgl_find_top_scores()
            print(jgl_top_scores)
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