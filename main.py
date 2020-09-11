import pygame as pygame
import numpy as np
#import random
#import alg
import time
from alg import *
from route import *
from sys import exit
from collections import deque

# To comment blocks of code press ctrl + /

class maze:
    PYGAMEWIDTH = 300  # 600   # Do not change this: This is window sizing
    PYGAMEHEIGHT = 300  # Do not change this: This is window sizing
    row = 20  # row
    col = 20  # col
    box_width = 15
    box_height = 15
    maze_array = np.zeros((0, 0), dtype=int)
    player_movement = [[1, 1]]
    first_row = 0
    last_row = row - 1
    first_col = 0
    last_col = col - 1
    screen = None

    def __init__(self, sc_py):
        self.screen = sc_py

# Functionality: Sets Value to border(top,bottom,left,right) to apply physicality - center for the real maze is
# still empty
    def get_arr(self):
        return self.maze_array

    def Apply_border(self,a):
        for i in range(0,self.row):
            for j in range(0,self.col):
                if i==self.first_row or i==self.last_row:
                    self.maze_array[i,j] = 8
                if i!=self.first_row and i!=self.last_row and (j==self.first_col or j==self.last_row):
                    self.maze_array[i, j] = 8

    # Functionality: Displays boxes on the screen
    def maze_generator(self,display, color, row_x , col_y):
        pygame.draw.rect(display, color, [col_y, row_x, self.box_width, self.box_height])   # row_x=row and col_y=col is the position where the box will be displayed

    # Functionality: This function draws the maze on the pygame canvas/screen
    def draw_maze(self,screen, color):
        pl = 6
        for i in range(0,self.row):
            for j in range(0,self.col):
                if self.maze_array[i,j] == 8:
                    self.maze_generator(screen, color, i * (self.box_width+1), j * (self.box_height+1))
                if self.maze_array[i, j] == 1:
                    self.maze_generator(screen, (255,255,255), i * (self.box_width + 1), j * (self.box_height + 1)) # +1 is to add a border shade to the cells

    # This is to color the moving routes
    def m_pattern(self, i, j, color, status):
        self.set_maze_pattern(self.screen, i, j, color, status)

    # Functionality: Sets the canvas color for cells and values for the array indices
    def set_maze_pattern(self, screen, i, j , color, status):
        if status == 'blocked':
            self.maze_array[i, j] = 8
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            #pygame.display.flip()
        if status == 'start':
            self.maze_array[i, j] = 4
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            #pygame.display.flip()
        else:
            self.maze_array[i, j] = 1
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            #pygame.display.flip()
        #time.sleep(0.2)


    # This is to color the moving routes
    def player_movement(self, i, j, color, status):
        self.set_player_movement(self.screen, i, j, color, status)

    # Functionality: Sets the player movement values on the array
    def set_player_movement(self, screen, i, j , color, status):
        if status == 'blocked':
            self.maze_array[i, j] = 8
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        if status == 'fire':
            self.maze_array[i, j] = 7
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        if status == 'back track':
            self.maze_array[i, j] = 1
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        else:
            self.maze_array[i, j] = 4
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        time.sleep(0.1)

    # This is not color blocked cells
    def m_pattern_for_blockedpaths(self,i,j):
        self.set_maze_blocks(self.screen, i, j)

    def set_maze_blocks(self, screen, i, j):
        self.maze_array[i, j] = 8
        self.maze_generator(screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))
        pygame.display.flip()
        #time.sleep(1)

    #Functionality: Converts closed mazes into open deadend spaces
    def render_maze(self):
        num = random.randint(0, 3)
        for i in range(2, self.row-2):
            for j in range(2, self.col-2):
                if self.maze_array[i][j]==0:
                    n2 = random.randint(0, 3)
                    if num == 1 and n2== 0 and self.maze_array[i-1][j]  == 8:
                        self.maze_array[i-1][j] = 1
                    if num == 1 and n2== 1 and self.maze_array[i+1][j]  == 8:
                        self.maze_array[i+1][j] = 1
                    if num == 1 and n2== 2 and self.maze_array[i][j-1]  == 8:
                        self.maze_array[i][j-1] = 1
                    if num == 1 and n2== 3 and self.maze_array[i][j+1] == 8:
                        self.maze_array[i][j+1] = 1
                    #self.maze_generator(self.screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))

    #Functionality: maps values to 2d maze
    def map_values(self):
        for i in range(1, self.row-1):
            for j in range(1, self.col-1):
                if self.maze_array[i][j]==0:
                    self.maze_array[i][j] = 1
                    #self.maze_generator(self.screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))

    def val_for_Astr(self):
        for i in range(1, self.row-1):
            for j in range(1, self.col-1):
                if self.maze_array[i][j] == 1:
                    self.maze_array[i][j] = 0


    def generate_maze(self, obj):
        # THIS IS WHERE YOU KNOW WHAT MAZE YOU ARE GENERATING
        array = []
        #array = obj.maze_generate_BFS()   # Generates map with BFS algorithm with dfs traversing as pathways with open and blocked cells
        #array = obj.maze_generate_DFS()    # Generates map with DFS algorithm with dfs traversing as pathways with open and blocked cells
        #
        ######

        array = obj.generate_maze_no_alg()  # To generate maze with out any algorithm
        self.maze_array = array

        #########
        #self.render_maze()  # Renders the map


        self.map_values() # To map values on 2d array maze map


        self.draw_maze(self.screen , (0,128,0)) # Draws out the GUI from the stored array values

    def start_game(self, obj):
        ThingsToAppearOnScreen_Display = self.screen
        self.maze_array = np.zeros((self.row, self.col), dtype=int)
        self.Apply_border(self.maze_array)  # Sets array values for the border

        pygame.display.set_caption("TITLE", "ASD")
        pygame.display.flip()

        # Note: The passed oject has the ref address that way I do not ahve to initialize new obj
        a = mazeGen(ThingsToAppearOnScreen_Display, self.get_arr() , obj)   # MY OWN CLASS
        self.generate_maze(a)   # This function draws the maze

        #print(self.maze_array)
        #pygame.display.flip()

        b =  move(ThingsToAppearOnScreen_Display, self.get_arr() , obj)
        pygame.display.flip()
        # b.cls_start_end_points()
        b.fire_movement()
        #b.player_move_dfs()

        #self.val_for_Astr() # Sets values of 1 to 0 on generated map for developer

        #print(self.maze_array)
        pygame.display.flip()
        self.generate_maze(a)
        #print(self.maze_array)

        pygame.display.flip()

        window_display_status = True

        # Keeps the window running unless specifically you hit the x to close it
        while window_display_status:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        window_display_status = False
                        pygame.quit()
                        exit()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()  # initializes the pygame object - Required to run the window on screen
    resolution = (600, 600)  # screen resolution
    flags = pygame.DOUBLEBUF  # Dont use noframe - easier when you update the screen
    ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution,flags)  # This sets the width and height of the screen that pops up
    m = maze(ThingsToAppearOnScreen_Display)
    # m passed to start_game is for ref so no new object is called/copied instead I deal with the one I want to deal with
    m.start_game(m)
    #print_hi('PyCharm')

# References:
# https://stackoverflow.com/questions/19882415/closing-pygame-window