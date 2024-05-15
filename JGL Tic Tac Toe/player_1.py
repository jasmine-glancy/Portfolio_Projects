"""Responsible for the user's choices and coding"""

from gameplay import JglTicTacToe

class JglPlayer1():
    def __init__(self, jgl_game):
        """Loads game board"""
        
        self.jgl_user_symbol = None
        self.jgl_game = jgl_game
        self.jgl_assign_user_symbol()
        
    def jgl_assign_user_symbol(self):
        """Asks user to choose a symbol"""
        
        while self.jgl_user_symbol is None or (self.jgl_user_symbol != "X" and self.jgl_user_symbol !="O"):
            # Only asks for input if it isn't already set yet
            self.jgl_user_symbol = input("Please choose your preferred symbol for this game. Xs or Os?: ").upper()
    
            # Verifies symbol as an option
            if self.jgl_user_symbol != "X" and self.jgl_user_symbol !="O":
                print("Please choose a valid symbol.")
            else:
                break
        
        return self.jgl_user_symbol
    

    def jgl_box_mark(self):
        """Ask user to place their sign in the available empty boxes"""
        
        self.jgl_user_mark = int(input(
            "Please enter where you want to mark to go by entering the box number (0-8): "
            ))
        
        if self.jgl_user_mark < 0 or self.jgl_user_mark > 8:
            print("Please enter a number between 0 and 8.")
            return self.jgl_box_mark()
        
        
        # Line suggested by CoPilot
        jgl_key = self.jgl_user_mark
        
        self.jgl_game.jgl_game_board[jgl_key] = f"_{self.jgl_user_symbol}_"
