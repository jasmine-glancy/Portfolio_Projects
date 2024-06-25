"""A program that emulates the original game Breakout, 
published by Atari, Inc. and released on May 13, 1976!"""

from paddle import jglPaddle
from turtle import Screen
import time
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
jgl_paddle = jglPaddle((0, -300))

jgl_game_on = True

while jgl_game_on:
    jgl_screen.update()
    time.sleep(1)
    # TODO: Paddle is controlled by the mouse moving left to right
# TODO: Create the ball
    # TODO: User must click the right mouse button to launch the ball 
        # toward the wall
    # TODO: The ball is launched at an angle depending on how it hits the
        # paddle

# TODO: Load in scoreboard

# TODO: Allow user input from the mouse or keyboard?
    # TODO: Allow user to launch the ball from the paddle
    # TODO: Enable paddle to move left
    # TODO: Enable paddle to move right

# TODO: Start game in progress flag

# TODO: Check if ball collides with the left or right walls
    # TODO: If so, bounce the ball at an angle
    
# TODO: Detect collision with the paddle
    # TODO: Ball bounces at an angle depending on where it was hit
    
# TODO: Detect when paddle misses
    # TODO: Lose a life
    # TODO: Reset the ball's position
    # TODO: After 3 lives lost, trigger game over
    
# TODO: Detect collision with the wall
    # TODO: When the brick is hit, it dissolves
    
# TODO: Show high score screen
jgl_screen.exitonclick()