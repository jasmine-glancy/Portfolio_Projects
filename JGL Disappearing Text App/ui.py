"""
    The UI for the Writer's Block Buster!
"""
import tkinter as tk
from tkinter.constants import CENTER

FONT_CHOICE = ("Helvetica Monospaced", 20, "bold")

class JglWritersBlockBuster():
    def __init__(self):
        """Loads the window and the functions"""
        
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Writer's Block Buster")
        self.jgl_window.geometry("700x500")
        self.jgl_load_colors()
        self.jgl_instructions()
        self.jgl_start_button()
        self.jgl_window.config(padx=20, pady=20, background=self.russian_violet)
        self.jgl_window.mainloop()

    def jgl_load_colors(self):
        """Loads in colors from https://coolors.co/palette/f4effa-2f184b-532b88-9b72cf-c8b1e4"""
        
        self.magnolia = "#F4EFFA"
        self.russian_violet = "#2F184B"
        self.tekhelet = "#532B88"
        self.amethyst = "#9B72CF"
        self.wisteria = "#C8B1E4"
        
    def jgl_instructions(self):
        
        self.jgl_instructions = tk.Label()
        self.jgl_instructions.config(
            text="Type as much as you can!",
            bg=self.russian_violet,
            fg=self.amethyst,
            font=("Helvetica Monospaced", 14, "normal"))
        self.jgl_instructions.place(relx=0.5, rely=0.4, anchor=CENTER)
        
        self.jgl_warning = tk.Label()
        self.jgl_warning.config(
            text="If you stop for more than 5 seconds, the words are wiped.",
            bg=self.russian_violet,
            fg=self.amethyst,
            font=("Helvetica Monospaced", 14, "normal"))
        self.jgl_warning.place(relx=0.5, rely=0.5, anchor=CENTER)
        
    def jgl_start_button(self):
        """When the start button is clicked, the application begins"""

        self.start_button = tk.Button(text="Start Writing!",
                                      width=35,
                                      highlightthickness=0,
                                      bg=self.tekhelet,
                                      fg=self.wisteria,
                                      activebackground=self.amethyst,
                                      activeforeground=self.magnolia,
                                      pady=10,
                                      padx=10,
                                      font=FONT_CHOICE)
        self.start_button.place(relx=0.5, rely=0.75, anchor=CENTER)
    


# TODO: Load a cursor that moves to reveal typed text

# TODO: As long as the user continues to type with breaks no longer than 
# # 5-10 seconds, the application continues

# TODO: If the exercise ends, display "The time ran out, killing your darlings!"
