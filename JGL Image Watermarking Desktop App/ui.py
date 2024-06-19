"""Creates the user interface for the desktop app"""


# Import libraries for GUI (TKinter)
import tkinter as tk
from PIL import Image

    
class JglUserInterface():
    def __init__(self):
        self.jgl_window = tk.Tk()
        self.jgl_window.title("Image Watermarker")
        self.jgl_window.minsize(width=755, height=375)
        self.jgl_window.config(padx=20, pady=20, background="#FFF5D6")
        self.jgl_load_logo()
        self.jgl_ask_user_for_image()
        self.jgl_ask_for_watermark()
        self.jgl_add_watermark()
        self.jgl_window.mainloop()
        
    def jgl_load_logo(self):
        """Adds the app logo"""
        jgl_canvas = tk.Canvas(width=950, height=525, bg="#FFF5D6", highlightthickness=0)
        self.jgl_logo = tk.PhotoImage(file="D:/Work/Portfolio Projects/JGL Image Watermarking Desktop App/icon.png")
        jgl_canvas.create_image(475, 225, image=self.jgl_logo)
        jgl_canvas.grid(column=0, row=0, columnspan=4)
        
    def jgl_ask_user_for_image(self):
        """Asks user for the path to the image"""
        
        # Image path label
        jgl_image_label = tk.Label()
        jgl_image_label.config(text="Image name (i.e. file.png): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_image_label.grid(column=0, row=1)
        
        # Image path input
        self.jgl_image_path_entry = tk.Entry(width=35, bg="#FFF8EB")
        self.jgl_image_path_entry.grid(column=1, row=1, columnspan=2)
        
        
    def jgl_ask_for_watermark(self):
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
        jgl_watermark_text = tk.Entry(width=98, bg="#FFF8EB")
        jgl_watermark_text.grid(column=1, row=3, columnspan=3)
        
        # Font X-coordinate label
        jgl_font_xcord_label = tk.Label()
        jgl_font_xcord_label.config(text="Please enter the x-coordinate of the text: ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_font_xcord_label.grid(column=0, row=4)
        
        # Font X-coordinate input
        jgl_font_xcord_entry = tk.Entry(width=10, bg="#FFF8EB")
        jgl_font_xcord_entry.grid(column=1, row=4)
        
        # Font Y-coordinate label
        jgl_font_ycord_label = tk.Label()
        jgl_font_ycord_label.config(text="Please enter the y-coordinate of the text: ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"),
                               padx=25)
        jgl_font_ycord_label.grid(column=2, row=4)
        
        # Font Y-coordinate input
        jgl_font_ycord_entry = tk.Entry(width=10, bg="#FFF8EB")
        jgl_font_ycord_entry.grid(column=3, row=4, padx=25)
        
        # Font fill red value label
        jgl_font_fill_r_label = tk.Label()
        jgl_font_fill_r_label.config(text="Please enter red font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"))
        jgl_font_fill_r_label.grid(column=0, row=5)
        
        # Font fill red value input
        jgl_font_fill_r_entry = tk.Entry(width=10, bg="#FFF8EB")
        jgl_font_fill_r_entry.grid(column=1, row=5)
        
        # Font fill green value label
        jgl_font_fill_g_label = tk.Label()
        jgl_font_fill_g_label.config(text="Please enter green font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"),
                               padx=25)
        jgl_font_fill_g_label.grid(column=2, row=5)
        
        # Font fill green value input
        jgl_font_fill_g_entry = tk.Entry(width=10, bg="#FFF8EB")
        jgl_font_fill_g_entry.grid(column=3, row=5, padx=25)
        
        # Font fill blue value label
        jgl_font_fill_b_label = tk.Label()
        jgl_font_fill_b_label.config(text="Please enter blue font fill value (between 0 and 255): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 12, "bold"),
                               padx=25)
        jgl_font_fill_b_label.grid(column=0, row=6)
        
        # Font fill blue value input
        jgl_font_fill_b_entry = tk.Entry(width=10, bg="#FFF8EB")
        jgl_font_fill_b_entry.grid(column=1, row=6)
        
        # Font style label
        jgl_style_label = tk.Label()
        jgl_style_label.config(text="Please enter font size (i.e. 10): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 11, "bold"))
        jgl_style_label.grid(column=2, row=6)
        
        # Font style input
        jgl_style_entry = tk.Entry(width=10, bg="#FFF8EB")
        jgl_style_entry.grid(column=3, row=6, padx=25)
        
        # Font anchor label
        jgl_anchor_label = tk.Label()
        jgl_anchor_label.config(text="Please enter font anchor (i.e. lt for vertical, la for horizontal): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 11, "bold"))
        jgl_anchor_label.grid(column=0, row=7)
        
        # Font anchor input
        jgl_anchor_entry = tk.Entry(width=10, bg="#FFF8EB")
        jgl_anchor_entry.grid(column=1, row=7, padx=25)
        
        # Font alignment label
        jgl_anchor_label = tk.Label()
        jgl_anchor_label.config(text="Please enter font alignment (i.e. center, left, right): ", 
                               bg="#FFF5D6", 
                               fg="#968C6D",
                               font=("Helvetica", 11, "bold"))
        jgl_anchor_label.grid(column=2, row=7)
        
        # Font alignment input
        jgl_anchor_entry = tk.Entry(width=10, bg="#FFF8EB")
        jgl_anchor_entry.grid(column=3, row=7, padx=25)
        
    def jgl_add_watermark(self):
        """Takes info and marks it on the image the user inputs"""
        
        # Watermark Button
        jg_watermark_button = tk.Button(text="Watermark", width=35, highlightthickness=0, 
                                     bg="#968C6D", fg="#FFF8EB", pady=10, padx=10,
                                     command=self.jgl_watermark)
        jg_watermark_button.grid(column=0, row=8, columnspan=4, pady=25)

    def jgl_watermark(self):
        """Watermarks the image"""
        jgl_image_to_mark = self.jgl_image_path_entry.get()
        print("Tapped!")
        print(jgl_image_to_mark)   
        
        #------------  Watermark Image & Saving it ----------------

        try:
            # 2. Use image.open() for the opening of the image 
            with Image.open(jgl_image_to_mark) as jgl_img:
                # Opens the photo viewer
                jgl_img.show()
        except FileNotFoundError as jgl_not_found:
            print(f"File not found, exception: {jgl_not_found}")
        except Exception as e:
            print(f"Can't open file, exception: {e}")

        # TODO: 3. plt.imshow() is used to open the image in the IDE

        # TODO: 4. Make a copy of an image for the creation of the watermark image with the same dimensions as the older one

        # TODO: 5. Make the image editable using ImageDraw

        # TODO: 6. Use ImageFont to specify font and font size

        # TODO: 7. Create a draw method of ImageDraw module and pass the image as a parameter in the function

        # TODO: 8. Create a Font using ImageFont module function truetypel() as it neads two parameters
            # i.e. ("font type", size)
            
        # TODO: 9. Then use text() function of draw object and pass the 4 parameters
            # the 4 parameters should be (point of starting for text, "sample text", Color, ImageFont object)
            
        # TODO: 10. plt.Imshow(watermark_image) for the output
    
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

