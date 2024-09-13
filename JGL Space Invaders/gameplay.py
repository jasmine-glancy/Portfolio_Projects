"""Adds various events to the Python version of Space Invaders"""

from aliens import JglRowsOfAliens, JglMysteryShip
from bunkers import JglBunkers
import queries as q
from turtle import ontimer
import scoreboard as sb
from screen_setup import jgl_screen

# ---------------------- Alien functionality ---------------------- #
 
# Build the aliens
jgl_aliens = JglRowsOfAliens(jgl_screen)

# Functions suggested by CoPilot
def update_game() -> None:
    """Moves the aliens and updates the screen"""
    jgl_aliens.jgl_move_aliens()
    ontimer(update_game, 1000)
    
    
def fire_alien_laser() -> None:
    """Allows the "aliens" to fire a laser at the player"""
    jgl_aliens.jgl_alien_lasers()
    ontimer(fire_alien_laser, 3000)
  
        
def jgl_check_aliens_in_list() -> bool:
    """Makes sure the aliens exist"""
    
    if jgl_aliens.jgl_aliens_list:
        return True
    
    return False


def jgl_stop_aliens() -> None:
    """Stops aliens if the game is over"""
    
    jgl_aliens.jgl_stop_movement()
    
    
# Build the mystery ship
jgl_mystery_ship = JglMysteryShip()

def jgl_show_mystery_ship() -> None:
    """Randomly makes the mystery ship fly across
    the screen"""
    
    jgl_mystery_ship.jgl_fly_mystery_ship()
    ontimer(jgl_show_mystery_ship, 100)
    
    
def jgl_schedule_mystery_ship() -> None:
    """Schedules the mystery ship to appear every 20 seconds"""
    
    jgl_mystery_ship.jgl_surprise_alien.goto(500, 345)
    jgl_show_mystery_ship()
    ontimer(jgl_schedule_mystery_ship, 20000)
    
# -------------------- Collision functionality -------------------- #

jgl_scoreboard = sb.JglScoreBoard()

def jgl_check_alien_collision(player_lasers, cannon) -> None:
    """Checks if the cannon's laser has hit one of the aliens"""
    
    jgl_surprise_alien = jgl_mystery_ship.jgl_surprise_alien
    # Check if surprise alien is hit
    for laser in player_lasers:
        if laser.distance(jgl_surprise_alien) < 25:
            # Surprise alien has been hit
            jgl_alien_hit(jgl_surprise_alien)
            jgl_surprise_alien.clear()
            jgl_surprise_alien.hideturtle()
            
    # Iterate over alien list and laser lists
    for alien in jgl_aliens.jgl_aliens_list:
        for laser in player_lasers:
            if laser.distance(alien) < 25:
                # The laser hits the alien!
                
                jgl_alien_hit(alien)
                jgl_aliens.jgl_alien_quantity -= 1
                    
                # Remove the alien from the list
                if alien in jgl_aliens.jgl_aliens_list:
                    alien.clear()
                    alien.hideturtle()
                    jgl_aliens.jgl_aliens_list.remove(alien)
                    
                # Remove the laser from the list
                laser.clear()
                laser.hideturtle()
                cannon.clear_laser(laser)

def jgl_alien_hit(alien):
    # Get the color of the alien
    alien_color = alien.color()[0] 
    
    # Query the database for the ID that matches the color string
    color_id = q.jgl_find_color_id(alien_color)
    
    # Query the database for the score associated with the alien color ID
    score = q.jgl_find_score_value(color_id)
    
    print(f"Alien hit! Color: {alien_color}, Color ID: {color_id}, Score: {score}")
    jgl_scoreboard.jgl_increase_score(score=score)
    
    # Increase alien speed
    jgl_aliens.jgl_increase_alien_speed()                
                   
def jgl_check_bunker_collision(player_lasers, alien_lasers, bunkers: JglBunkers) -> None:
    """Checks if any laser has "blasted" the bunkers"""
    
    jgl_bunker_data = bunkers.jgl_get_bunker_range_dict()
    
    # Combine both sets of lasers into a single list
    all_lasers = player_lasers + alien_lasers
    
    for laser in all_lasers:
        laser_x = laser.xcor()
        laser_y = laser.ycor()
        
        # print(f"Checking laser at ({laser_x}, {laser_y})")
        
        for jgl_bunker_name, data in jgl_bunker_data.items():
            x_range = data["x_range"]
            y_range = data["y_range"]
            
            # print(f"Checking bunker {jgl_bunker_name} with x_range {x_range} and y_range {y_range}")
            
            if x_range[0] < laser_x < x_range[1]and y_range[0] < laser_y < y_range[1]:
                # If the left edge of the bunker is less than or equal to the lasers' x-coordinates
                ## or the lasers' x-coordinates are greater than or equal to the right edge of the bunker
                # print(f"Laser hits the {jgl_bunker_name} at ({laser_x}, {laser_y})")
                
                
                # Reduce bunker size when hit
                bunker = getattr(bunkers, f"jgl_{jgl_bunker_name}")
                print(f"Shrinking bunker {jgl_bunker_name} with current size {bunker.shapesize()}")

                bunkers.shrink_bunker(bunker)

                laser.hideturtle()
                laser.clear()
                
                # Remove the laser from the appropriate list
                if laser in player_lasers:
                    print("Removing laser from player_lasers")
                    player_lasers.remove(laser)
                elif laser in alien_lasers:
                    print("Removing laser from alien_lasers")
                    alien_lasers.remove(laser)
                
                
                # Get new range
                jgl_bunker_data = bunkers.jgl_get_bunker_range_dict()
                
                # Exit the loop once a collision is detected
                break
        
     
# ---------------------- Losing conditionals ---------------------- #

def jgl_aliens_reach_player(cannon, bunkers: JglBunkers) -> bool:
    """Checks if the aliens have reached the player"""
    
    top_of_cannon = cannon.jgl_cannon_top()
    bunker_y_coords = bunkers.get_bunker_y_coords()
    
    for bunker in bunkers.bunker_map:
        
        bunker_name = bunkers.bunker_map[bunker]
        for alien in jgl_aliens.jgl_aliens_list:
                
            if bunkers.hit_counters[bunker_name] >= 3 and alien.ycor() <= top_of_cannon:
                # If the bunkers have been destroyed aliens have reached the player
            
                return True
            
            elif bunkers.hit_counters[bunker_name] < 3 and alien.ycor() <= bunker_y_coords[bunker_name]:
                # If the bunkers are still up and the aliens reach them, trigger game over
                return True
    
    return False


# ----------------------- Check for "wins" ----------------------- #

def jgl_check_all_aliens_gone() -> None:
    """Checks if the current wave is gone"""
    
    if jgl_aliens.jgl_alien_quantity <= 0:
        # TODO: Reset aliens and start their position slightly lower
        pass
