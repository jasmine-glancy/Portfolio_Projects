"""Creates the user interface for the desktop app"""


# Import libraries for GUI (TKinter)
import ctypes
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.constants import CENTER
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageDraw, ImageFont, ImageTk

JGL_IMAGE_FOLDER = "../pictures/coding"

# Suggested by ThePythonCode.Com for a sharper window
# (https://thepythoncode.com/article/how-to-make-typing-speed-tester-in-python-using-tkinter)
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class JglUserInterface():
    def __init__(self) -> None:
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Image Watermarker")
        self.jgl_window.minsize(width=1200, height=900)
        self.jgl_window.geometry("1200x900")
        self.jgl_window.config(padx=20, pady=20, background="#FFF5D6")
        self.jgl_load_logo()
        self.jgl_load_placeholder()
        self.jgl_ask_user_for_image()
        self.jgl_ask_for_watermark()
        self.jgl_window.mainloop()
        
    def jgl_load_logo(self) -> None:
        """Adds the app logo"""
        jgl_canvas = tk.Canvas(width=475, height=250, bg="#FFF5D6", highlightthickness=0)
        self.jgl_logo = tk.PhotoImage(file="D:/Work/Portfolio Projects/JGL Image Watermarking Desktop App/icon.png")
        jgl_canvas.create_image(225, 125, image=self.jgl_logo)
        jgl_canvas.place(relx=0.25, rely=0.18, anchor=CENTER)
        
    def jgl_load_placeholder(self) -> None:
        """Loads in an invisible photo that will be replaced with the new watermarked image"""
        
        jgl_placeholder = ImageTk.PhotoImage(file="D:/Work/Portfolio Projects/JGL Image Watermarking Desktop App/placeholder.png")
        self.panel = tk.Label(self.jgl_window, image=jgl_placeholder, highlightthickness=0)
        
        # Keeps a reference
        self.panel.image = jgl_placeholder
        self.panel.place(relx=0.5, rely=0.7, anchor=CENTER)
        
        
    def jgl_ask_user_for_image(self) -> None:
        """Asks user for the path to the image"""
        
        # Image path label
        jgl_image_label = tk.Label()
        jgl_image_label.config(text="Please choose an image: ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_image_label.place(relx=0.55, rely=0.06, anchor=CENTER)
        
        # Browsing button and notifier
        self.jgl_browsing = tk.StringVar()
        jgl_find_file_button = tk.Button(self.jgl_window,
                                         command=self.jgl_open_file,
                                         textvariable=self.jgl_browsing,
                                         font="Helvetica",
                                         bg="#968C6D",
                                         fg="#FFF5D6",
                                         width=35)
        self.jgl_browsing.set("Open File Explorer")
        jgl_find_file_button.place(relx=0.8, rely=0.06, anchor=CENTER)
        
    def jgl_ask_for_watermark(self) -> None:
        """Ask for user's watermark preferences"""
        
        # Watermark preferences label
        jgl_watermark_label = tk.Label()
        jgl_watermark_label.config(text="Watermark Preferences", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 16, "bold"),
                               pady=10)
        jgl_watermark_label.place(relx=0.725, rely=0.12, anchor=CENTER)
        
        # Font watermark label
        jgl_watermark_text_label = tk.Label()
        jgl_watermark_text_label.config(text="Please enter the text of your watermark: ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_watermark_text_label.place(relx=0.6, rely=0.18, anchor=CENTER)
        
        # Font watermark input
        self.jgl_watermark_text = tk.Entry(width=39, bg="#FFF8EB")
        self.jgl_watermark_text.place(relx=0.84, rely=0.18, anchor=CENTER)
        
        # Font fill red value label
        jgl_font_fill_r_label = tk.Label()
        jgl_font_fill_r_label.config(text="Please enter red font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"),
                               wraplength=225)
        jgl_font_fill_r_label.place(relx=0.55, rely=0.23, anchor=CENTER)
        
        # Font fill red value input
        self.jgl_font_fill_r_entry = tk.Entry(width=10, bg="#FFF8EB")
        self.jgl_font_fill_r_entry.place(relx=0.67, rely=0.23, anchor=CENTER)
        
        # Font fill green value label
        jgl_font_fill_g_label = tk.Label()
        jgl_font_fill_g_label.config(text="Please enter green font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"),
                               wraplength=225)
        jgl_font_fill_g_label.place(relx=0.795, rely=0.23, anchor=CENTER)
        
        # Font fill green value input
        self.jgl_font_fill_g_entry = tk.Entry(width=10, bg="#FFF8EB")
        self.jgl_font_fill_g_entry.place(relx=0.915, rely=0.23, anchor=CENTER)
        
        # Font fill blue value label
        jgl_font_fill_b_label = tk.Label()
        jgl_font_fill_b_label.config(text="Please enter blue font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"),
                               wraplength=225)
        jgl_font_fill_b_label.place(relx=0.55, rely=0.288, anchor=CENTER)
        
        # Font fill blue value input
        self.jgl_font_fill_b_entry = tk.Entry(width=10, bg="#FFF8EB")
        self.jgl_font_fill_b_entry.place(relx=0.67, rely=0.288, anchor=CENTER)
        
        # Font size label
        jgl_size_label = tk.Label()
        jgl_size_label.config(text="Please enter font size (i.e. 10): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 11, "bold"),
                               wraplength=125)
        jgl_size_label.place(relx=0.765, rely=0.288, anchor=CENTER)
        
        # Font size input
        self.jgl_size_entry = tk.Entry(width=20, bg="#FFF8EB")
        self.jgl_size_entry.place(relx=0.89, rely=0.288, anchor=CENTER)
        
        # Watermark Button
        self.jg_watermark_button = tk.Button(text="Watermark", width=35, highlightthickness=0, 
                                        bg="#968C6D", fg="#FFF8EB", pady=10, padx=10,
                                        command=self.jgl_watermark_image,
                                        font="Helvetica")
        self.jg_watermark_button.place(relx=0.5, rely=0.4, anchor=CENTER)
    
        
    def jgl_watermark_image(self) -> None:
        """Watermarks the image"""
    
        if self.jgl_verify_watermark_info():
            try:
                # Use image.open() for the opening of the image 
                with Image.open(self.jgl_original_image).convert("RGBA") as jgl_main_img:
                
                    # Make a copy of an image for the creation of the watermark image with the same dimensions as the older one
                    self.jgl_img_copy = Image.new("RGBA", jgl_main_img.size, (255, 255, 255, 0))
                    
                    # Use ImageFont to specify font and font size
                    self.jgl_font = ImageFont.truetype("arial.ttf", self.jgl_font_size)
                    

                    self.jgl_browsing.set("Image Found!")
                    
                    # Make the image editable using ImageDraw
                    self.jgl_drawing = ImageDraw.Draw(self.jgl_img_copy)
                    
                    # Draw text
                    self.jgl_drawing.text((self.jgl_halved_width, self.jgl_halved_height),
                                    self.jgl_text,
                                    fill=self.jgl_color_choice,
                                    font=self.jgl_font)
                    
                    # Show watermarked photo
                    jgl_output = Image.alpha_composite(jgl_main_img, self.jgl_img_copy)
                    jgl_resize_marked_image = jgl_output.convert("RGBA")
                    jgl_watermarked_image = self.jgl_resize_image(jgl_resize_marked_image)
                    self.panel.configure(image=jgl_watermarked_image)
                    self.panel.image = jgl_watermarked_image
                    self.panel.place(relx=0.5, rely=0.7, anchor=CENTER)
                    plt.imshow(jgl_watermarked_image)
            except Exception as e:
                print(f"Can't watermark image, exception: {e}")
            else:
                # Shows the output
                plt.imshow(jgl_watermarked_image)
        else:
            print("Can't watermark image, information not verified")
            
    def jgl_open_file(self):
        """Opens file selector"""  
        
        # Opens the file browser to choose an image, suggested by Paul D Bourret on Udemy
        self.jgl_browsing.set("Searching...")
        jgl_photo_file = askopenfilename(initialdir=JGL_IMAGE_FOLDER, title="Select A File", filetype=
        (("jpeg files", "*.jpg"), ("all files", "*.*")))
        
        if jgl_photo_file:
            # If the file is found, save modify it
            
            try:
                self.jgl_original_image = Image.open(jgl_photo_file).convert("RGBA")
                self.jgl_show_image(jgl_photo_file)
                    
            except FileNotFoundError as jgl_not_found:
                print(f"File not found, exception: {jgl_not_found}")
            except Exception as e:
                print(f"Can't open file, exception: {e}")
                self.jgl_browsing.set("Couldn't Open File!")
    
    def jgl_show_image(self, jgl_file) -> None:
        """Handles the user interaction and GUI updates to adjust image size"""   
            
        if self.jgl_verify_watermark_info:
            # Opens the original image 
            jgl_image = (Image.open(jgl_file))
            
            # Sets the width and the height
            self.jgl_orig_width, self.jgl_orig_height = jgl_image.size[0], jgl_image.size[1]
                
            jgl_resize_image = self.jgl_resize_image(jgl_image)
                
            # Displays the image
            self.panel.configure(image=jgl_resize_image)
            self.panel.image = jgl_resize_image
            self.jgl_halved_height = self.jgl_orig_height / 2
            self.jgl_halved_width = self.jgl_orig_width / 2
        else:
            # If image can't be verified, give error
            print("Image can't be shown.")
        
     
    def jgl_verify_watermark_info(self) -> bool:
        """Verifies info before trying to watermark the image"""
        
        self.jg_watermark_button.set("Watermarking...")
        
        # Gets the data input from the form
        self.jgl_text = self.jgl_watermark_text.get()
        
        
        try:
            self.jgl_font_size = int(self.jgl_size_entry.get())
            
            jgl_r = int(self.jgl_font_fill_r_entry.get())
            jgl_g = int(self.jgl_font_fill_g_entry.get())
            jgl_b = int(self.jgl_font_fill_b_entry.get())
            
            print(jgl_r, jgl_g, jgl_b) 
            self.jgl_color_choice = (jgl_r, jgl_g, jgl_b)
            print(self.jgl_color_choice)
            
        except Exception as e:
            print(f"Can't verify info, exception: {e}") 
            return False

        else:
            # If no errors, return True
            return True
                   
    def jgl_resize_image(self, jgl_file) -> None:
        """Resizes the original image to improve user experience, watermark consistency,
        performance, and memory management"""  
        jgl_size = jgl_file.size
        jgl_full_size = (600, 400)  
        
        # Allows the image to maintain its aspect ratio, recommended by Martyna Boradyn on Udemy 
        # https://www.udemy.com/user/martyna-boradyn/     
        jgl_scaling_factor = min(float(jgl_full_size[1]) / jgl_size[1], float(jgl_full_size[0]) / jgl_size[0])
        jgl_scaled_width = int(jgl_size[0] * jgl_scaling_factor)
        jgl_scaled_height = int(jgl_size[1] * jgl_scaling_factor)
        
        # Resize image using Image.LANCZOS to preserve quality
        self.jgl_resized_image = self.jgl_original_image.resize((jgl_scaled_width, jgl_scaled_height), Image.LANCZOS)
                
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

