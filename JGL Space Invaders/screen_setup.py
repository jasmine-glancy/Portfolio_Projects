"""Creates the screen for the Python version of Space Invaders"""

from turtle import Screen

# Create screen
jgl_screen = Screen()
jgl_screen.setup(width=950, height=750)
jgl_screen.bgcolor("black")
jgl_screen.title("Turtle Invaders by JGL")


# Turn off automatic screen updates
jgl_screen.tracer(0)
