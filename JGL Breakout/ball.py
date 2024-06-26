"""A Turtle ball for the game Breakout!"""

from turtle import Turtle


class jglBall(Turtle):

    def __init__(self, jgl_position) -> None:
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
        
    def jgl_move(self):
        """Allows the ball to move"""
        
        jgl_new_x = self.jgl_ball.xcor() - self.jgl_x_move
        jgl_new_y = self.jgl_ball.ycor() - self.jgl_y_move
        self.jgl_ball.goto(jgl_new_x, jgl_new_y)
     
    def jgl_bounce(self, jgl_x_bounce, jgl_y_bounce):
        """Bounces the ball based on its direction""" 
        
        if jgl_x_bounce:
           # Reverses the ball's horizontal movement direction 

            self.jgl_x_move *= -1
            self.jgl_move_speed *= 0.9
        
        if jgl_y_bounce: 
            # Reverses the ball's vertical movement direction
            
            self.jgl_y_move *= -1


    def reset_position(self):
        """Resets the ball's position after a life is lost"""
        
        self.goto(0, -100)
        self.jgl_move_speed = 0.1
        self.jgl_bounce_x()

    def jgl_check_collision_with_paddle(self, jgl_paddle):
        """Checks if the ball has collided with the paddle"""
        
        jgl_paddle_x = jgl_paddle.xcor()
        jgl_ball_x = self.jgl_ball.xcor()
        
        if self.jgl_ball.distance(jgl_paddle) < 20 and self.jgl_ball.ycor() < -100:
            
            # If the paddle is on the right side of the screen
            if jgl_paddle_x > 0:
                if jgl_ball_x > jgl_paddle_x:
                    # If the ball hits the paddle's left it
                    # should go back to the left
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=True)
                    return
                else:
                    self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
                    return
                
            # If the paddle is on the left side of the screen
            elif jgl_paddle_x < 0:
                if jgl_ball_x < jgl_paddle_x:
                    # If the ball hits the paddle's left it
                    # should go back to the left
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=True)
                    return
                else:
                    self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
                    return
                
            # Else the paddle is in the middle horizontally
            else:
                if jgl_ball_x > jgl_paddle_x:
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=True)
                    return
                elif jgl_ball_x < jgl_paddle_x:
                    self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=True)
                    return
                else:
                    self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
                    return
                    
    
    def jgl_check_collision_with_walls(self):
        """Checks collision with the walls"""
    
        # Check if collision with the top
        if self.jgl_ball.ycor() > 350:
            self.jgl_bounce(jgl_x_bounce=False, jgl_y_bounce=True)
            
        # Detect collision with the left or right walls
        if self.jgl_ball.xcor() > 450 or self.jgl_ball.xcor() < -450:
            self.jgl_bounce(jgl_x_bounce=True, jgl_y_bounce=False)
    