"""Adds various events to the Python version of Space Invaders"""

from aliens import JglRowsOfAliens, JglMysteryShip
from turtle import ontimer
from screen_setup import jgl_screen

# -------------- Alien functionality -------------- #
 
# Build the aliens
jgl_aliens = JglRowsOfAliens(jgl_screen)

# Functions suggested by CoPilot
def update_game():
    """Moves the aliens and updates the screen"""
    jgl_aliens.jgl_move_aliens()
    ontimer(update_game, 1000)
    
def fire_alien_laser():
    """Allows the "aliens" to fire a laser at the player"""
    jgl_aliens.jgl_alien_lasers()
    ontimer(fire_alien_laser, 3000)
        
# Build the mystery ship
jgl_mystery_ship = JglMysteryShip()

def jgl_show_mystery_ship():
    """Randomly makes the mystery ship fly across
    the screen"""
    
    jgl_mystery_ship.jgl_fly_mystery_ship()
    ontimer(jgl_show_mystery_ship, 100)
    
def jgl_schedule_mystery_ship():
    """Schedules the mystery ship to appear every 20 seconds"""
    
    jgl_mystery_ship.jgl_surprise_alien.goto(500, 345)
    jgl_show_mystery_ship()
    ontimer(jgl_schedule_mystery_ship, 20000)