
"""A typing speed test UI that tells how long it has taken the user to 
successfully write out a string of texts"""

import ctypes
from text_bank import JglTexts
import tkinter as tk
from tkinter.constants import CENTER, E, W


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
                               font=("Helvetica Monospaced", 14, "normal"))
        self.jgl_explain.place(relx=0.5, rely=0.3, anchor=CENTER)
        
        self.jgl_starting_button = tk.Button(text="Start Test!", width=35, highlightthickness=0, 
                                     bg=self.jgl_deep_purple, fg=self.jgl_darker_pink, pady=10, padx=10,
                                     font=JGL_FONT_CHOICE, command=self.jgl_start_game)
        
        self.jgl_starting_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        self.jgl_text_credit = tk.Label()
        self.jgl_text_credit.config(text="Hipster Ipsum credited to hipsum.co", 
                               bg=self.jgl_pink, 
                               fg=self.jgl_darker_pink,
                               font=("Helvetica Monospaced", 14, "normal"))
        self.jgl_text_credit.place(relx=0.5, rely=0.7, anchor=CENTER)
        
        
    def jgl_start_game(self) -> None:
        """Loads the test"""
        
        # Starts the game
        self.jgl_game_on = True
        
        # Create a dictionary of possible texts 
        jgl_texts = JglTexts()
        
        # Makes the start button and explanation go away when game is started
        self.jgl_starting_button.destroy()
        self.jgl_explain.destroy()
        self.jgl_text_credit.destroy()
        
        # ----------------- Load in the timer ------------------- #
        
        # Initiate the timer 
        self.jgl_seconds_left = 60
        
        # Show time left on the timer
        self.jgl_time_left = tk.Label()
        self.jgl_time_left.config(text=f"{self.jgl_seconds_left} seconds left", 
                               bg=self.jgl_pink, 
                               fg=self.jgl_darker_pink,
                               font=JGL_FONT_CHOICE)
        self.jgl_time_left.place(relx=0.5, rely=0.4, anchor=CENTER)
        

        # -------------- Load in the chosen string ---------------- #
        
        # Choose a random text from the text bank
        jgl_random_text = jgl_texts.jgl_random_text()
        print(jgl_random_text)
        
        # Set the split point, recommended by ThePyThonCode.com
        jgl_text_split = 0
        
        
        # Left Text (text already typed)
        self.jgl_left_text = tk.Label()
        self.jgl_left_text.config(text=jgl_random_text[0:jgl_text_split], 
                               bg=self.jgl_pink, 
                               fg=self.jgl_purple,
                               font=JGL_FONT_CHOICE)
        self.jgl_left_text.place(relx=0.5, rely=0.5, anchor=E)
        
       
        # Right Text (text to type)
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
        
        # Initiate typo count
        self.jgl_typo_count = 0
        
        # Current letter has to be typed in order to continue
        self.jgl_window.bind('<Key>', self.jgl_key_press)

        # After 60 seconds have passed, switch screen to finished_screen
        self.jgl_window.after(60000, self.jgl_finished_screen)
        self.jgl_counter()
        
    def jgl_finished_screen(self) -> None:
        """Loads the final screen of the game with an option to restart"""
        
        # Stops the game
        self.jgl_game_on = False
        
        # Show what the WPM is
        self.jgl_wpm = len(self.jgl_left_text.cget('text').split(' '))
        
        self.jgl_wpm_label = tk.Label()
        self.jgl_wpm_label.config(text=f"Your words per minute: {self.jgl_wpm}", 
                               bg=self.jgl_pink, 
                               fg=self.jgl_light_purple,
                               font=JGL_FONT_CHOICE)
        self.jgl_wpm_label.place(relx=0.5, rely=0.3, anchor=CENTER)
        
        # Hide the items on the previous screen
        self.jgl_left_text.destroy()
        self.jgl_right_text.destroy()
        self.jgl_current_letter.destroy()
        self.jgl_time_left.destroy()
        
        
        # Show typo count
        self.jgl_typo_result = tk.Label()
        self.jgl_typo_result.config(bg=self.jgl_pink, 
                                    fg=self.jgl_darker_pink,
                                    font=JGL_FONT_CHOICE)
        self.jgl_typo_result.place(relx=0.5, rely=0.5, anchor=CENTER)
        if self.jgl_typo_count == 1:
            self.jgl_typo_result.config(text=f"You had {self.jgl_typo_count} typo")
        else:
            self.jgl_typo_result.config(text=f"You had {self.jgl_typo_count} typos")
            
        # Include a button to restart the test
        self.jgl_restart_button = tk.Button(text="Try Again!", width=35, highlightthickness=0, 
                                     bg=self.jgl_deep_purple, fg=self.jgl_darker_pink, pady=10, padx=10,
                                     font=JGL_FONT_CHOICE, command=self.jgl_clear_board)
        
        self.jgl_restart_button.place(relx=0.5, rely=0.7, anchor=CENTER)
        
    def jgl_counter(self) -> None:
        """Counts down from 60"""
        
        try:
            self.jgl_time_left.config(text=f"{self.jgl_seconds_left} seconds left")
            
            self.jgl_seconds_left -= 1
            
            if self.jgl_game_on:
                # After recommended by ThePyThonCode.com
                self.jgl_window.after(1000, self.jgl_counter)
        except tk.TclError:
            pass
            
    def jgl_key_press(self, event=None) -> None:
        """Makes sure the user has to type the current letter shown"""
        
        try:
            # Conditions recommended by ThePythonCode.com
            if event.char == self.jgl_right_text.cget('text')[0]:
                # Deletes from the right side
                self.jgl_right_text.config(text=self.jgl_right_text.cget('text')[1:])
                self.jgl_left_text.config(text=self.jgl_left_text.cget('text') + event.char)
                
                # Get the next letter to type
                self.jgl_current_letter.config(text=self.jgl_right_text.cget('text')[0])
            else:
                # If the letter typed isn't the current letter, add to typo count
                self.jgl_typo_count += 1
                
        except tk.TclError:
            pass

    def jgl_clear_board(self) -> None:
        """Clears the board to start a new game"""
    
        self.jgl_wpm_label.destroy()
        self.jgl_typo_result.destroy()
        self.jgl_restart_button.destroy()
        self.jgl_start_game()