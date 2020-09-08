import pygame as pygame
import numpy as np
#import random
#import alg
import time
from alg import *
from sys import exit
from collections import deque

# To comment blocks of code press ctrl + /

class maze:
    PYGAMEWIDTH = 600  # 600   # Do not change this: This is window sizing
    PYGAMEHEIGHT = 600  # Do not change this: This is window sizing
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

    # Functionality: Sets player position at 1,1 as a starting point
    # def move_player_to_create_maze(self):
    #     self.maze_array[1][1] = 1


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

    # This is to color the moving routes
    def m_pattern(self, i, j, color, status):
        self.set_maze_pattern(self.screen, i, j, color, status)

    def set_maze_pattern(self, screen, i, j , color, status):
        if status == 'blocked':
            self.maze_array[i, j] = 8
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        else:
            self.maze_array[i, j] = 1
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        #time.sleep(0.1)

    # This is not color blocked cells
    def m_pattern_for_blockedpaths(self,i,j):
        self.set_maze_blocks(self.screen, i, j)

    def set_maze_blocks(self, screen, i, j):
        #self.maze_generator(screen, (255, 255, 255), i * (self.box_width + 1), j * (self.box_height + 1))
        self.maze_array[i, j] = 8
        self.maze_generator(screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))
        pygame.display.flip()
        #time.sleep(0.1)

    def set_screen(self , scrn):   # returns screen object for canvas
        self.screen = scrn
        print(self.screen)

    def get_screen(self):   # returns screen object for canvas
        return self.screen

    #Functionality: Convert and color unreached/blocked cells are maze generation for GUI
    def render_maze(self):
        for i in range(1, self.row-1):
            for j in range(1, self.col-1):
                if self.maze_array[i][j]==0:
                    self.maze_array[i][j] = 8
                    self.maze_generator(self.screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))


    def start_game(self, obj):
        ThingsToAppearOnScreen_Display = self.screen
        self.maze_array = np.zeros((self.row, self.col), dtype=int)
        self.Apply_border(self.maze_array)  # Sets array values for the border

        #self.move_player_to_create_maze()  # USE THIS TO SET THE PLAYER ON MAP

        pygame.display.set_caption("TITLE", "ASD")
        pygame.display.flip()
        green = (0,128,0)
        self.draw_maze(ThingsToAppearOnScreen_Display, green)
        #print(self.maze_array)

        # Note: The passed oject has the ref address that way I do not ahve to initialize new obj
        a = BFS(ThingsToAppearOnScreen_Display, self.get_arr() , obj)   # MY OWN CLASS
        pygame.display.flip()

        # THIS IS WHERE YOU KNOW WHAT MAZE YOU ARE GENERATING
        a.maze_generate_with_probability_BFS()
        print(self.maze_array)
        print()
        #a.generate_maze_no_alg()
        self.render_maze()  # This is to reach blocked cells after maze is generated
        print(self.maze_array)


        #self.draw_maze(ThingsToAppearOnScreen_Display, green)
        green = (0,128,0)
        #self.draw_maze(ThingsToAppearOnScreen_Display, green)
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
    pygame.init()  # initializes the pygame object - Required to run the window on screen
    resolution = (600, 600)  # screen resolution
    flags = pygame.DOUBLEBUF  # Dont use noframe - easier when you update the screen
    ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution,flags)  # This sets the width and height of the screen that pops up
    m = maze(ThingsToAppearOnScreen_Display)
    #time.sleep(1)
    # m passed to start_game is for ref so no new object is called/copied instead I deal with the one I want to deal with
    m.start_game(m)
    #print_hi('PyCharm')

# References:
# https://stackoverflow.com/questions/19882415/closing-pygame-window