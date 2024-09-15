"""The bunkers for the python version of Space Invaders using Turtle!"""

from turtle import Turtle
import math

class JglBunkers(Turtle):
    """Creates the bunkers"""
    
    def __init__(self):
        super().__init__()
        
        # Create left bunker
        self.jgl_left_bunker = self.jgl_create_bunker(-350, -150)
        
        # Create middle bunker
        self.jgl_middle_bunker = self.jgl_create_bunker(0, -150)
        
        # Create right bunker
        self.jgl_right_bunker = self.jgl_create_bunker(350, -150)
        
        # Initialize hit counters
        self.hit_counters = {
            "left_bunker": 0,
            "middle_bunker": 0,
            "right_bunker": 0
        }
        
        # Map bunkers to their names
        self.bunker_map = {
            self.jgl_left_bunker: "left_bunker",
            self.jgl_middle_bunker: "middle_bunker",
            self.jgl_right_bunker: "right_bunker"
        }
        
    def jgl_create_bunker(self, x, y) -> Turtle:
        bunker = Turtle()
        bunker.penup()
        bunker.shape("classic")
        bunker.setheading(90)
        bunker.color("pale green")
        bunker.shapesize(stretch_wid=15, stretch_len=10)
        bunker.goto(x, y)
        return bunker
        
    def get_width(self) -> float:
        """Returns the width of the bunker, suggested by CoPilot"""
        
        default_size = 20
        
        # Finds the stretch length
        stretch_len = self.shapesize()[0]  
        return default_size * stretch_len
    
    def get_bunker_y_coords(self) -> dict:
        """Returns the y-coordinates of the bunkers"""
        return {name: bunker.ycor() for bunker, name in self.bunker_map.items()}
    
    def shrink_bunker(self, bunker: Turtle, shrink_factor: float = math.sqrt(0.5)) -> None:
        """Shrinks the given bunker by the shrink factor, suggested by CoPilot"""
        
        if bunker in self.bunker_map:
            bunker_name = self.bunker_map[bunker]
            self.hit_counters[bunker_name] += 1
            if self.hit_counters[bunker_name] == 3:
                bunker.clear()
                bunker.hideturtle()
                del self.hit_counters[bunker_name]
                del self.bunker_map[bunker]
                return
        
        current_shapesize = bunker.shapesize()
        new_shapesize = (current_shapesize[0] * shrink_factor, current_shapesize[1] * shrink_factor)
        bunker.shapesize(stretch_wid=new_shapesize[0], stretch_len=new_shapesize[1])

    def jgl_get_bunker_range_dict(self) -> dict:
        """Returns the range of all bunkers"""
        
        def calculate_range(bunker):
            x = bunker.xcor()
            y = bunker.ycor()

            stretch_height, stretch_len = bunker.shapesize()[0], bunker.shapesize()[1]
            
            # Default turtle width and height are 20 pixels
            width = stretch_len * 20
            height = stretch_height * 20
            
            # Calculate the height of the arrow's sloped borders
            arrow_height = height * 0.3
            
            # Adjust the height for the arrow shape
            adjusted_height = height - arrow_height
            
            return {
                "x_range": (x - width / 2, x + width / 2),
                "y_range": (y - height / 2, y + adjusted_height / 2)
            }
                
        # Calculate the range for each bunker based on its position and size
        bunker_ranges = {
            "left_bunker": calculate_range(self.jgl_left_bunker),
            "middle_bunker": calculate_range(self.jgl_middle_bunker),
            "right_bunker": calculate_range(self.jgl_right_bunker)
        }
        
        # Debug print to verify the ranges
        # print(f"Bunker ranges: {bunker_ranges}")
        
        return bunker_ranges
