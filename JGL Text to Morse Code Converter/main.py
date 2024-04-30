from morse import jgl_morse_dict # Import morse code

"""A text-based Python program to convert Strings into Morse Code"""

def jgl_welcome():
    '''Welcomes the user'''
    print("Welcome to the Morse Code Converter!\n",
          "I'll take your phrase and present you with something telegraph-worthy!")

def jgl_message_to_morse(jgl_user_message):
    '''Converts a message into morse code using the dictionary as a reference'''
    
    jgl_ciphertext = ""
    for char in jgl_user_message.upper():
        if char in jgl_morse_dict:
            jgl_ciphertext += jgl_morse_dict[char] 
    return jgl_ciphertext
    
            
jgl_welcome()

# Ask user for some input
jgl_user_message = input("Enter your message: ")

# Returns the original message and the ciphertext
print(f"Original message: {jgl_user_message}\n",
      f"Message to morse: {jgl_message_to_morse(jgl_user_message)}")

