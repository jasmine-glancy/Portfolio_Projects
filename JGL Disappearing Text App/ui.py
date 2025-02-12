"""
    The UI for the Writer's Block Buster!
"""
import tkinter as tk
from tkinter.constants import CENTER

FONT_CHOICE = ("Helvetica Monospaced", 20, "bold")
SMALLER_FONT_CHOICE = ("Helvetica Monospaced", 14, "normal")


class JglWritersBlockBuster():
    def __init__(self):
        """Loads the window and the functions"""
        
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Writer's Block Buster")
        self.jgl_window.geometry("700x500")
        self.jgl_load_colors()
        self.jgl_start_page()
        self.jgl_window.config(padx=20, pady=20, background=self.russian_violet)
        self.jgl_window.mainloop()

    def jgl_start_page(self):
        """Load starting instructions and button"""
        self.jgl_instructions()
        self.jgl_start_button()    
        
    def jgl_load_colors(self):
        """Loads in colors from https://coolors.co/palette/f4effa-2f184b-532b88-9b72cf-c8b1e4"""
        
        self.magnolia = "#F4EFFA"
        self.russian_violet = "#2F184B"
        self.tekhelet = "#532B88"
        self.amethyst = "#9B72CF"
        self.wisteria = "#C8B1E4"
        
    def jgl_instructions(self):
        
        self.title = tk.Label()
        self.title.config(
            text="Writer's Block Buster",
            bg=self.russian_violet,
            fg=self.amethyst,
            font=FONT_CHOICE)
        self.title.place(relx=0.5, rely=0.2, anchor=CENTER)
        
        self.jgl_instructions_text = tk.Label()
        self.jgl_instructions_text.config(
            text="Type as much as you can!",
            bg=self.russian_violet,
            fg=self.amethyst,
            font=SMALLER_FONT_CHOICE)
        self.jgl_instructions_text.place(relx=0.5, rely=0.4, anchor=CENTER)
        
        self.jgl_warning = tk.Label()
        self.jgl_warning.config(
            text="If you stop for more than 5 seconds, the words are wiped.",
            bg=self.russian_violet,
            fg=self.amethyst,
            font=SMALLER_FONT_CHOICE)
        self.jgl_warning.place(relx=0.5, rely=0.5, anchor=CENTER)
        
    def jgl_start_button(self):
        """Makes the start button"""

        self.start_button = tk.Button(text="Start Writing!",
                                      width=35,
                                      highlightthickness=0,
                                      bg=self.tekhelet,
                                      fg=self.wisteria,
                                      activebackground=self.amethyst,
                                      activeforeground=self.magnolia,
                                      pady=10,
                                      padx=10,
                                      font=FONT_CHOICE,
                                      command=self.jgl_start_writing)
        self.start_button.place(relx=0.5, rely=0.75, anchor=CENTER)
    
    def jgl_start_writing(self):
        """Starts the application"""
        
        # Set game flag
        self.app_on = True
        
        self.text = ""
        self.timer = None
        
        # Disintegrate previous screen
        self.title.destroy()
        self.jgl_instructions_text.destroy()
        self.jgl_warning.destroy()
        self.start_button.destroy()
        
        self.jgl_typed_text()
        
    def jgl_typed_text(self):
        """Shows the user's typed text"""
        
        # Creates the typing area where the user types their text
        self.typing_area = tk.Text(
            font=("Helvetica Monospaced", 12, "normal"),
            bg=self.tekhelet, fg=self.amethyst,
            width=72, height=14, wrap="w",
            highlightthickness=0,
            padx=5, pady=5 
            )
        
        self.typing_area.bind("<KeyPress>", self.start_timer)
        self.typing_area.place(relx=0, rely=0.2)
                
    def start_timer(self, event):
        """
         As long as the user continues to type with breaks no 
         longer than 5-10 seconds, the application continues
        """

        if self.timer is not None:
            self.jgl_window.after_cancel(self.timer)
            
        # Use keysym to keep track of which key was pressed
        if event.keysym == "BackSpace":
            self.text = self.text[0: len(self.text) - 1]
            self.jgl_timer_countdown()
            
        elif event.char:
            # Adds typed text for display
            self.text += event.char
            self.jgl_timer_countdown()
        
    def jgl_timer_countdown(self):
        """
        Changes text color based on how long it's been since the user has typed
        """    
        self.jgl_window.after(3000, self.jgl_fade_text)
        self.timer = self.jgl_window.after(5000, self.reset_app)
        
    def reset_app(self):
        """Deletes the typed text and notifies the user"""
        
        self.typing_area.delete("1.0", "end")
        self.text = ""
        self.timer = None   
        
        self.jgl_notification = tk.Label()
        self.jgl_notification.config(
            text="The time ran out, killing your darlings!",
            font=FONT_CHOICE,
            bg=self.russian_violet, fg=self.amethyst,
        )
        self.jgl_notification.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.jgl_end_button()
        
    def jgl_fade_text(self):
        self.typing_area.configure(fg="#774eac")
        
    def jgl_end_button(self):
        
        self.end_button = tk.Button(text="Try Again",
                                      width=35,
                                      highlightthickness=0,
                                      bg=self.tekhelet,
                                      fg=self.wisteria,
                                      activebackground=self.amethyst,
                                      activeforeground=self.magnolia,
                                      pady=10,
                                      padx=10,
                                      font=FONT_CHOICE,
                                      command=self.jgl_restart_app)
        self.end_button.place(relx=0.5, rely=0.9, anchor=CENTER)
    
    def jgl_restart_app(self):
        self.typing_area.destroy()
        self.end_button.destroy()
        self.jgl_notification.destroy()
        
        self.jgl_start_page()
        
