"""Responsible for the CPU's choices and coding"""

from gameplay import JglTicTacToe
from player_1 import JglPlayer1
import random


class JglPlayer2():
    def __init__(self, ):
        """Loads in player 1 and game board"""
        
        self.jgl_player_1 = JglPlayer1()
        self.jgl_game = JglTicTacToe()
    
    def jgl_computer_symbol(self):
        """Checks the user's chosen symbol and then assigns the opposite to the computer"""
        
        self.jgl_user_symbol = self.jgl_player_1.jgl_assign_user_symbol()
        
        if self.jgl_user_symbol == "X":
            self.jgl_cpu_symbol = "O"
        
        if self.jgl_user_symbol == "O":
            self.jgl_cpu_symbol = "X"
        
        print(f"Player 1 is {self.jgl_user_symbol}s!\n", f"Player 2 is {self.jgl_cpu_symbol}s!")
        return self.jgl_cpu_symbol
            
    def jgl_computer_mark(self):
        """Computer chooses the next move based on the available slots on the game board"""
        self.jgl_possible_rows = [0, 1, 2]
        self.jgl_possible_columns = [0, 1, 2]
        
        
        # Assign variable for readability
        jgl_board = self.jgl_game.jgl_game_board
        
        jgl_winning_combos = [
            [jgl_board["1"], jgl_board["2"], jgl_board["3"]], # Row 1
            [jgl_board["4"], jgl_board["5"], jgl_board["9"]], # Row 2
            [jgl_board["7"], jgl_board["8"], jgl_board["9"]], # Row 3
            [jgl_board["3"], jgl_board["5"], jgl_board["7"]], # Right diagonal
            [jgl_board["1"], jgl_board["5"], jgl_board["9"]], # Left diagonal
            [jgl_board["1"], jgl_board["4"], jgl_board["7"]], # Column 1
            [jgl_board["2"], jgl_board["5"], jgl_board["8"]], # Column 2
            [jgl_board["3"], jgl_board["6"], jgl_board["9"]] # Column 3
            ]
        
        for combination in jgl_winning_combos:
            # Checks if all the elements in combination are the same. count() counts how many times the 
            # first element appears in comvination. If the count is equal to the length, all elements are the same
            if combination.count(combination[0]) == len(combination) and combination[0] != "___":
                # 
                return
                
            
        # TODO: Second player chooses a sign from an available empty box
            # TODO: If no move will automatically win the game, computer chooses randomly from the "empty" boxes
            # otherwise the computer will choose the box that is most likely to win the game
            # TODO: If the user is likely to win next turn, prioritize that box
        
        # TODO: Keep in mind the list of computer priorities, in order:
            # Win: If there's a move that will allow the computer to win the game, it should take it.

            # Block: If the opponent has two in a row, the computer should play the third to block the opponent.

            # Fork: This is a move that creates an opportunity where the computer has two threats to win (two non-blocked lines of 2).

            # Block Opponent's Fork: The player should block the opponent's fork opportunities.

            # Center: If the center square is free, the computer should take it. This is often a good move because it gives the most opportunities for making three in a row.

            # Opposite Corner: If the opponent is in the corner, the computer should play the opposite corner.

            # Empty Corner: The computer should take an empty corner if available.

            # Empty Side: The computer should take an empty side if available.
            