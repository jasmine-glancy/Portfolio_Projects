
"""A typing speed test that tells how long it has taken the user to 
successfully write out a string of texts"""

import ctypes
from text_bank import JglTexts
import time
import tkinter as tk
from tkinter.constants import CENTER, E, N, W


# Suggested by ThePythonCode.Com for a sharper window
# (https://thepythoncode.com/article/how-to-make-typing-speed-tester-in-python-using-tkinter)
ctypes.windll.shcore.SetProcessDpiAwareness(1)

JGL_FONT_CHOICE = ("Helvetica Monospaced", 20, "bold")

class JglTypingUI():
    def __init__(self) -> None:
        """Loads the window and the functions"""
        
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Speed Typing Test")
        self.jgl_window.geometry("700x500")
        self.jgl_load_colors()
        self.jgl_start_button()
        self.jgl_window.config(padx=20, pady=20, background=self.jgl_pink)
        self.jgl_window.mainloop()
        
    def jgl_load_colors(self) -> str:
        """Loads in colors from https://coolors.co/palette/231942-5e548e-9f86c0-be95c4-e0b1cb"""
        
        self.jgl_pink = "#E0B1CB"
        self.jgl_darker_pink = "#BE95C4"
        self.jgl_light_purple = "#9F86C0"
        self.jgl_purple = "#5E548E"
        self.jgl_deep_purple = "#231942"
        
    def jgl_start_button(self) -> None:
        """Starts the test when clicked"""
        
        self.jgl_explain = tk.Label()
        self.jgl_explain.config(text="Type the letter closest to the bottom of the screen to progress!", 
                               bg=self.jgl_pink, 
                               fg=self.jgl_purple,
                               font=("Helvetica Monospaced", 14, "bold"))
        self.jgl_explain.place(relx=0.5, rely=0.3, anchor=CENTER)
        
        self.jgl_starting_button = tk.Button(text="Start Test!", width=35, highlightthickness=0, 
                                     bg=self.jgl_deep_purple, fg=self.jgl_darker_pink, pady=10, padx=10,
                                     font=JGL_FONT_CHOICE, command=self.jgl_start_game)
        
        self.jgl_starting_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        
    def jgl_start_game(self) -> None:
        """Loads the test"""

        print("Tapped!")
        
        # Starts the game
        game_on = True
        
        # TODO: Create and load Key Press function
        # self.jgl_window.bind('<Key>', jglKeyPress)
        
        # Create a dictionary of possible texts 
        jgl_texts = JglTexts()
        
        # Makes the start button and explanation go away when game is started
        self.jgl_starting_button.destroy()
        self.jgl_explain.destroy()
        
        # TODO: Show time left on the timer
        self.jgl_time_left = tk.Label()
        self.jgl_time_left.config(text="seconds left", 
                               bg=self.jgl_pink, 
                               fg=self.jgl_darker_pink,
                               font=JGL_FONT_CHOICE)
        self.jgl_time_left.place(relx=0.5, rely=0.4, anchor=CENTER)

        # -------------- Load in the chosen string ---------------- #
        
        # Choose a random text from the text bank
        jgl_random_text = jgl_texts.jgl_random_text()
        print(jgl_random_text)
        
        # Set the split point
        jgl_text_split = 0
        
        
        # Left Text
        self.jgl_left_text = tk.Label()
        self.jgl_left_text.config(text=jgl_random_text[0:jgl_text_split], 
                               bg=self.jgl_pink, 
                               fg=self.jgl_purple,
                               font=JGL_FONT_CHOICE)
        self.jgl_left_text.place(relx=0.5, rely=0.5, anchor=E)
        
       
        # Right Text
        self.jgl_right_text = tk.Label()
        self.jgl_right_text.config(text=jgl_random_text[jgl_text_split:], 
                               bg=self.jgl_pink, 
                               fg=self.jgl_light_purple,
                               font=JGL_FONT_CHOICE)
        self.jgl_right_text.place(relx=0.5, rely=0.5, anchor=W)
        
        # Load in the current letter to type at the bottom of the screen
        self.jgl_current_letter = tk.Label()
        self.jgl_current_letter.config(text=jgl_random_text[jgl_text_split], 
                               bg=self.jgl_pink, 
                               fg=self.jgl_light_purple,
                               font=JGL_FONT_CHOICE)
        self.jgl_current_letter.place(relx=0.5, rely=0.6, anchor=CENTER)
            # TODO: Letter has to be typed in order to continue
        
        # TODO: Load in the chosen string 5 words at a time
            # TODO: On the left are the letters/words that already have been written, 
                # and on the right are the letters that will be written. 
                # User should type the letter which is currently on the grey letters so that letter moves over.
            # The first part of the string should be a different color than the second
            # Put ... before and after section
 

        # TODO: After the time has passed, switch screen to finished_screen
            
    def jgl_finished_screen(self) -> None:
        """Loads the final screen of the game with an option to restart"""
        
        # TODO: Show what the WPM is
        # TODO: Include a button to restart the test
        # TODO: Show typo count
        
        
            



    
