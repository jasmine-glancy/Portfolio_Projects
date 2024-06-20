"""Creates the user interface for the desktop app"""


# Import libraries for GUI (TKinter)
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageDraw, ImageFont

JGL_IMAGE_FOLDER = "../pictures/coding"

class JglUserInterface():
    def __init__(self) -> None:
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Image Watermarker")
        self.jgl_window.minsize(width=755, height=375)
        self.jgl_window.config(padx=20, pady=20, background="#FFF5D6")
        self.jgl_load_logo()
        self.jgl_ask_user_for_image()
        self.jgl_ask_for_watermark()
        self.jgl_add_watermark()
        self.jgl_verify_watermark_info()
        self.jgl_window.mainloop()
        
    def jgl_load_logo(self) -> None:
        """Adds the app logo"""
        jgl_canvas = tk.Canvas(width=950, height=525, bg="#FFF5D6", highlightthickness=0)
        self.jgl_logo = tk.PhotoImage(file="D:/Work/Portfolio Projects/JGL Image Watermarking Desktop App/icon.png")
        jgl_canvas.create_image(475, 225, image=self.jgl_logo)
        jgl_canvas.grid(column=0, row=0, columnspan=4)
        
    def jgl_ask_user_for_image(self) -> None:
        """Asks user for the path to the image"""
        
        # Image path label
        jgl_image_label = tk.Label()
        jgl_image_label.config(text="Please choose an image: ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_image_label.grid(column=0, row=1)
        
        # Browsing button and notifier
        self.jgl_browsing = tk.StringVar()
        jgl_find_file_button = tk.Button(self.jgl_window,
                                         command=self.jgl_open_file,
                                         textvariable=self.jgl_browsing,
                                         font="Helvetica",
                                         bg="#968C6D",
                                         fg="#FFF5D6",
                                         width=53)
        self.jgl_browsing.set("Open File Explorer")
        jgl_find_file_button.grid(column=1, row=1, columnspan=3)
        
    def jgl_ask_for_watermark(self) -> None:
        """Ask for user's watermark preferences"""
        
        # Watermark preferences label
        jgl_watermark_label = tk.Label()
        jgl_watermark_label.config(text="Watermark Preferences", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 16, "bold"),
                               pady=10)
        jgl_watermark_label.grid(column=0, row=2, columnspan=4)
        
        # Font watermark label
        jgl_watermark_text_label = tk.Label()
        jgl_watermark_text_label.config(text="Please enter the text of your watermark: ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_watermark_text_label.grid(column=0, row=3)
        
        # Font watermark input
        self.jgl_watermark_text = tk.Entry(width=98, bg="#FFF8EB")
        self.jgl_watermark_text.grid(column=1, row=3, columnspan=3)
        
        # Font fill red value label
        jgl_font_fill_r_label = tk.Label()
        jgl_font_fill_r_label.config(text="Please enter red font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_font_fill_r_label.grid(column=0, row=5)
        
        # Font fill red value input
        self.jgl_font_fill_r_entry = tk.Entry(width=10, bg="#FFF8EB")
        self.jgl_font_fill_r_entry.grid(column=1, row=5)
        
        # Font fill green value label
        jgl_font_fill_g_label = tk.Label()
        jgl_font_fill_g_label.config(text="Please enter green font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"),
                               padx=25)
        jgl_font_fill_g_label.grid(column=2, row=5)
        
        # Font fill green value input
        self.jgl_font_fill_g_entry = tk.Entry(width=10, bg="#FFF8EB")
        self.jgl_font_fill_g_entry.grid(column=3, row=5, padx=25)
        
        # Font fill blue value label
        jgl_font_fill_b_label = tk.Label()
        jgl_font_fill_b_label.config(text="Please enter blue font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"),
                               padx=25)
        jgl_font_fill_b_label.grid(column=0, row=6)
        
        # Font fill blue value input
        self.jgl_font_fill_b_entry = tk.Entry(width=10, bg="#FFF8EB")
        self.jgl_font_fill_b_entry.grid(column=1, row=6)
        
        # Font size label
        jgl_size_label = tk.Label()
        jgl_size_label.config(text="Please enter font size (i.e. 10): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 11, "bold"))
        jgl_size_label.grid(column=2, row=6)
        
        # Font size input
        self.jgl_size_entry = tk.Entry(width=10, bg="#FFF8EB")
        self.jgl_size_entry.grid(column=3, row=6, padx=25)
    
        
    def jgl_add_watermark(self) -> None:
        """Takes info and marks it on the image the user inputs"""
        
        # Watermark Button
        jg_watermark_button = tk.Button(text="Watermark", width=35, highlightthickness=0, 
                                     bg="#968C6D", fg="#FFF8EB", pady=10, padx=10,
                                     command=self.jgl_verify_watermark_info)
        jg_watermark_button.grid(column=0, row=8, columnspan=4, pady=25)

    def jgl_verify_watermark_info(self) -> None:
        """Watermarks the image"""
        
        # Gets the data input from the form
        jgl_watermark_text = self.jgl_watermark_text.get()
        
        
        try:
            jgl_font_size = int(self.jgl_size_entry.get())
        except Exception as e:
            print(f"Please enter a size greater than 0. Exception: {e}")
            
        try:
            # Use ImageFont to specify font and font size
            jgl_font = ImageFont.truetype("arial.ttf", jgl_font_size)
            
        except Exception as e:
            print(f"Can't choose font, exception: {e}")
            
        try:
            self.jgl_color_choice = (int(self.jgl_font_fill_r_entry.get()), int(self.jgl_font_fill_g_entry.get()), int(self.jgl_font_fill_b_entry.get()))
        except Exception as e:
            print(f"Can't choose color, exception: {e}")
            
        try:
            transparent = Image.new('RGBA', self.jgl_original_image.size, (0,0,0,0))
            transparent.paste(self.jgl_original_image, (0, 0))
            transparent.paste(self.jgl_img_copy_mask, self.position, mask=self.jgl_img_copy_mask)
            transparent.show()
            
            # Use text() function of draw object

            self.jgl_drawing.text(self.position,
                            jgl_watermark_text,
                            fill=self.jgl_color_choice,
                            font=jgl_font)
            
            # Save watermarked photo
            finished_img = transparent.convert("RGB")
            jgl_watermarked_image = Image.alpha_composite(self.jgl_original_image, self.jgl_img_copy)
        except Exception as e:
            print(f"Can't watermark image, exception: {e}")
        else:
            # Shows the output
            plt.imshow(finished_img)
            
        
            
            print("Tapped!")
            print(jgl_watermark_text)   
        
            
    def jgl_open_file(self):
        """Opens file selector"""  
        
        # Opens the file browser to choose an image, suggested by Paul D Bourret on Udemy
        self.jgl_browsing.set("Searching...")
        jgl_photo_file = askopenfilename(initialdir=JGL_IMAGE_FOLDER, title="Select A File", filetype=
        (("jpeg files", "*.jpg"), ("all files", "*.*")))
        
        if jgl_photo_file:
            # If the file is found, modify it
            
            try:
                # Use image.open() for the opening of the image 
                self.jgl_original_image = Image.open(jgl_photo_file).convert("RGBA")
                
                # Opens the photo viewer
                self.jgl_original_image.show()
                    
                # Opens the image in the IDE
                plt.imshow(self.jgl_original_image)
                    
                # Make a copy of an image for the creation of the watermark image with the same dimensions as the older one
                self.jgl_img_copy = Image.new("RGBA", self.jgl_original_image.size, (255, 255, 255, 0))
                
                self.jgl_img_resize = self.jgl_img_copy.resize((round(self.jgl_original_image.size[0]*0.25), 
                                                    (round(self.jgl_original_image.size[1]*0.25))))
                self.jgl_img_copy_mask = self.jgl_img_copy.convert("RGBA")
                    
            except FileNotFoundError as jgl_not_found:
                print(f"File not found, exception: {jgl_not_found}")
            except Exception as e:
                print(f"Can't open file, exception: {e}")
            else:
                # If the image can be opened, proceed to the watermarking process
                
                
                # Set position to lower right corner, suggested by Paul D Bourret on Udemy
                self.position = (self.jgl_original_image.size[0] - self.jgl_img_resize.size[0], self.jgl_original_image.size[1] - self.jgl_img_resize.size[1])
            
                # Make the image editable using ImageDraw
                self.jgl_drawing = ImageDraw.Draw(self.jgl_img_copy)
                
                    
                
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

