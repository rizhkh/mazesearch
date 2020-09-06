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
maze_array = np.zeros((row, col), dtype = int)
player_movement = [[1,1]]
# maze_array = [
#     [1,2,3,4],
#     [5,6,7,8],
#     [9,10,11,12],
#     [1,2,3,4],
# ]

first_row = 0
last_row = row - 1
first_col = 0
last_col = col - 1

# Functionality: Sets Value to border(top,bottom,left,right) to apply physicality - center for the real maze is
# still empty
def Apply_border(a):
    b = Generate_Maze(maze_array) # this is just to set the middle maze
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
def Generate_Maze(arr):
    #print(maze_array)
    number = []
    stored_num = []
    for i in range(0,80):
        index_i = random.randint(1, row-1)
        index_j = random.randint(1, col-1)
        number = [index_i, index_j]
        if number not in stored_num:
            stored_num.append(number)

    return stored_num

# Functionality: Displays boxes on the screen
def maze_generator(display, color, row_x , col_y):
    # row_x=row and col_y=col is the position where the box will be displayed
    pygame.draw.rect(display, color, [col_y, row_x, box_width, box_height])

# Functionality: This function draws the maze on the pygame canvas/screen
def draw_maze(screen, color):
    pl = 6
    for i in range(0,row):
        for j in range(0,col):
            if maze_array[i,j] == 8:
                maze_generator(screen, color, i * (box_width+1), j * (box_height+1))
            if maze_array[i, j] == 1:
                maze_generator(screen, (255,255,255), i * (box_width + 1), j * (box_height + 1))
                #Note: *6 should be changed according to box_width and box_height (always add + 1 to  box_width and box_height above)

# Functionality:
def move_player_to_create_maze():
    maze_array[1][1] = 1


## This is temporary:
# player_movement is a stack that stores the last moved position by player - will be overwritten by traverse algorith
# when a new movement is made the last made movement is removed and the new position(i,j) is saved in the stack
# so that a new index can be called out when a movement has to be made

def moveDown(screen):
    result = player_movement.pop()
    i = result[0]
    j= result[1]
    print("Pressed down: ", i, j)
    maze_array[i+1, j] = 1
    player_movement.append( [i+1, j] )
    maze_generator(screen, (255, 255, 255), (i+1) * (box_width + 1), j * (box_height + 1))


def moveUp(screen):
    result = player_movement.pop()
    i = result[0]
    j = result[1]
    print("Pressed up: ", i, j)
    maze_array[i - 1, j] = 1
    player_movement.append([i - 1, j])
    maze_generator(screen, (123, 156, 120), (i - 1) * (box_width + 1), j * (box_height + 1))

def moveLeft(screen):
    result = player_movement.pop()
    i = result[0]
    j = result[1]
    print("Pressed left: ", i, j)
    maze_array[i, j - 1] = 1
    player_movement.append([i, j - 1])
    maze_generator(screen, (255, 255, 255), i * (box_width + 1), (j - 1) * (box_height + 1))

def moveRight(screen):
    result = player_movement.pop()
    i = result[0]
    j = result[1]
    print("Pressed right: ", i, j)
    maze_array[i, j + 1] = 1
    player_movement.append([i, j + 1])
    maze_generator(screen, (255, 255, 255), i * (box_width + 1), (j + 1) * (box_height + 1))

def start_game():
    #fill_array(maze_array)
    Apply_border(maze_array)    #Sets array values for the border
    move_player_to_create_maze()

    pygame.init()   # initializes the pygame object - Required to run the window on screen

    resolution = (PYGAMEWIDTH, PYGAMEHEIGHT)    # screen resolution
    flags = pygame.DOUBLEBUF    # Dont use noframe - easier when you update the screen

    ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution, flags) # This sets the width and height of the screen that pops up
    # background_colour = (255, 255, 255)
    # ThingsToAppearOnScreen_Display.fill(background_colour)
    #pygame.display.flip()
    pygame.display.set_caption("TITLE","ASD")
    green = (0,128,0)
    draw_maze(ThingsToAppearOnScreen_Display, green)
    pygame.display.flip()

    window_display_status = True

    # Keeps the window running unless specifically you hit the x to close it
    while window_display_status:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        moveDown(ThingsToAppearOnScreen_Display)
                        pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        moveUp(ThingsToAppearOnScreen_Display)
                        pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        moveLeft(ThingsToAppearOnScreen_Display)
                        pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        moveRight(ThingsToAppearOnScreen_Display)
                        pygame.display.flip()
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