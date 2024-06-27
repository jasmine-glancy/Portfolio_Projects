"""A Turtle ball for the game Breakout!"""

from turtle import Turtle
from scoreboard import jglScoreboard

class jglBall(Turtle):

    def __init__(self, jgl_position, jgl_walls, jgl_game_on, scoreboard, jgl_paddle) -> None:
        """Creates the ball"""
        
        super().__init__()
        self.jgl_ball = Turtle(shape="circle")
        self.jgl_ball.penup()
        self.jgl_ball.goto(jgl_position)
        self.jgl_ball.shapesize(stretch_wid=0.75, stretch_len=0.75)
        self.jgl_ball.color("white")
        self.jgl_ball.speed("fastest")
        self.jgl_y_move = 10
        self.jgl_x_move = 10
        self.jgl_move_speed = 0.1
        self.jgl_walls = jgl_walls
        self.jgl_game_on = jgl_game_on
        self.jgl_paddle = jgl_paddle
        
        # Initialize instructions 
        self.jgl_instruct = Turtle()
        self.jgl_instruct.hideturtle()
        self.jgl_instruct.penup()
        self.jgl_instruct.color("white")
        
        # Ensures the ball moves with the paddle until launched
        self.jgl_moving_with_paddle = True
        self.scoreboard = scoreboard
   
    
    def jgl_display_instructions(self) -> None:
        """Displays gameplay instructions""" 
        
        self.jgl_instruct.goto(0,-85)
        self.jgl_instruct.write("Click the right mouse button to launch the ball!", align="center", font=("Courier", 16, "normal"))
        self.jgl_instruct.goto(0,-150)
        self.jgl_instruct.write("Press the A and D keys to move the paddle left and right.", align="center", font=("Courier", 16, "normal"))


    def jgl_hide_instructions(self) -> None:
        
        self.jgl_instruct.clear()
     
            
    def jgl_move(self) -> None:
        """Allows the ball to move"""
        
        jgl_new_x = self.jgl_ball.xcor() + self.jgl_x_move
        jgl_new_y = self.jgl_ball.ycor() + self.jgl_y_move
        self.jgl_ball.goto(jgl_new_x, jgl_new_y)
    
    
    def jgl_move_with_paddle(self, jgl_paddle) -> None:
        """Positions the ball on top of the paddle"""
        
        if self.jgl_moving_with_paddle:
            self.jgl_ball.goto(jgl_paddle.xcor(), jgl_paddle.ycor() + 20)
  
     
    def jgl_bounce(self, jgl_x_bounce, jgl_y_bounce) -> None:
        """Bounces the ball based on its direction""" 
        
        if jgl_x_bounce:
           # Reverses the ball's horizontal movement direction 

            self.jgl_x_move *= -1
            self.jgl_move_speed *= 0.95
        
        if jgl_y_bounce: 
            # Reverses the ball's vertical movement direction
            
            self.jgl_y_move *= -1


    def jgl_reset_position(self) -> None:
        """Resets the ball's position after a life is lost"""
        
        self.jgl_ball.goto(0, -280)
        self.jgl_moving_with_paddle = True
        self.jgl_move_speed = 0.1
        self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=False)


    def jgl_check_collision_with_paddle(self, jgl_paddle) -> None:
        """Checks if the ball has collided with the paddle"""
        
        jgl_paddle_x = jgl_paddle.xcor()
        jgl_ball_x = self.jgl_ball.xcor()
        
        self.jgl_paddle_left_wall = jgl_paddle.xcor() - 30
        self.jgl_paddle_right_wall = jgl_paddle.xcor() + 30
        self.jgl_paddle_upper_wall = jgl_paddle.ycor() + 30
        self.jgl_paddle_lower_wall = jgl_paddle.ycor() - 30
        # Check if the ball is moving downwards, suggested by CoPilot
        if self.jgl_ball.distance(jgl_paddle) < 35 and self.jgl_ball.ycor() < -280 and self.jgl_y_move <0:
            
            # If the paddle is on the right side of the screen
            if jgl_paddle_x > 0:
                if jgl_ball_x > self.jgl_paddle_left_wall:
                    # If the ball hits the paddle's left it
                    # should go back to the left
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=True)
                    return
                else:
                    self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
                    return
                
            # If the paddle is on the left side of the screen
            elif jgl_paddle_x < 0:
                if jgl_ball_x < self.jgl_paddle_right_wall:
                    # If the ball hits the paddle's left it
                    # should go back to the left
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=True)
                    return
                else:
                    self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
                    return
                
            # Else the paddle is in the middle horizontally
            else:
                if jgl_ball_x > self.jgl_paddle_left_wall:
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=True)
                    return
                elif jgl_ball_x < self.jgl_paddle_right_wall:
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=True)
                    return
                else:
                    self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
                    return
                    

    def jgl_check_collision_with_walls(self) -> None:
        """Checks collision with the walls"""
    
        # Check if collision with the top
        if self.jgl_ball.ycor() > 350:
            self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
            
        # Detect collision with the left or right walls
        if self.jgl_ball.xcor() > 450 or self.jgl_ball.xcor() < -450:
            self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=False)
            
        # Check if collision with the bottom
        if self.jgl_ball.ycor() < -350:
            self.scoreboard.jgl_remove_life()
            self.jgl_reset_position()
            self.jgl_paddle.jgl_reset_paddle_position()
            return
    
    
    def jgl_check_collision_with_bricks(self) -> None:
        """Checks collision with the bricks"""
        
        for brick in self.jgl_walls.jgl_bricks[:]:
            if self.jgl_ball.distance(brick) < 25:
                self.jgl_walls.jgl_quantity -= 1
                
                brick.clear()
                brick.hideturtle()
                self.jgl_walls.jgl_bricks.remove(brick)
                
                if self.scoreboard is not None:
                    self.scoreboard.jgl_increase_score()
                    
                # Detects collision from the left
                if self.jgl_ball.xcor() < self.jgl_walls.jgl_left_wall:
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=False)
                
                # Detects collision from the right
                elif self.jgl_ball.xcor() > self.jgl_walls.jgl_right_wall:
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=False)
                
                # Detects collision from the bottom
                elif self.jgl_ball.ycor() < self.jgl_walls.jgl_lower_wall:
                    self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
                
                # Detects collision from the top
                elif self.jgl_ball.ycor() > self.jgl_walls.jgl_upper_wall:
                    self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
                break
            
            
    def jgl_launch_ball(self, jgl_x, jgl_y) -> None:
        """Launches the ball when the user clicks the screen"""
        
        
        self.jgl_moving_with_paddle = False
        self.jgl_y_move = abs(self.jgl_y_move)
        self.jgl_move()