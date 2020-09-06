import pygame as pygame
import numpy as np
import random
#import alg
from alg import *
from sys import exit
from collections import deque

# To comment blocks of code press ctrl + /

class maze:
    PYGAMEWIDTH = 600  # 600   # Do not change this: This is window sizing
    PYGAMEHEIGHT = 600  # Do not change this: This is window sizing
    row = 10  # row
    col = 10  # col
    box_width = 10
    box_height = 10
    maze_array = np.zeros((0, 0), dtype=int)
    player_movement = [[1, 1]]
    first_row = 0
    last_row = row - 1
    first_col = 0
    last_col = col - 1

    def __init__(self):
        self.maze_array = np.zeros((self.row, self.col), dtype=int)
        #Function below are called to set the outer border and player position
        self.Apply_border(self.maze_array)  # Sets array values for the border
        self.move_player_to_create_maze()

# PYGAMEWIDTH = 600 # 600   # Do not change this: This is window sizing
# PYGAMEHEIGHT = 600  # Do not change this: This is window sizing
# row = 10   # row
# col = 10    # col
# box_width = 10
# box_height = 10
# maze_array = np.zeros((row, col), dtype = int)
# player_movement = [[1,1]]
# # maze_array = [
# #     [1,2,3,4],
# #     [5,6,7,8],
# #     [9,10,11,12],
# #     [1,2,3,4],
# # ]
#
#     ad
# # Re-usablity: for nested loop structures
# first_row = 0
# last_row = row - 1
# first_col = 0
# last_col = col - 1
#
# # q = deque[]
#
# # Functionality: We use BFS to expand the whole map and on each exploring cell we use probability  (0<p<1) if cell is filled or not
# def maze_generate_with_probability():
#     #Neighbors are: top, left, right and down



# Functionality: Sets Value to border(top,bottom,left,right) to apply physicality - center for the real maze is
# still empty
    def get_arr(self):
        return self.maze_array

    def Apply_border(self,a):
        #b = Generate_Maze(maze_array) # this is just to set the middle maze
        for i in range(0,self.row):
            for j in range(0,self.col):
                if i==self.first_row or i==self.last_row:
                    self.maze_array[i,j] = 8
                if i!=self.first_row and i!=self.last_row and (j==self.first_col or j==self.last_row):
                    self.maze_array[i, j] = 8

    # Functionality: This function gets non repeating numbers and sets those as mazes // is not a maze yet
    def Generate_Maze(self,arr):
        #print(maze_array)
        number = []
        stored_num = []
        for i in range(0,80):
            index_i = random.randint(1, self.row-1)
            index_j = random.randint(1, self.col-1)
            number = [index_i, index_j]
            if number not in stored_num:
                stored_num.append(number)

        return stored_num

    # Functionality: Displays boxes on the screen
    def maze_generator(self,display, color, row_x , col_y):
        # row_x=row and col_y=col is the position where the box will be displayed
        pygame.draw.rect(display, color, [col_y, row_x, self.box_width, self.box_height])

    # Functionality: This function draws the maze on the pygame canvas/screen
    def draw_maze(self,screen, color):
        pl = 6
        for i in range(0,self.row):
            for j in range(0,self.col):
                if self.maze_array[i,j] == 8:
                    self.maze_generator(screen, color, i * (self.box_width+1), j * (self.box_height+1))
                if self.maze_array[i, j] == 1:
                    self.maze_generator(screen, (255,255,255), i * (self.box_width + 1), j * (self.box_height + 1))
                    #Note: *6 should be changed according to box_width and box_height (always add + 1 to  box_width and box_height above)

    # Functionality: Sets player position at 1,1 as a starting point
    def move_player_to_create_maze(self):
        self.maze_array[1][1] = 1


    ## This is temporary:
    # player_movement is a stack that stores the last moved position by player - will be overwritten by traverse algorith
    # when a new movement is made the last made movement is removed and the new position(i,j) is saved in the stack
    # so that a new index can be called out when a movement has to be made

    def moveDown(self,screen):
        result = self.player_movement.pop()
        i = result[0]
        j= result[1]
        print("Pressed down: ", i, j)
        if self.maze_array[i+1, j] != 8:
            self.maze_generator(screen, (255, 255, 255), i * (self.box_width + 1), j * (self.box_height + 1))  # this leave white trail color on paths visited// paths
            self.maze_array[i+1, j] = 1
            self.player_movement.append( [i+1, j] )
            self.maze_generator(screen, (255, 0, 255), (i + 1) * (self.box_width + 1), j * (self.box_height + 1)) # current position color
        else:
            self.player_movement.append([i,j])

    def moveUp(self,screen):
        result = self.player_movement.pop()
        i = result[0]
        j = result[1]
        print("Pressed up: ", i, j)
        if self.maze_array[i - 1, j] != 8:
            self.maze_generator(screen, (255, 255, 255), i * (self.box_width + 1), j * (self.box_height + 1))  # this leave white trail color on paths visited// paths
            self.maze_array[i - 1, j] = 1
            self.player_movement.append([i - 1, j])
            self.maze_generator(screen, (255, 0, 255), (i - 1) * (self.box_width + 1), j * (self.box_height + 1)) # current position color
        else:
            self.player_movement.append([i,j])

    def moveLeft(self,screen):
        result = self.player_movement.pop()
        i = result[0]
        j = result[1]
        print("Pressed left: ", i, j)
        if  self.maze_array[i, j - 1] != 8:
            self.maze_generator(screen, (255, 255, 255), i * (self.box_width + 1), j * (self.box_height + 1))  # this leave white trail color on paths visited// paths
            self.maze_array[i, j - 1] = 1
            self.player_movement.append([i, j - 1])
            self.maze_generator(screen, (255, 0, 255), i * (self.box_width + 1), (j - 1) * (self.box_height + 1)) # current position color
        else:
            self.player_movement.append([i,j])

    def moveRight(self,screen):
        result = self.player_movement.pop()
        i = result[0]
        j = result[1]
        print("Pressed right: ", i, j)
        if self.maze_array[i, j + 1] != 8:
            self.maze_generator(screen, (255, 255, 255), i * (self.box_width + 1), j * (self.box_height + 1))  # this leave white trail color on paths visited// paths
            self.maze_array[i, j + 1] = 1
            self.player_movement.append([i, j + 1])
            self.maze_generator(screen, (255, 0, 255), i * (self.box_width + 1), (j + 1) * (self.box_height + 1)) # current position color
        else:
            self.player_movement.append([i,j])

    def start_game(self):
        a = BFS()   # MY OWN CLASS
        a.maze_generate_with_probability_BFS()

        pygame.init()   # initializes the pygame object - Required to run the window on screen

        resolution = (self.PYGAMEWIDTH, self.PYGAMEHEIGHT)    # screen resolution
        flags = pygame.DOUBLEBUF    # Dont use noframe - easier when you update the screen

        ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution, flags) # This sets the width and height of the screen that pops up
        # background_colour = (255, 255, 255)
        # ThingsToAppearOnScreen_Display.fill(background_colour)
        #pygame.display.flip()
        pygame.display.set_caption("TITLE","ASD")
        green = (0,128,0)
        self.draw_maze(ThingsToAppearOnScreen_Display, green)
        pygame.display.flip()

        window_display_status = True

        # Keeps the window running unless specifically you hit the x to close it
        while window_display_status:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            self.moveDown(ThingsToAppearOnScreen_Display)
                            pygame.display.flip()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.moveUp(ThingsToAppearOnScreen_Display)
                            pygame.display.flip()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.moveLeft(ThingsToAppearOnScreen_Display)
                            pygame.display.flip()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            self.moveRight(ThingsToAppearOnScreen_Display)
                            pygame.display.flip()
                    if event.type == pygame.QUIT:
                        window_display_status = False
                        pygame.quit()
                        exit()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    m = maze()
    m.start_game()
    #print_hi('PyCharm')

# References:
# https://stackoverflow.com/questions/19882415/closing-pygame-window