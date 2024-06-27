"""A program that emulates the original game Breakout, 
published by Atari, Inc. and released on May 13, 1976!"""

from ball import jglBall
from paddle import jglPaddle
from turtle import Screen, Turtle
import time
from scoreboard import jglScoreboard
from walls import jglWalls

# Create the screen
jgl_screen = Screen()
jgl_screen.setup(width=950, height=750)
jgl_screen.bgcolor("black")
jgl_screen.title("Breakout by JGL")

# Turn off automatic screen updates 
jgl_screen.tracer(0)

# Build walls
jgl_walls = jglWalls()

# Create the paddle
jgl_paddle = jglPaddle()

# Set game flag
jgl_game_on = True

# Load in scoreboard
jgl_score = jglScoreboard(jgl_game_on)

# Create the ball
jgl_ball = jglBall((0, -280), jgl_walls, jgl_game_on, jgl_score, jgl_paddle)

# Event listeners to check for user input
jgl_screen.listen()

# Movement is controlled by the "A" and "D" keys
jgl_screen.onkeypress(jgl_paddle.jgl_move_paddle_left, "a")
jgl_screen.onkeypress(jgl_paddle.jgl_move_paddle_right, "d")

# Launches the ball on click
jgl_screen.onclick(jgl_ball.jgl_launch_ball)


while jgl_game_on:
    
    # Checks if the ball has been launched yet to determine movement
    if jgl_ball.jgl_moving_with_paddle:
        jgl_ball.jgl_display_instructions()
        jgl_ball.jgl_move_with_paddle(jgl_paddle)
    else:
        jgl_ball.jgl_hide_instructions()
        jgl_ball.jgl_move()
        
    # Updates the screen and makes the ball move 
    #  faster as the game goes on
    time.sleep(jgl_ball.jgl_move_speed)
    jgl_screen.update()
    
    # Check if collision with walls
    jgl_ball.jgl_check_collision_with_walls()
    
    # Detect collision with the paddle
    jgl_ball.jgl_check_collision_with_paddle(jgl_paddle)
    
    # Detect collision with bricks
    jgl_ball.jgl_check_collision_with_bricks()

    if jgl_score.jgl_lives == 0:
        print("Game over!")
        jgl_game_on = False
        jgl_score.jgl_save_score()
        
        # Hide the turtles before showing the final scores
        jgl_ball.hideturtle()
        
        for brick in jgl_walls.jgl_bricks:
            brick.reset()
        jgl_paddle.reset()
        
        # Show top 10 highest scores
        jgl_score.jgl_top_scores()
        
jgl_screen.exitonclick()