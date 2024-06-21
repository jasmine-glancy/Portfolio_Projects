
"""A typing speed test that tells how long it has taken the user to 
successfully write out a string of texts"""

import ctypes
import time
import tkinter as tk

# Suggested by The Python Code.Com for a sharper window
# (https://thepythoncode.com/article/how-to-make-typing-speed-tester-in-python-using-tkinter)
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class JglTypingUI():
    def __init__(self) -> None:
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Speed Typing Test")
        self.jgl_window.geometry('700x500')
        self.jgl_load_colors()
        self.jgl_window.config(padx=20, pady=20, background=self.jgl_light_pink)
        self.jgl_window.mainloop()
        
    def jgl_load_colors(self) -> str:
        """Loads in colors from https://coolors.co/palette/cdb4db-ffc8dd-ffafcc-bde0fe-a2d2ff"""
        self.jgl_baby_blue = "#BDE0FE"
        self.jgl_robin_egg_blue = "#A2D2FF"
        self.jgl_light_pink = "#FFC8DD"
        self.jgl_darker_pink = "#FFAFCC"
        self.jgl_purple = "#CDB4DB"
        
    

# TODO: Show time left on the timer

# TODO: Program possible texts

# TODO: On the left are the letters/words that already have been written, 
# and on the right are the letters that will be written. 
#   We always want the user to type the letter which is currently on the 
    #   left of the grey letters so that letter moves over. 
    
# TODO: View the letter at the bottom of the screen to indicate that letter
    # has to be typed in order to continue
    
# TODO: After the time has passed, switch screen
    # TODO: Show what the WPM is
    # TODO: Include a button to restart the test