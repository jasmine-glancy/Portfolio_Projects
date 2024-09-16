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

ALIEN_QUANTITY_MAX = jgl_aliens.get_alien_quantity()

# Make a copy of the global variable for modification
alien_quantity = ALIEN_QUANTITY_MAX


# Functions not tagged by jgl were suggested by CoPilot
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
 
def jgl_check_alien_collision(player_lasers, cannon, jgl_scoreboard) -> None:
    """Checks if the cannon's laser has hit one of the aliens"""
    global alien_quantity
    
    jgl_surprise_alien = jgl_mystery_ship.jgl_surprise_alien
    # Check if surprise alien is hit
    for laser in player_lasers:
        if laser.distance(jgl_surprise_alien) < 25:
            # Surprise alien has been hit
            jgl_alien_hit(jgl_surprise_alien, jgl_scoreboard)
            jgl_surprise_alien.clear()
            jgl_surprise_alien.hideturtle()
            
    # Iterate over alien list and laser lists
    aliens_to_remove = []
    lasers_to_remove = []
    

    for alien in jgl_aliens.jgl_aliens_list:
        for laser in player_lasers:
            if laser.distance(alien) < 25:
                # The laser hits the alien!
                jgl_alien_hit(alien, jgl_scoreboard)
                alien_quantity -= 1
                
                # print(f"ALIEN_QUANTITY: {alien_quantity}")

                # Mark the alien and laser for removal
                aliens_to_remove.append(alien)
                lasers_to_remove.append(laser)    
                            
                # Break out of the inner loop to prevent double hits
                break

    # Remove the marked aliens and lasers
    for alien in aliens_to_remove:
        if alien in jgl_aliens.jgl_aliens_list:
            print(f"Removing alien at ({alien.xcor()}, {alien.ycor()})")
            alien.clear()
            alien.hideturtle()
            jgl_aliens.jgl_aliens_list.remove(alien)

    for laser in lasers_to_remove:
        laser.clear()
        laser.hideturtle()
        cannon.clear_laser(laser)

    # Debugging: Print the length of the alien list
    # print(f"ALIEN_QUANTITY: {alien_quantity}, Actual list length: {len(jgl_aliens.jgl_aliens_list)}")

def jgl_alien_hit(alien, jgl_scoreboard):
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
                print(f"Laser hits the {jgl_bunker_name} at ({laser_x}, {laser_y})")
                
                
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
            
def jgl_check_cannon_collision(alien_lasers, cannon, jgl_scoreboard) -> None:
    """Checks if any aliens have hit the player"""
    
    jgl_cannon_borders = cannon.jgl_cannon_borders()
    lasers_to_remove = []
    
    for laser in alien_lasers:
        
        jgl_laser_x = laser.xcor()
        jgl_laser_y = laser.ycor()
        
        # Abridged border condition checks recommended by CoPilot
        if (jgl_cannon_borders["left"] <= jgl_laser_x <= jgl_cannon_borders["right"] and
            jgl_cannon_borders["bottom"] <= jgl_laser_y <= jgl_cannon_borders["top"]):
            # Alien hits the player!
            print("Player is hit!")
            
            jgl_scoreboard.jgl_remove_life()
            lasers_to_remove.append(laser)
            
    for laser in lasers_to_remove:
        jgl_aliens.clear_laser(laser)

     
# ---------------------- Losing conditionals ---------------------- #

def jgl_aliens_reach_player(cannon, bunkers: JglBunkers) -> str:
    """Checks if the aliens have reached the player"""
    
    jgl_cannon_borders = cannon.jgl_cannon_borders()
    bunker_y_coords = bunkers.get_bunker_y_coords()
    
    print(f"Cannon Borders: {jgl_cannon_borders}")
    print(f"Number of Aliens: {len(jgl_aliens.jgl_aliens_list)}")
    
    for alien in jgl_aliens.jgl_aliens_list:
        alien_y = alien.ycor()

        for bunker in bunkers.bunker_map:
            bunker_name = bunkers.bunker_map[bunker]
            hit_counter = bunkers.hit_counters[bunker_name]
            
            print(f"Alien Y-Coordinate: {alien_y}, Bunker: {bunker_name}, Hit Counter: {hit_counter}")
            
            if bunkers.hit_counters[bunker_name] < 3 and alien.ycor() <= bunker_y_coords[bunker_name]:
                # If the bunkers are still up and the aliens reach them, trigger game over
                
                print("Aliens have reached the bunkers!")
                return "bunker"
        
        if alien.ycor() <= jgl_cannon_borders["top"]:
            # If aliens have reached the player
                
            print("Aliens have reached the player!")
            return "player"
        
    return "none"


# ----------------------- Check for "wins" ----------------------- #

def jgl_check_all_aliens_gone() -> None:
    """Checks if the current wave is gone"""
    
    global alien_quantity, ALIEN_QUANTITY_MAX
    
    if alien_quantity == 0:
        # Reset aliens and start their position slightly lower
        jgl_aliens.jgl_lower_starting_position()
        print("All aliens are gone. Resetting...")
        
        # Reset alien quantity
        alien_quantity = ALIEN_QUANTITY_MAX
        
def jgl_check_if_lives_left(jgl_scoreboard) -> None:
    """Checks if the user has any lives left"""
    
    lives = int(jgl_scoreboard.jgl_lives)
    
    if lives > 0:
        return True
    
    return False
    
    
        
        