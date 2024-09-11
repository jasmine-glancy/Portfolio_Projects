"""A Python version of the 1978 shoot 'em up game Space Invaders!"""

from bunkers import JglBunkers
from cannon import JglCannon
import gameplay as gp
import time
from screen_setup import jgl_screen
from scoreboard import JglScoreBoard

# Create cannon
jgl_cannon = JglCannon()

# Create bunkers
jgl_bunkers = JglBunkers()

# Event listeners to check for user input
jgl_screen.listen()

# Movement is controlled by the "A" and "D" keys
jgl_screen.onkeypress(jgl_cannon.jgl_move_cannon_left, "a")
jgl_screen.onkeypress(jgl_cannon.jgl_move_cannon_right, "d")

# Cannon is fired with the space bar
jgl_screen.onkeypress(jgl_cannon.jgl_shoot_cannon, "space")

# Set game flag
jgl_game_on = True

# Show scoreboard
jgl_score = JglScoreBoard()

# TODO: The game ends immediately if the aliens reach the bottom of the screen
    
# TODO: The goal is to eliminate all of the aliens by shooting them

    # TODO: As the aliens are defeated, their movement and the music speed up

    # TODO: When all the aliens are defeated, bring another wave which starts lower
        # Loop continues

# Start the game updates and laser firing
gp.update_game()
gp.fire_alien_laser()
gp.jgl_schedule_mystery_ship()

# Main loop to keep the screen updating
while jgl_game_on:
    jgl_screen.update()
    time.sleep(0.1)
    gp.jgl_check_bunker_collision(jgl_cannon.lasers, gp.jgl_aliens.jgl_alien_laser_list, jgl_bunkers) 
    
jgl_screen.exitonclick()