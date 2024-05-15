"""A text-based tic tac toe game!"""

from player_1 import JglPlayer1
from player_2 import JglPlayer2
from gameplay import JglTicTacToe

# Two players, x and o

# There's a board with 9 boxes +/- nested array?

print("Welcome to Text-Based Tic Tac Toe! Try to beat the computer. ✗ ❤︎ 0")

# Print game board
jgl_game = JglTicTacToe()
jgl_game.jgl_print_board()

# Ask user to choose a symbol and verify it
jgl_player_1 = JglPlayer1(jgl_game)

# Assign the computer's symbol
jgl_player_2 = JglPlayer2(jgl_game, jgl_player_1)
jgl_player_2.jgl_computer_symbol()

# Mark the boxes
jgl_player_1.jgl_box_mark()

# Print board again
jgl_game.jgl_print_board()

# Computer picks a mark
jgl_player_2.jgl_computer_mark()
jgl_game.jgl_print_board()
# TODO: If the current player won the game, then print a winning message and break the infinite loop.


# Goal is to place respective signs completely row-wise, column-wise, or diagonally

# TODO: Game continues until it ends in a draw or a win
    # It's a draw if all the boxes are filled without either player getting a winning match
    
    # TODO: If the board is filled, then print the draw message and break the infinite loop.

    # TODO: Finally, show the user the final view of the board.