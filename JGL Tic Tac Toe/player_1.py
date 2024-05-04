"""Responsible for the user's choices and coding"""

from gameplay import JglTicTacToe


class JglPlayer1():
    def __init__(self):
        """Loads game board"""
        
        self.jgl_game = JglTicTacToe()
        self.jgl_user_symbol = None
        
    def jgl_assign_user_symbol(self):
        """Asks user to choose a symbol"""
        
        if self.jgl_user_symbol is None:
            # Only asks for input if it isn't already set yet
            self.jgl_user_symbol = input("Please choose your preferred symbol for this game. Xs or Os?: ").upper()
    
        # Verifies symbol as an option
        if self.jgl_user_symbol != "X" and self.jgl_user_symbol !="O":
            print("Please choose a valid symbol.")
            return self.jgl_assign_user_symbol()
        
        return self.jgl_user_symbol
    

    def jgl_box_mark(self):
        """Ask user to place their sign in the available empty boxes"""
        
        self.jgl_row_user_mark = int(input(
            "Please enter where you want to mark to go by entering the row number (0-2): "
            ))
        
        if self.jgl_row_user_mark < 0 or self.jgl_row_user_mark > 2:
            print("Please enter a number between 0 and 2.")
            return self.jgl_box_mark()
            
        self.jgl_column_user_mark = int(input(
            "Please enter where you want to mark to go by entering the column number (0-2): "
            ))
        
        if self.jgl_column_user_mark < 0 or self.jgl_column_user_mark > 2:
            print("Please enter a number between 0 and 2.")
            return self.jgl_box_mark()
        
        self.jgl_game.jgl_game_board[self.jgl_row_user_mark][self.jgl_column_user_mark] = f"_{self.jgl_user_symbol}_"
