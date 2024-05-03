"""Responsible for the CPU's choices and coding"""

from player_1 import JglPlayer1


class JglPlayer2():
    def __init__(self, ):
        self.jgl_player_1 = JglPlayer1()
    
    def jgl_computer_symbol(self):
        '''Checks the user's chosen symbol and then assigns the opposite to the computer'''
        self.jgl_user_symbol = self.jgl_player_1.jgl_check_symbol()
        
        if self.jgl_user_symbol == "X":
            self.jgl_cpu_symbol = "O"
        
        if self.jgl_user_symbol == "O":
            self.jgl_cpu_symbol = "X"
        
        print(f"Player 1 is {self.jgl_user_symbol}s!\n", f"Player 2 is {self.jgl_cpu_symbol}s!")
        return self.jgl_cpu_symbol
            
    # TODO: Second player chooses a sign from an available empty box
        # TODO: If no move will automatically win the game, computer chooses randomly from the "empty" boxes
        # otherwise the computer will choose the box that is most likely to win the game
        # TODO: If the user is likely to win next turn, prioritize that box