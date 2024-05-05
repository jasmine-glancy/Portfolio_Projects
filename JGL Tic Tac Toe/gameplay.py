"""Responsible for the gameplay"""

class JglTicTacToe():
    def __init__(self):
        """Creates a 3x3 board using a dictionary and initialize each element as empty"""
        self.jgl_rows, self.jgl_columns = (3, 3)
        self.jgl_game_board = {'1': '___', '2': '___', '3': '___',
                               '4': '___', '5': '___', '6': '___',
                               '7': '___', '8': '___', '9': '___',}
        
    def jgl_print_board(self):
        """Prints the game board"""
        print(" _________________ ")
        print("|", self.jgl_game_board["1"], "|", self.jgl_game_board["2"], "|", self.jgl_game_board["3"], "|")
        print("|", self.jgl_game_board["4"], "|", self.jgl_game_board["5"], "|", self.jgl_game_board["6"], "|")
        print("|", self.jgl_game_board["7"], "|", self.jgl_game_board["8"], "|", self.jgl_game_board["9"], "|")
        print(" ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")

        # TODO: Write a new function to check if the board is filed or not
            # TODO: Iterate over the board and return false if the board has an empty sign
            
        # TODO: Write a new function to check whether a player has won or not 
            # TODO: Check for all the rows, columns, and the two diagonals
            
        # TODO: Show the board every time a new move is made by someone
        