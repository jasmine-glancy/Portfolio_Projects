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

# Pre-determine winning combinations for faster checks
jgl_winning_combos = jgl_game.jgl_winning_combos()

# Load in empty boxes
jgl_empty_boxes = jgl_game.jgl_empty_boxes

# Ask user to choose a symbol and verify it
jgl_player_1 = JglPlayer1(jgl_game, jgl_empty_boxes)

# Assign the computer's symbol
jgl_player_2 = JglPlayer2(jgl_game, jgl_player_1, jgl_winning_combos, jgl_empty_boxes)
jgl_player_2.jgl_computer_symbol()

# Winner found
winner_found = jgl_game.jgl_check_for_wins()
while jgl_game.jgl_is_board_filled != False or winner_found == False:
    
    
    # Mark the boxes
    jgl_player_1.jgl_box_mark(jgl_empty_boxes)
    jgl_game.jgl_check_for_wins()

    # Print board and update winning combinations
    jgl_game.jgl_print_board()
    jgl_game.jgl_check_for_wins()

    # Computer picks a mark
    jgl_player_2.jgl_computer_choice(jgl_winning_combos, jgl_empty_boxes)
    jgl_game.jgl_print_board()
    jgl_game.jgl_check_for_wins()
# TODO: If the current player won the game, then print a winning message and break the infinite loop.


# Goal is to place respective signs completely row-wise, column-wise, or diagonally

# TODO: Game continues until it ends in a draw or a win
    # It's a draw if all the boxes are filled without either player getting a winning match
    
    # TODO: If the board is filled, then print the draw message and break the infinite loop.

    # TODO: Finally, show the user the final view of the board.