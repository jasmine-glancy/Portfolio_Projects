"""A program that emulates the original game Breakout, 
published by Atari, Inc. and released on May 13, 1976!"""

from ball import jglBall
from paddle import jglPaddle
from turtle import Screen
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
jgl_ball = jglBall((0, -100), jgl_walls, jgl_game_on, jgl_score)


jgl_screen.listen()
jgl_screen.onkeypress(jgl_paddle.jgl_move_paddle_left, "a")
jgl_screen.onkeypress(jgl_paddle.jgl_move_paddle_right, "d")



while jgl_game_on:
    time.sleep(jgl_ball.jgl_move_speed)
    jgl_screen.update()
    jgl_ball.jgl_move()
    
    # Check if collision with walls
    jgl_ball.jgl_check_collision_with_walls()
    
    # Detect collision with the paddle
    jgl_ball.jgl_check_collision_with_paddle(jgl_paddle)
    
    # Detect collision with bricks
    jgl_ball.jgl_check_collision_with_bricks()

    if jgl_score.jgl_lives == 0:
        print("Game over!")
        jgl_game_on = False
    
# TODO: Show high score screen
jgl_screen.exitonclick()