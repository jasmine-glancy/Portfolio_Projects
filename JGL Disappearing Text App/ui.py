"""
    The UI for the Writer's Block Buster!
"""
import tkinter as tk

class JglWritersBlockBuster():
    def __init__(self) -> None:
        """Loads the window and the functions"""
        
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Writer's Block Buster")
        self.jgl_window.geometry("700x500")
        self.jgl_load_colors()
        self.jgl_window.config(padx=20, pady=20, background=self.russian_violet)
        self.jgl_window.mainloop()

    def jgl_load_colors(self) -> str:
        """Loads in colors from https://coolors.co/palette/f4effa-2f184b-532b88-9b72cf-c8b1e4"""
        
        self.magnolia = "#F4EFFA"
        self.russian_violet = "#2F184B"
        self.tekhelet = "#532B88"
        self.amethyst = "#9B72CF"
        self.wisteria = "#C8B1E4"
        

