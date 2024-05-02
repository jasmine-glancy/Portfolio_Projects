"""Responsible for the gameplay"""

class JglTicTacToe():
    def __init__(self):
        """Creates a 3x3 board using 2-d array and initialize each element as empty"""
        self.jgl_rows, self.jgl_columns = (3, 3)
        self.jgl_game_board = [["___" for jgl_col in range(self.jgl_columns)] for jgl_row in range(self.jgl_rows)]
        
    def jgl_print_board(self):
        """Prints the game board"""
        for jgl_row in self.jgl_game_board:
            print(jgl_row)
        
        # TODO: Write a new function to check if the board is filed or not
            # TODO: Iterate over the board and return false if the board has an empty sign
            
        # TODO: Write a new function to check whether a player has won or not 
            # TODO: Check for all the rows, columns, and the two diagonals
            
        # TODO: Show the board every time a new move is made by someone
        