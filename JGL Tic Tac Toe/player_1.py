"""Responsible for the user's choices and coding"""

from gameplay import JglTicTacToe

jgl_game = JglTicTacToe()

class JglPlayer1():
    def __init__(self, jgl_game):
        """Asks for user's preferred symbol"""
        self.jgl_user_symbol = input("Please choose your preferred symbol for this game. Xs or Os?: ").upper()
        self.jgl_game = jgl_game
    
    def jgl_check_symbol(self):
        """Verifies symbol as an option"""
        if self.jgl_user_symbol != "X" and self.jgl_user_symbol !="O":
            print("Please choose a valid symbol.")
        else:
            print(f"Player 1 is {self.jgl_user_symbol}s!")
            
        return self.jgl_user_symbol
    
    def jgl_box_mark(self):
        """Ask user to place their sign in the available empty boxes"""
        self.jgl_row_user_mark = int(input(
            "Please enter where you want to mark to go by entering the row number (0-2): "
            ))
        self.jgl_column_user_mark = int(input(
            "Please enter where you want to mark to go by entering the column number (0-2): "
            ))
        self.jgl_game.jgl_game_board[self.jgl_row_user_mark][self.jgl_column_user_mark] = f"_{self.jgl_user_symbol}_"
