"""A text-based tic tac toe game!"""

from player_1 import JglPlayer1
from player_2 import JglPlayer2
from gameplay import JglTicTacToe

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
board_filled = jgl_game.jgl_is_board_filled()

# print(winner_found, board_filled)
while not board_filled and not winner_found: 
    
    # Mark the boxes
    jgl_player_1.jgl_box_mark(jgl_empty_boxes)
    winner_found = jgl_game.jgl_check_for_wins()

    # Print board and update winning combinations
    jgl_game.jgl_print_board()
    winner_found = jgl_game.jgl_check_for_wins() 
    board_filled = jgl_game.jgl_is_board_filled()
    
    if winner_found:
        break
    elif board_filled:
        print("It's a draw!")
        break
    
    # Computer picks a mark
    jgl_player_2.jgl_computer_choice(jgl_winning_combos, jgl_empty_boxes)
    jgl_game.jgl_print_board()
    winner_found = jgl_game.jgl_check_for_wins() 
    board_filled = jgl_game.jgl_is_board_filled()
    
    if winner_found:
        break
    elif board_filled:
        print("It's a draw!")
        break