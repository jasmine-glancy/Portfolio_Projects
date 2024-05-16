"""Responsible for the CPU's choices and coding"""

from gameplay import JglTicTacToe
from player_1 import JglPlayer1
import random


class JglPlayer2():
    def __init__(self, jgl_game, jgl_player_1, jgl_winning_combos, jgl_empty_boxes):
        """Loads in player 1 and game board"""
        
        self.jgl_player_1 = jgl_player_1
        self.jgl_game = jgl_game
        self.jgl_game.jgl_winning_combos = jgl_winning_combos
        self.jgl_game.jgl_empty_boxes = jgl_empty_boxes
    
    def jgl_computer_symbol(self):
        """Checks the user's chosen symbol and then assigns the opposite to the computer"""
        
        self.jgl_user_symbol = self.jgl_player_1.jgl_assign_user_symbol()
        
        if self.jgl_user_symbol == "X":
            self.jgl_cpu_symbol = "O"
        
        if self.jgl_user_symbol == "O":
            self.jgl_cpu_symbol = "X"
        
        print(f"Player 1 is {self.jgl_user_symbol}s!\n", f"Player 2 is {self.jgl_cpu_symbol}s!")
        return self.jgl_cpu_symbol
            
    def jgl_computer_choice(self, jgl_winning_combos, jgl_empty_boxes):
        """Computer chooses the next move based on the available slots on the game board"""
        
        # Assign variables for readability
        jgl_board = self.jgl_game.jgl_game_board
        
        print(jgl_empty_boxes)
        for combination in jgl_winning_combos:
            
            # Win: If there's a move that will allow the computer to win the game, it should take it.
            if self.jgl_cpu_can_win(combination):
                return self.jgl_cpu_mark_box(combination)
            
            # Block: If the opponent has two in a row, the computer should play the third to block the opponent.
            if self.jgl_cpu_can_block(combination):
                return self.jgl_cpu_mark_box(combination)
            
        # Center: If the center square is free, the computer should take it.
        if jgl_board[4] == "___":
            return self.jgl_cpu_mark_box(4)
        
        
        # If a corner or side box is free, take it
        for jgl_box in [0, 2, 6, 8] or jgl_box in [1, 3, 5, 7]:
            if jgl_box in jgl_empty_boxes:
                return self.jgl_cpu_mark_box(jgl_box, jgl_empty_boxes)
            
    def jgl_cpu_can_win(self, combination):
        """Checks if the computer can win"""
        return combination.count(self.jgl_cpu_symbol) == 2 and combination.count("___") == 1
                    
    def jgl_cpu_can_block(self, combination):
        """Checks if the computer can block the user from winning"""
        return combination.count(self.jgl_user_symbol) == 2 and combination.count("___") == 1
               
    def jgl_cpu_mark_box(self, jgl_box, jgl_empty_boxes):
        """Marks a certain box with the computer's symbol"""
        # Updates the game board and the list of empty boxes
        self.jgl_game.jgl_game_board[jgl_box] = f"_{self.jgl_cpu_symbol}_"
        
        if jgl_box in jgl_empty_boxes:
            del jgl_empty_boxes[jgl_box]
            
