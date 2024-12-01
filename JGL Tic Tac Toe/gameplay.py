"""Responsible for the gameplay"""

class JglTicTacToe():
    def __init__(self):
        """Creates a 3x3 board using a dictionary and initialize each element as empty"""
        
        self.jgl_game_board = {0: '___', 1: '___', 2: '___',
                               3: '___', 4: '___', 5: '___',
                               6: '___', 7: '___', 8: '___',}
        
        self.jgl_empty_boxes = {jgl_box: "___" for jgl_box in range(len(self.jgl_game_board))}

    
    def jgl_print_board(self):
        """Prints the game board"""
        
        print(" _________________ ")
        print("|", self.jgl_game_board[0], "|", self.jgl_game_board[1], "|", self.jgl_game_board[2], "|")
        print("|", self.jgl_game_board[3], "|", self.jgl_game_board[4], "|", self.jgl_game_board[5], "|")
        print("|", self.jgl_game_board[6], "|", self.jgl_game_board[7], "|", self.jgl_game_board[8], "|")
        print(" ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ")

    def jgl_winning_combos(self):
        """Loads in winning combinations"""
        
        self.jgl_winning_combinations = [
                                        [0, 1, 2], # Row 1
                                        [3, 4, 5], # Row 2
                                        [6, 7, 8], # Row 3
                                        [2, 4, 6], # Right diagonal
                                        [0, 4, 8], # Left diagonal
                                        [0, 3, 6], # Column 1
                                        [1, 4, 7], # Column 2
                                        [2, 5, 8] # Column 3
                                        ]
        return self.jgl_winning_combinations

    def jgl_is_board_filled(self):
        """Checks if the board is filled or not"""
        
        # Iterate over the board and return false if the board has an empty sign
        for key, spot in self.jgl_game_board.items():
            if spot == "___":
                return False
            
        return True


    def jgl_check_for_wins(self):
        """Checks if either player has won"""
        
        winner_found = False
        
        for combo in self.jgl_winning_combinations:
            spot_1 = self.jgl_game_board[combo[0]]
            spot_2 = self.jgl_game_board[combo[1]]
            spot_3 = self.jgl_game_board[combo[2]]
            
            if spot_1 == spot_2 == spot_3 != "___":
                
                if spot_1 == spot_2 == spot_3:
                    # If all spots match, the winner was found
                    winner_found = True
                    
                    try:
                        # Grab the winning character
                        winning_character = spot_1.split("_")[1]

                        print(f"Winner found! {winning_character}s win!")
                    except Exception as e:
                        print(f"Exception: {e}")
        return winner_found
    
    
    def jgl_get_combinations_and_positions(self, jgl_position):
        """Get winning combinations and positions on the game board"""
        
        # Keep track of player positions and computer positions
        jgl_combos_with_positions = []
        for combo in self.jgl_winning_combinations:
            if jgl_position in combo:
                jgl_combos_with_positions.append(combo)
        return jgl_combos_with_positions
    
        