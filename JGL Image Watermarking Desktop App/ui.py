"""Creates the user interface for the desktop app"""

# TODO: Import libraries for GUI (TKinter)
import tkinter as tk

class JglUserInterface():
    def __init__(self):
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Image Watermarker")
        self.jgl_window.minsize(width=500, height=500)
        self.jgl_window.config(padx=20, pady=20)
        self.jgl_window.mainloop()
        
#-------------- Step 2: Setting up widgets -------------------- 
# TODO: Use the canvas widget to create a background. 
# TODO: Set up its size equal to the image dimensions. 
# TODO: Create a usable image using PhotoImage() 
# TODO: Use create_image and create_text to display an image and text for good UI. 
# TODO: Create an input field and two buttons for uploading images and submit button. 
# TODO: (hint) Use grid layout to display widgets in a systematic matter. 

#------------ Step 3: Define methods of buttons ----------------
# TODO: Define a method for the Upload button
# TODO: use filedialog.askopenfilename method of tkinter to open a dialogue box to ask the user to upload the file
# TODO: we save its name and display the name on the screen and make Upload button text green to show the file as uploaded
# TODO: Save the uploaded file path in a global variable that is passed to the method of the submit button

