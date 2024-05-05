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
        
        for i in range(jgl_board):
            pass
                # Chooses the box in the middle if the cpu marked the left and right box
                        
                # print("Imminent user win detected!")
                # self.jgl_game.jgl_game_board[i][1] = f"_{self.jgl_cpu_symbol}_"
                        
                # elif jgl_column[0:] == "___":
                #     # If nothing has been chosen, choose randomly
                #     self.jgl_game.jgl_game_board[random.choice(self.jgl_possible_rows)][random.choice(self.jgl_possible_columns)] = f"_{self.jgl_cpu_symbol}_"
                        
                # elif jgl_column[0] == f"_{self.jgl_cpu_symbol}_" and jgl_column[2] == f"_{self.jgl_cpu_symbol}_":
                #     # Chooses the box in the middle if the user marked the left and right box
                        
                #     print("Imminent user win detected!")
                #     self.jgl_game.jgl_game_board[1] = f"_{self.jgl_cpu_symbol}_"
                        
                # elif jgl_column[1:] == f"_{self.jgl_user_symbol}_" and self.jgl_game.jgl_game_board[0] == "___":
                #     # Chooses the box on the left if the user marked the middle and right most box
                        
                #     print("Imminent user win detected!")
                #     self.jgl_game.jgl_game_board[0] = f"_{self.jgl_cpu_symbol}_"
                        
                # elif jgl_row[:2] == f"_{self.jgl_user_symbol}_" and self.jgl_game.jgl_game_board[2] == "___":
                #     # Chooses the box on the right if the user marked the left and middle box
                        
                #     print("Imminent user win detected!")
                #     self.jgl_game.jgl_game_board[2] = f"_{self.jgl_cpu_symbol}_"
                
            
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
            