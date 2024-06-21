"""A typing speed test that tells how long it has taken the user to 
successfully write out a string of texts"""

from text_bank import JglTexts
from ui import JglTypingUI

# Create a dictionary of possible texts 
jgl_texts = JglTexts()

# Create the GUI
jgl_ui = JglTypingUI()

# Choose a random text from the text bank
jgl_random_text = jgl_texts.jgl_random_text()
print(jgl_random_text)