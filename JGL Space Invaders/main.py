"""A Python version of the 1978 shoot 'em up game Space Invaders!"""

from bunkers import JglBunkers
from cannon import JglCannon
import gameplay as gp
import time
from screen_setup import jgl_screen
from scoreboard import JglNotifications, JglScoreBoard

# Create cannon
jgl_cannon = JglCannon()

# Create bunkers
jgl_bunkers = JglBunkers()

# Create an instance of JglScoreBoard and JglNotifications
jgl_scoreboard = JglScoreBoard()
jgl_notify = JglNotifications(jgl_scoreboard)

# Event listeners to check for user input
jgl_screen.listen()

# Movement is controlled by the "A" and "D" keys
jgl_screen.onkeypress(jgl_cannon.jgl_move_cannon_left, "a")
jgl_screen.onkeypress(jgl_cannon.jgl_move_cannon_right, "d")

# Cannon is fired with the space bar
jgl_screen.onkeypress(jgl_cannon.jgl_shoot_cannon, "space")

# Set game flag
jgl_game_on = True


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
    gp.jgl_check_aliens_in_list()
    gp.jgl_check_bunker_collision(jgl_cannon.lasers, gp.jgl_aliens.jgl_alien_laser_list, jgl_bunkers) 
    gp.jgl_check_alien_collision(jgl_cannon.lasers, jgl_cannon, jgl_scoreboard)
    gp.jgl_check_cannon_collision(gp.jgl_aliens.jgl_alien_laser_list, jgl_cannon, jgl_scoreboard)
    gp.jgl_check_all_aliens_gone()
    
    jgl_reach_status = gp.jgl_aliens_reach_player(jgl_cannon, jgl_bunkers)
    if jgl_reach_status == "player":
        gp.jgl_stop_aliens()
        jgl_notify.jgl_game_over()
        print("Game over! Aliens have reached the player.")
        jgl_game_on = False
    elif jgl_reach_status == "bunker":
        gp.jgl_stop_aliens()
        jgl_notify.jgl_game_over()
        print("Game over! Aliens have reached the bunkers.")
        jgl_game_on = False
          
    jgl_lives_left = gp.jgl_check_if_lives_left(jgl_scoreboard)
    
    if jgl_lives_left == False:
        
        jgl_notify.jgl_game_over()
        print("Game over!")
        jgl_game_on = False
  
if jgl_game_on == False:
    jgl_notify.jgl_save_score()
    
    # Show top 10 highest scores
    jgl_notify.jgl_top_scores()
jgl_screen.exitonclick()