# import colorgram
#print out a list of each color you extracted from the list and make each color a tuple

# # Extract 8 colors fom an image
# colors = colorgram.extract('image.jpg', 30)
#
# #create new empty list of rgb_colors
# rgb_colors = []
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#
#     # Create a new tuple to hold our colors
#     new_colors = (r, g, b)
#
#     # Append tuple to list
#     rgb_colors.append(new_colors)

import random
import turtle

color_palette = [(144, 172, 199), (3, 8, 20), (230, 146, 62), (234, 216, 75), (193, 11, 51),
                (38, 186, 35), (231, 55, 101), (39, 107, 163), (13, 153, 29), (204, 33, 77),
                (205, 128, 157), (240, 85, 34), (105, 205, 97), (9, 56, 138), (40, 161, 200),
                (186, 234, 196), (140, 228, 128), (89, 129, 174), (236, 194, 217), (240, 160, 191),
                (9, 105, 31)]

def random_color():
    color = random.choice(color_palette)
    r = color[0]
    g = color[1]
    b = color[2]

    img_colors = (r, g, b)
    return img_colors

print(random_color())
# Paint a painting with 10 by 10 rows of spots around 20 in size
# space by 50

import turtle as turtle_module
import random

tina = turtle_module.Turtle()
turtle_module.colormode(255)
tina.hideturtle()
tina.penup()

# Start at upper left corner
tina.setheading(225)
tina.forward(300)
tina.setheading(0)
tina.speed("fastest")
number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    tina.dot(20, random_color())
    tina.forward(50)
    # If the dot_count is a multiple fof 10...
    if dot_count % 10 == 0:
        # Draw dots
        tina.setheading(90)
        tina.forward(50)
        tina.penup()
        tina.setheading(180)
        tina.forward(500)
        tina.setheading(0)

    tina.penup()


screen = turtle_module.Screen()
screen.exitonclick()
screen.screensize(150, 150)