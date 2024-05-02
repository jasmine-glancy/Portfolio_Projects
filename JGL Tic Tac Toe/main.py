"""A text-based tic tac toe game!"""

from player_1 import JglPlayer1
from player_2 import JglPlayer2

# Two players, x and o

# There's a board with 9 boxes +/- nested array?

print("Welcome to Text-Based Tic Tac Toe! Try to beat the computer. ✗ ❤︎ 0")

jgl_player_1 = JglPlayer1()
jgl_player_1.jgl_check_symbol()

# Goal is to place respective signs completely row-wise, column-wise, or diagonally

# TODO: Game continues until it ends in a draw or a win
    # It's a draw if all the boxes are filled without either player getting a winning match