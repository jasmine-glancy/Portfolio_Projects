"""Responsible for the CPU's choices and coding"""

from gameplay import JglTicTacToe
from player_1 import JglPlayer1


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
        
        # Assign variables for readability, copy suggested by CoPilot
        jgl_board = self.jgl_game.jgl_game_board.copy()
        possible_moves = [x for x, letter in jgl_board.items() if letter == "___"]
        move = None 
        
        
        # Center: If the center square is free, the computer should take it.
        if jgl_board[4] == "___":
            return self.jgl_cpu_mark_box(4, jgl_empty_boxes)
                
        for combo in jgl_winning_combos:
            spot_1 = jgl_board[combo[0]]
            spot_2 = jgl_board[combo[1]]
            spot_3 = jgl_board[combo[2]]
            
            print(spot_1, spot_2, spot_3)
            self.row = [spot_1, spot_2, spot_3]           
            
            # Win: If there's a move that will allow the computer to win the game, it should take it.
            if self.row.count(f"_{self.jgl_cpu_symbol}_") == 2 and self.row.count("___") == 1:
                print("Computer can win!")
                empty_index = self.row.index("___")
                move = combo[empty_index]
                return self.jgl_cpu_mark_box(move, jgl_empty_boxes)
                        
            # Block: If the opponent has two in a row, the computer should play the third to block the opponent.
            if self.row.count(f"_{self.jgl_user_symbol}_") == 2 and self.row.count("___") == 1:
                print("Computer can block!")
                empty_index = self.row.index("___")
                move = combo[empty_index]
                return self.jgl_cpu_mark_box(move, jgl_empty_boxes)      

        # If a side box is free, take it
        for jgl_box in [1, 3, 5, 7]:
            if jgl_box in jgl_empty_boxes:
                return self.jgl_cpu_mark_box(jgl_box, jgl_empty_boxes)                
        # If a corner box is free, take it
        for jgl_box in [0, 2, 6, 8]:
            if jgl_box in jgl_empty_boxes:
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

    