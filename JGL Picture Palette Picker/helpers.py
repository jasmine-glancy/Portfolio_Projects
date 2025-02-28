import tkinter as tk
from tkinter.constants import CENTER

def upload_files():
    """Allow the user to upload an image"""

    choose_image_label = tk.Label()
    choose_image_label.config(text="Please choose an image:",
                              font=("Helvetica", 12, "bold"))
    choose_image_label.place(relx=0.3, rely=0.2, anchor=CENTER)