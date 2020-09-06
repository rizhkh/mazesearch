import pygame as pygame
import numpy as np
import random
from sys import exit

# To comment blocks of code press ctrl + /

PYGAMEWIDTH = 600 # 600   # Do not change this: This is window sizing
PYGAMEHEIGHT = 600  # Do not change this: This is window sizing
row = 50   # row
col = 50    # col
box_width = 10
box_height = 10


#maze_array = np.array((3,3))
#maze_array = np.zeros((width_x, height_y), dtype = int)
maze_array = np.zeros((row, col), dtype = int)
# maze_array = [
#     [1,2,3,4],
#     [5,6,7,8],
#     [9,10,11,12],
#     [1,2,3,4],
# ]

# MY idea: Have a 2d Array, initialize the whole 2d array as 0 and then make sure I write a function that takes
# the border (top , bottom, left, right) into 1 and later it would be maze as 1. 1 would be phyisical objects


first_row = 0
last_row = row - 1
first_col = 0
last_col = col - 1
# Functionality: Fills out the 2d array for the physicality/collision
def fill_array(a):
    print(maze_array)

# Functionality: Sets Value to border(top,bottom,left,right) to apply physicality - center for the real maze is
# still empty
def Apply_border(a):
    b = add_box_in_maze(maze_array)
    for i in range(0,row):
        for j in range(0,col):
            if i==first_row or i==last_row:
                maze_array[i,j] = 8
            if i!=first_row and i!=last_row and (j==first_col or j==last_row):
                maze_array[i, j] = 8

    for i in b:
        maze_array[i[0],i[1]] = 8

    print(maze_array)

# Functionality: This function gets non repeating numbers and sets those as mazes // is not a maze yet
def add_box_in_maze(arr):
    #print(maze_array)
    number = []
    stored_num = []
    for i in range(0,50):
        index_i = random.randint(1, 49)
        index_j = random.randint(1, 49)
        number = [index_i, index_j]
        if number not in stored_num:
            stored_num.append(number)

    return stored_num

# Functionality: Displays boxes on the screen
def maze_generator(display, color, row_x , col_y):
    # row_x=row and col_y=col is the position where the box will be displayed
    # box_width = 5
    # box_height = 5
    pygame.draw.rect(display, color, [col_y, row_x, box_width, box_height])

# Functionality:
def draw_maze(screen, color):
    pl = 6
    for i in range(0,row):
        for j in range(0,col):
            if maze_array[i,j] == 8:
                maze_generator(screen, color, i * (box_width+1), j * (box_height+1))
                #Note: *6 should be changed according to box_width and box_height (always add + 1 to  box_width and box_height above)

#################
#
#     # x = 0  # x axis
#     # y = 0  # y axis
#     # w = 20  # width of cell
# grid = []
# def build_grid(screen,x, y, w):
#     WHITE = (255, 255, 255)
#     GREEN = (0, 255, 0,)
#     BLUE = (0, 0, 255)
#     YELLOW = (255, 255, 0)
#     for i in range(1,21):
#         x = 20                                                            # set x coordinate to start position
#         y = y + 20                                                        # start a new row
#         for j in range(1, 21):
#             pygame.draw.line(screen, WHITE, [x, y], [x + w, y])           # top of cell
#             pygame.draw.line(screen, GREEN, [x + w, y], [x + w, y + w])   # right of cell
#             pygame.draw.line(screen, BLUE, [x + w, y + w], [x, y + w])   # bottom of cell
#             pygame.draw.line(screen, YELLOW, [x, y + w], [x, y])           # left of cell
#             grid.append((x,y))                                            # add cell to grid list
#             x = x + 20                                                    # move cell to new position

def start_game():
    #fill_array(maze_array)
    Apply_border(maze_array)    #Sets array values for the border
    pygame.init()   # initializes the pygame object - Required to run the window on screen

    resolution = (PYGAMEWIDTH, PYGAMEHEIGHT)    # screen resolution
    flags = pygame.DOUBLEBUF    # Dont use noframe - easier when you update the screen

    ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution, flags) # This sets the width and height of the screen that pops up

    # background_colour = (255, 255, 255)
    # ThingsToAppearOnScreen_Display.fill(background_colour)

    #pygame.display.flip()
    pygame.display.set_caption("TITLE","ASD")
    green = (0,128,0)
    #
    # x = 0  # x axis
    # y = 0  # y axis
    # w = 20  # width of cell
    # #build_grid(ThingsToAppearOnScreen_Display,40,0,20)

    draw_maze(ThingsToAppearOnScreen_Display, green)


    # maze_generator(ThingsToAppearOnScreen_Display, green, 0, 0)
    # maze_generator(ThingsToAppearOnScreen_Display, green, 0, 6)
    # maze_generator(ThingsToAppearOnScreen_Display, green, 0, 12)
    #
    # maze_generator(ThingsToAppearOnScreen_Display, green, 6, 0)
    # maze_generator(ThingsToAppearOnScreen_Display, green, 6, 6)
    # maze_generator(ThingsToAppearOnScreen_Display, green, 6, 12)
    #
    # maze_generator(ThingsToAppearOnScreen_Display, green, 12, 0)
    # maze_generator(ThingsToAppearOnScreen_Display, green, 12, 6)
    # maze_generator(ThingsToAppearOnScreen_Display, green, 12, 12)

    pygame.display.flip()

    window_display_status = True

    # Keeps the window running unless specifically you hit the x to close it
    while window_display_status:
            for event in pygame.event.get():

                # if event.type == pygame.KEYDOWN:
                #     background_colour = (255, 255, 255)
                #     screen.fill(background_colour)
                #     pygame.display.flip()
                #
                # if event.type == pygame.KEYUP:
                #     background_colour = (255, 200, 155)
                #     screen.fill(background_colour)
                #     pygame.display.flip()

                if event.type == pygame.QUIT:
                    window_display_status = False
                    pygame.quit()
                    exit()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_game()
    #print_hi('PyCharm')

# References:
# https://stackoverflow.com/questions/19882415/closing-pygame-window