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
        
        self.jgl_winning_combos = [
            [self.jgl_game_board[0], self.jgl_game_board[1], self.jgl_game_board[2]], # Row 1
            [self.jgl_game_board[3], self.jgl_game_board[4], self.jgl_game_board[5]], # Row 2
            [self.jgl_game_board[6], self.jgl_game_board[7], self.jgl_game_board[8]], # Row 3
            [self.jgl_game_board[3], self.jgl_game_board[4], self.jgl_game_board[6]], # Right diagonal
            [self.jgl_game_board[0], self.jgl_game_board[4], self.jgl_game_board[8]], # Left diagonal
            [self.jgl_game_board[0], self.jgl_game_board[3], self.jgl_game_board[6]], # Column 1
            [self.jgl_game_board[1], self.jgl_game_board[4], self.jgl_game_board[7]], # Column 2
            [self.jgl_game_board[2], self.jgl_game_board[5], self.jgl_game_board[8]] # Column 3
            ]
        
        return self.jgl_winning_combos
    
    def jgl_is_board_filled(self):
        """Checks if the board is filled or not"""
        
        # Iterate over the board and return false if the board has an empty sign
        for spot in self.jgl_game_board:
            if self.jgl_game_board[spot] == "___":
                return False
            else:
                return True


        # TODO: Write a new function to check whether a player has won or not 
            # TODO: Check for all the rows, columns, and the two diagonals
                
    def jgl_get_combinations_and_positions(self, jgl_position, jgl_winning_combos):
        """Get winning combinations and positions on the game board"""
        
        # TODO: Keep track of player positions and computer positions
        jgl_combos_with_positions = []
        for combo in self.jgl_winning_combos:
            if jgl_position in combo:
                jgl_combos_with_positions.append(combo)
        return jgl_combos_with_positions
    
        # TODO: Keep track of possible winning combos for computer logic
        