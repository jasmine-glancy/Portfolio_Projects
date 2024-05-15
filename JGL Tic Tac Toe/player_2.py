"""Responsible for the CPU's choices and coding"""

from gameplay import JglTicTacToe
from player_1 import JglPlayer1
import random


class JglPlayer2():
    def __init__(self, jgl_game, jgl_player_1, jgl_winning_combos):
        """Loads in player 1 and game board"""
        
        self.jgl_player_1 = jgl_player_1
        self.jgl_game = jgl_game
    
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
        
        # Assign variables for readability
        jgl_board = self.jgl_game.jgl_game_board
        jgl_winning_combos = self.jgl_game.jgl_winning_combos

        self.jgl_empty_boxes = {jgl_box: "___" for jgl_box in range(len(jgl_board))}

        print(self.jgl_empty_boxes)
        for combination in jgl_winning_combos:
            # Checks if all the elements in combination are the same. count() counts how many times the 
            # element appears in combination.
            if combination.count(self.jgl_cpu_symbol) == 2 and combination.count("___") == 1:
                # Win: If there's a move that will allow the computer to win the game, it should take it.

                # Suggested by CoPilot
                jgl_winning_move = combination.index("___")
                    
                jgl_board[jgl_winning_move] = f"_{self.jgl_cpu_symbol}_"
                    

            elif combination.count(self.jgl_user_symbol) == 2 and combination.count("___") == 1:
                # Block: If the opponent has two in a row, the computer should play the third to block the opponent.

                jgl_blocking_move = combination.index("___")
                    
                jgl_board[jgl_blocking_move] = f"_{self.jgl_cpu_symbol}_"
                    
                # Delete the filled box from empty_boxes
                del self.jgl_empty_boxes[jgl_blocking_move]
            
        # Fork: This is a move that creates an opportunity where the players have two threats to win (two non-blocked lines of 2).
        for jgl_box in self.jgl_empty_boxes:
            # Simulate a move by the computer in the current box, suggested by CoPilot
            jgl_board[jgl_box] = self.jgl_cpu_symbol
                
                
            # Checks if the computer has 2 or more winning moves
            jgl_winning_moves = 0
            jgl_user_winning_moves = 0
            for combination in jgl_winning_combos:
                if combination.count(self.jgl_cpu_symbol) == 2 and combination.count("___") == 1:
                    jgl_winning_moves += 1
                        
                if combination.count(self.jgl_user_symbol) == 2 and combination.count("___") == 1:
                    jgl_user_winning_moves += 1
                        
            # Undo the simulated move
            jgl_board[jgl_box] = "___"
                
            # If the computer has 2 or more winning moves, a fork was found
            if jgl_winning_moves >= 2:
                jgl_forked_move = jgl_box
                jgl_board[jgl_forked_move] = f"_{self.jgl_cpu_symbol}_"
                break
                
            # Block Opponent's Fork: The player should block the opponent's fork opportunities.
            if jgl_user_winning_moves >= 2:
                jgl_blocking_forked_move = jgl_box
                jgl_board[jgl_blocking_forked_move] = f"_{self.jgl_cpu_symbol}_"
                    
                # Delete the filled box from empty_boxes
                del self.jgl_empty_boxes[jgl_blocking_forked_move]
            
        jgl_corners = [0, 2, 6, 8]
        jgl_sides = [1, 3, 5, 7]
            
        # Center: If the center square is free, the computer should take it. This is often a good move because it gives the most opportunities for making three in a row.
        if jgl_board["4"] == "___":
            jgl_board["4"] = f"_{self.jgl_cpu_symbol}_"
                
            # # Delete the filled box from empty_boxes
            # del self.jgl_empty_boxes[4]
                
        # Opposite Corner: If the opponent is in the corner, the computer should play the opposite corner.
        elif jgl_board["0"] == f"_{self.jgl_user_symbol}_":
            jgl_board["2"] = f"_{self.jgl_cpu_symbol}_"
                
            # # Delete the filled box from empty_boxes
            # del self.jgl_empty_boxes[2]
                
        elif jgl_board["2"] == f"_{self.jgl_user_symbol}_":
            jgl_board["0"] = f"_{self.jgl_cpu_symbol}_"
                
            # # Delete the filled box from empty_boxes
            # del self.jgl_empty_boxes[0]
            
        elif jgl_board["6"] == f"_{self.jgl_user_symbol}_":
            jgl_board["8"] = f"_{self.jgl_cpu_symbol}_"
                
            # # Delete the filled box from empty_boxes
            # del self.jgl_empty_boxes[8]
                
        elif jgl_board["8"] == f"_{self.jgl_user_symbol}_":
            jgl_board["6"] = f"_{self.jgl_cpu_symbol}_"
                
            # # Delete the filled box from empty_boxes
            # del self.jgl_empty_boxes[6]

        elif "___" in jgl_corners:
            # Empty Corner: The computer should take an empty corner if available.

            jgl_corner_choice = random.choice(jgl_corners)
            jgl_board[jgl_corner_choice] = f"_{self.jgl_cpu_symbol}_"
                
            # Delete the filled box from empty_boxes
            # del self.jgl_empty_boxes[jgl_corner_choice]
                
            # Delete the filled box from the corners list
            jgl_corners.remove(jgl_corner_choice)
            print(jgl_corners)

        elif "___" in jgl_sides:
            # Empty Side: The computer should take an empty side if available.
            jgl_side_choice = random.choice(jgl_sides)
            jgl_board[jgl_side_choice] = f"_{self.jgl_cpu_symbol}_"
                
            # # Delete the filled box from empty_boxes
            # del self.jgl_empty_boxes[jgl_side_choice]
                
            # Delete the filled box from the corners list
            jgl_sides.remove(jgl_sides)
            print(jgl_sides)
            