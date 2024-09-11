"""Adds various events to the Python version of Space Invaders"""

from aliens import JglRowsOfAliens, JglMysteryShip
from bunkers import JglBunkers
from turtle import ontimer
from screen_setup import jgl_screen

# ------------------ Alien functionality ------------------ #
 
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
    
# ---------------- Collision functionality ---------------- #


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
        
    # TODO: Bunkers are gradually destroyed from the top by the alien lasers
    
    # If bunker x distance is less than either laser x distance, reduce bunker size

        
    # TODO: If the player fires underneath the bunker, the bottoms get destroyed
    