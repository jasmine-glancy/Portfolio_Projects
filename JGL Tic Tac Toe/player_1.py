"""Responsible for the user's choices and coding"""


class JglPlayer1():
    """Asks for user's preferred symbol and verifies it as an option"""
    def __init__(self):
        self.jgl_user_symbol = input("Please choose your preferred symbol for this game. Xs or Os?: ").upper()
    
    def jgl_check_symbol(self):
        if self.jgl_user_symbol != "X" and self.jgl_user_symbol !="O":
            print("Please choose a valid symbol.")
        else:
            print(f"Player 1 is {self.jgl_user_symbol}s!")
            
        return self.jgl_user_symbol

# TODO: Ask user to place their sign in the available empty boxes
