
"""A typing speed test that tells how long it has taken the user to 
successfully write out a string of texts"""

import ctypes
import time
import tkinter as tk
from tkinter.constants import CENTER


# Suggested by ThePythonCode.Com for a sharper window
# (https://thepythoncode.com/article/how-to-make-typing-speed-tester-in-python-using-tkinter)
ctypes.windll.shcore.SetProcessDpiAwareness(1)

JGL_FONT_CHOICE = ("Helvetica Monospaced", 25, "normal")

class JglTypingUI():
    def __init__(self) -> None:
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Speed Typing Test")
        self.jgl_window.geometry("700x500")
        self.jgl_load_colors()
        self.jgl_start_button()
        self.jgl_window.config(padx=20, pady=20, background=self.jgl_light_pink)
        self.jgl_window.mainloop()
        
    def jgl_load_colors(self) -> str:
        """Loads in colors from https://coolors.co/palette/cdb4db-ffc8dd-ffafcc-bde0fe-a2d2ff"""
        self.jgl_baby_blue = "#BDE0FE"
        self.jgl_robin_egg_blue = "#A2D2FF"
        self.jgl_light_pink = "#FFC8DD"
        self.jgl_darker_pink = "#FFAFCC"
        self.jgl_purple = "#CDB4DB"
        
    def jgl_start_button(self) -> None:
        """Starts the test when clicked"""
        
        jgl_start_button = tk.Button(text="Start Test!", width=35, highlightthickness=0, 
                                     bg=self.jgl_purple, fg=self.jgl_baby_blue, pady=10, padx=10)
        
        jgl_start_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        # TODO: Program start button to go away when it is clicked
        # TODO: Button starts the game
        
    def jgl_start_game(self) -> None:
        """Loads the test"""

        # TODO: Show time left on the timer
        # TODO: Load in the chosen string 5 words at a time
            # TODO: On the left are the letters/words that already have been written, 
                # and on the right are the letters that will be written. 
                # User should type the letter which is currently on the grey letters so that letter moves over.
            # The first part of the string should be a different color than the second
            # Put ... before and after section
        # TODO: Load in the current letter to type at the bottom of the screen
            # has to be typed in order to continue

        # TODO: After the time has passed, switch screen to finished_screen
            
    def jgl_finished_screen(self) -> None:
        """Loads the final screen of the game with an option to restart"""
        
        # TODO: Show what the WPM is
        # TODO: Include a button to restart the test
        # TODO: Show typo count
        
        
            



    
