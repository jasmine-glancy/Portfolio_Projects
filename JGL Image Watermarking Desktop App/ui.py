"""Creates the user interface for the desktop app"""

# Import libraries for GUI (TKinter)
import tkinter as tk

class JglUserInterface():
    def __init__(self):
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Image Watermarker")
        self.jgl_window.minsize(width=755, height=375)
        self.jgl_window.config(padx=20, pady=20, background="#FFF5D6")
        self.jgl_load_logo()
        self.jgl_ask_user_for_image()
        self.jgl_ask_for_watermark()
        self.jgl_window.mainloop()
        
    def jgl_load_logo(self):
        """Adds the app logo"""
        jgl_canvas = tk.Canvas(width=750, height=370, bg="#FFF5D6", highlightthickness=0)
        self.jgl_logo = tk.PhotoImage(file="D:/Work/Portfolio Projects/JGL Image Watermarking Desktop App/icon.png")
        jgl_canvas.create_image(375, 150, image=self.jgl_logo)
        jgl_canvas.grid(column=0, row=0, columnspan=4)
        
    def jgl_ask_user_for_image(self):
        """Asks user for the path to the image"""
        
        # Image path label
        jgl_image_label = tk.Label()
        jgl_image_label.config(text="Image Location (i.e. /pictures/pathway.png): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_image_label.grid(column=0, row=1)
        
        # Image path input
        jgl_image_path_entry = tk.Entry(width=35, bg="#FFF8EB")
        jgl_image_path_entry.grid(column=1, row=1, columnspan=2)
        
    def jgl_ask_for_watermark(self):
        """Ask for user's watermark preferences"""
        
        # Watermark preferences label
        jgl_watermark_label = tk.Label()
        jgl_watermark_label.config(text="Watermark Preferences", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 16, "bold"),
                               pady=10)
        jgl_watermark_label.grid(column=0, row=2)
        
        # Font type label
        jgl_font_label = tk.Label()
        jgl_font_label.config(text="Please choose a font type (i.e. Helvetica): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_font_label.grid(column=0, row=3)
        
        # Font type input
        jgl_font_entry = tk.Entry(width=35, bg="#FFF8EB")
        jgl_font_entry.grid(column=1, row=3, columnspan=2)
        
        # Font size label
        jgl_size_label = tk.Label()
        jgl_size_label.config(text="Please enter font size (i.e. 12): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_size_label.grid(column=0, row=4)
        
        # Font size input
        jgl_size_entry = tk.Entry(width=35, bg="#FFF8EB")
        jgl_size_entry.grid(column=1, row=4, columnspan=2)
        
        # Font style label
        jgl_style_label = tk.Label()
        jgl_style_label.config(text="Please enter font style (i.e. bold, normal, italic): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_style_label.grid(column=0, row=5)
        
        # Font style input
        jgl_style_entry = tk.Entry(width=35, bg="#FFF8EB")
        jgl_style_entry.grid(column=1, row=5, columnspan=2)
        
        # Add Button
        jg_upload_button = tk.Button(text="Watermark", width=35, highlightthickness=0, 
                                     bg="#968C6D", fg="#FFF8EB", pady=10, padx=10)
        jg_upload_button.grid(column=0, row=6, columnspan=4, pady=25)

        
    
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

