"""A Python version of the 1978 shoot 'em up game Space Invaders!"""

from cannon import JglCannon
from turtle import Screen

# Create screen
jgl_screen = Screen()
jgl_screen.setup(width=950, height=750)
jgl_screen.bgcolor("black")
jgl_screen.title("Space Invaders by JGL")


# Turn off automatic screen updates
jgl_screen.tracer(0)

# Create cannon
jgl_cannon = JglCannon()

# TODO: Create "aliens" 

# TODO: Create bunkers

# Event listeners to check for user input
jgl_screen.listen()

# Movement is controlled by the "A" and "D" keys
jgl_screen.onkeypress(jgl_cannon.jgl_move_paddle_left, "a")
jgl_screen.onkeypress(jgl_cannon.jgl_move_paddle_right, "d")

# Set game flag
jgl_game_on = True

# TODO: Player has 3 lives
    # TODO: But the game ends immediately if the aliens reach the bottom of the screen
    
    
# TODO: The goal is to eliminate all of the aliens by shooting them

    # TODO: As the aliens are defeated, their movement and the music speed up

    # TODO: When all the aliens are defeated, bring another wave which starts lower
        # Loop continues

while jgl_game_on:
    jgl_screen.update()
    
jgl_screen.exitonclick()