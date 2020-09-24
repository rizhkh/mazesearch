import pygame as pygame
import numpy as np
import genData
#import random
#import alg
import time
from alg import *
from ast import literal_eval
from route import *
from sys import exit
from collections import deque

# To comment blocks of code press ctrl + /

class start:
    PYGAMEWIDTH = 300  # 600   # Do not change this: This is window sizing
    PYGAMEHEIGHT = 300  # Do not change this: This is window sizing
    row = 20  # row
    col = 20  # col
    box_width = 20
    box_height = 20
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
            self.maze_array[i, j] = 1
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            #pygame.display.flip()
        else:
            self.maze_array[i, j] = 1
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            #pygame.display.flip()


    # This is to color the moving routes
    def player_movement(self, i, j, color, status):
        self.set_player_movement(self.screen, i, j, color, status)

    # Functionality: Sets the player movement values on the array
    def set_player_movement(self, screen, i, j , color, status):
        if status == 'blocked':
            self.maze_array[i, j] = 8
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        if status == 'start':
            self.maze_array[i, j] = 1
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        if status == 'fire':
            self.maze_array[i, j] = 1111
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        if status == 'back track':
            self.maze_array[i, j] = 1
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        if status == 'player':
            self.maze_array[i, j] = 2
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        else:
            self.maze_array[i, j] = 4
            self.maze_generator(screen, color, i * (self.box_width + 1), j * (self.box_height + 1))
            pygame.display.flip()
        time.sleep(0.05) # PLAYER

    # This is not color blocked cells
    def m_pattern_for_blockedpaths(self,i,j):
        self.set_maze_blocks(self.screen, i, j)

    def set_maze_blocks(self, screen, i, j):
        self.maze_array[i, j] = 8
        self.maze_generator(screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))
        pygame.display.flip()

    #Functionality: maps values to 2d maze
    def map_values(self):
        for i in range(1, self.row-1):
            for j in range(1, self.col-1):
                if self.maze_array[i][j]==0:
                    self.maze_array[i][j] = 1
                    #self.maze_generator(self.screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))

    # def val_for_Astr(self):
    #     for i in range(1, self.row-1):
    #         for j in range(1, self.col-1):
    #             if self.maze_array[i][j] == 1:
    #                 self.maze_array[i][j] = 0

    def mark_start_end(self,start_i,start_j,i,j):
        self.maze_generator(self.screen, (255, 51, 255), start_i * (self.box_width + 1), start_j * (self.box_height + 1))
        self.maze_generator(self.screen , (255, 51, 255), i * (self.box_width + 1), j * (self.box_height + 1))

    def generate_maze(self, obj):
        # THIS IS WHERE YOU KNOW WHAT MAZE YOU ARE GENERATING
        array = []

        array = obj.maze_generate_BFS( self.maze_array )
        # array = obj.maze_generate_DFS()
        ##array = obj.generate_maze_no_alg()  # To generate maze with out any algorithm
        array = obj.make_path_door(array)
        array = obj.clear_start(array , [1,1] , [self.last_row , self.last_col])
        self.maze_array = array

        #
        # array = obj.DELETETHISFUNCT()
        # self.maze_array = array
        #row - 2

        self.map_values() # To map values on 2d array maze map
        self.draw_maze(self.screen , (0,128,0)) # Draws out the GUI from the stored array values
        self.mark_start_end(1,1,self.row - 2,self.col - 2)

    def strategy_one(self, b, flammability):    # b is the object
        move_player = b.player_init()
        move_player = b.a_star_SOne(move_player)
        b.init_fire()
        i = 0
        j = 0
        status = False
        if type(move_player) == bool:
            if move_player == False:
                print(" Target Not Reachable! ")
            if move_player == True:
                print(" Target Not Reachable! ")

        if type(move_player) == list:
            while i < 5 or status == False:

                if j == len(move_player):
                    print(" Target Reached! ")
                    break

                status = b.fire_movement_process(status, i, flammability)
                current_move = move_player[j]

                if self.maze_array[current_move[0]][current_move[1]] == 4:
                    print(" DIED! ")
                    break

                if j < len(move_player):
                    self.player_movement(current_move[0], current_move[1], (0, 0, 255), "player")
                    self.player_movement(current_move[0], current_move[1], (255, 255, 102), "player")
                    if status == True:
                        print(" Game Over! ")
                        break
                i += 1
                j += 1
                if i == 5:
                    i = 0

    def strategy_Two(self, b, flammability):    # b is the object
        move_player = b.player_init()
        b.init_fire()
        i = 0
        status = False
        already_visited = []
        inc = 0
        inc_stop = 0
        moves_list = b.recompute_a_star_Two(move_player,'returnList')

        if type(moves_list) == bool:
            print("Target Not reachable")
        if moves_list==66:
            print("Target Not reachable")

        else:
            print(moves_list)
            currentmove = moves_list.pop(0)

            while i < 5 or status == False:
                status = b.fire_movement_process(status, i, flammability)
                sttus = b.recompute_a_star_Two(currentmove,'returnBool')
                if sttus == True:
                    self.player_movement(currentmove[0], currentmove[1], (109, 109, 85), "player")
                    #self.player_movement(currentmove[0], currentmove[1], (255, 255, 102), "player")
                    if currentmove == [18, 18]:
                        print("Target Reached")
                        break
                    else:
                        currentmove = moves_list.pop(0)
                        already_visited.append(currentmove)
                else:
                    print("PATH CHANGED ****************************************************")
                    moves_list = b.recompute_a_star_Two(move_player, 'returnList')

                    if type(moves_list) == bool or moves_list == 66:
                        print("Target Not reachable")
                        break
                    else:
                        currentmove = already_visited[-2]  # moves_list.pop(0)
                        print("STARTING AGAIN----------------------------------------------------")

                        if inc_stop >= 15:
                            print("ERROR")
                            break
                        if inc>=10 :    # if backtracking is stuck between two spots and is not moving - then all cells that are added in restricted cells are removed for a new path computation
                            b.rcmp_clear_restricted()
                            inc = 0
                        #b.rcmp_clear_restricted()
                        self.player_movement(currentmove[0], currentmove[1], (0, 0, 255), "player")
                        inc_stop += 1  # this is to confirm that infinite loop is on and break the loop
                i += 1
                inc += 1
                if i == 5:
                    i = 0

            for k in already_visited:
                self.player_movement(k[0], k[1], (199, 156, 85), "player")

    def strategy_Own(self, b, flammability):    # b is the object
        move_player = b.player_init()
        b.init_fire()
        i = 0
        status = False
        while i<5 or status == False:
            status = b.fire_movement_process(status,i,flammability)
            move_player = b.player_move_process(move_player)

            if type(move_player) == bool:
                if move_player==False:
                    print("Target Not Reachable !")
                    break

            if move_player == [18, 18]:#[ obj.row - 2, obj.col - 2 ]:
                print(" Target Reached")
                break

            if move_player == 88:
                print(" DIED !")
                break

            if status == True:
                print(" DIED")
                break

            i += 1
            if i==5:
                i=0

        b.clear_fire_list()



    def start_algorithm(self, obj, choice, flammability_rate):
        ThingsToAppearOnScreen_Display = self.screen
        self.maze_array = np.zeros((self.row, self.col), dtype=int)
        self.Apply_border(self.maze_array)  # Sets array values for the border
        pygame.display.set_caption("TITLE", "ASD")
        pygame.display.flip()
        a = mazeGen(ThingsToAppearOnScreen_Display, self.get_arr() , obj)   # MY OWN CLASS
        self.generate_maze(a)   # This function draws the maze
        pygame.display.flip()
        b =  move(ThingsToAppearOnScreen_Display, self.get_arr() , obj)
        pygame.display.flip()
        flammability = flammability_rate

        if choice == 'StrategyOne' :
            self.strategy_one(b , flammability)     # This should return results

        if choice == 'StrategyTwo':
            self.strategy_Two(b, flammability)  # This should return results

        if choice == 'Own':
            self.strategy_Own(b, flammability)  # This should return results

        pygame.display.flip()



# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     # pygame.init()  # initializes the pygame object - Required to run the window on screen
#     # resolution = (600, 600)  # screen resolution
#     # flags = pygame.DOUBLEBUF  # Dont use noframe - easier when you update the screen
#     # ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution,flags)  # This sets the width and height of the screen that pops up
#     # m = maze(ThingsToAppearOnScreen_Display)
#     # # m passed to start_game is for ref so no new object is called/copied instead I deal with the one I want to deal with
#     # m.start_game(m)
#
#     # g = genData.generateData()
#     # g.avg_of_all()

# References:
# https://stackoverflow.com/questions/19882415/closing-pygame-window
# https://www.machinelearningplus.com/plots/matplotlib-tutorial-complete-guide-python-plot-examples/