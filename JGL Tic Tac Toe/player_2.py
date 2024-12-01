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
        
        # self.jgl_combinations = self.jgl_game.jgl_get_combinations_and_positions(jgl_position, jgl_winning_combos)

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
        
        # Assign variables for readability, copy suggested by CoPilot
        jgl_board = self.jgl_game.jgl_game_board.copy()
        

        possible_moves = [x for x, letter in enumerate(jgl_board) if letter == "___" and x != 0]
        move = 0 
        
        for combination in jgl_winning_combos:
            for i in possible_moves:
                
                jgl_board[i] = f"_{self.jgl_cpu_symbol}_"
                
                # Win: If there's a move that will allow the computer to win the game, it should take it.
                if self.jgl_cpu_can_win(jgl_board, self.jgl_cpu_symbol):
                    move = i
                    return self.jgl_cpu_mark_box(move, jgl_empty_boxes)
                
                jgl_board[i] = "___"
            
        # Block: If the opponent has two in a row, the computer should play the third to block the opponent.
 
        for combination in jgl_winning_combos: 
            for i in possible_moves:
                if self.jgl_cpu_can_block(combination, jgl_winning_combos):
                    jgl_blocking_box = combination.index("___")
                    return self.jgl_cpu_mark_box(jgl_box, jgl_blocking_box)    
                
                jgl_board[i] = "___"       
                
        # Center: If the center square is free, the computer should take it.
        if jgl_board[4] == "___":
            return self.jgl_cpu_mark_box(4, jgl_empty_boxes)
        
        else:    
            # If a side box is free, take it
            for jgl_box in [1, 3, 5, 7]:
                if jgl_box in jgl_empty_boxes and self.jgl_user_can_win_next_turn(jgl_box):
                    return self.jgl_cpu_mark_box(jgl_box, jgl_empty_boxes)                
            # If a corner box is free, take it
            for jgl_box in [0, 2, 6, 8]:
                if jgl_box in jgl_empty_boxes and self.jgl_user_can_win_next_turn(jgl_box):
                    return self.jgl_cpu_mark_box(jgl_box, jgl_empty_boxes)
                    
        print(jgl_empty_boxes)

            
    def jgl_cpu_mark_box(self, jgl_box, jgl_empty_boxes):
        """Marks a certain box with the computer's symbol"""
        # Updates the game board and the list of empty boxes
        self.jgl_game.jgl_game_board[jgl_box] = f"_{self.jgl_cpu_symbol}_"

        if jgl_box in jgl_empty_boxes:
            jgl_empty_boxes.pop(jgl_box)
    
        print(f"Marked box {jgl_box} with {self.jgl_cpu_symbol}")
        print(f"Updated game board: {self.jgl_game.jgl_game_board}")
        print(f"Updated empty boxes: {jgl_empty_boxes}")

    def jgl_cpu_can_win(self, board, letter):
        """Checks if the computer can win"""
        
        # TODO: Prioritize winning over blocking
            
        return ((board[1] == letter and board[2] == letter and board[3] == letter) \
             or (board[4] == letter and board[5] == letter and board[6] == letter) or \
                (board[7] == letter and board[8] == letter and board[9] == letter) or \
                    (board[1] == letter and board[4] == letter and board[7] == letter) or \
                        (board[2] == letter and board[5] == letter and board[8] == letter) or \
                            (board[3] == letter and board[6] == letter and board[9] == letter) or \
                                (board[1] == letter and board[5] == letter and board[9] == letter) or \
                                    (board[3] == letter and board[5] == letter and board[7] == letter))
                
                    
    def jgl_cpu_can_block(self, combination, jgl_winning_combos):
        """Checks if the computer can block the user from winning"""
        
        for combination in jgl_winning_combos:  
            if combination.count(f"_{self.jgl_user_symbol}_") == 2 and combination.count("___") == 1:
                print("block found!")
                self.jgl_copy_board[combination[self.jgl_empty_box_index]] = f"_{self.jgl_user_symbol}_"
                    
                if all(self.jgl_copy_board[i] == f"_{self.jgl_user_symbol}_" for i in combination):
                    return True
            return False
    
    def jgl_user_can_win_next_turn(self, box):
        """Checks if the user will win next turn"""
        
        # Create a copy of the game board, suggested by CoPilot
        jgl_board_copy = self.jgl_game.jgl_game_board.copy()
        jgl_board_copy[box] = f"_{self.jgl_user_symbol}_"

        # Check if this will allow the user to win
        for winning_combo in self.jgl_game.jgl_winning_combinations:
            if all(jgl_board_copy[i] == f"_{self.jgl_user_symbol}_" for i in winning_combo):
                return True
        return False
    
    def jgl_is_winning_combination(self, combination, jgl_winning_combos):
        """Checks the winning combinations"""
        print(f"winning combos {combination}", f"all winning combos")
        return combination in jgl_winning_combos
    
            
