import pygame as pygame
import numpy as np
#import random
#import alg
import time
from alg import *
from ast import literal_eval
from route import *
from sys import exit
from collections import deque

# To comment blocks of code press ctrl + /

class maze:
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
        time.sleep(0.01) # PLAYER

    # This is not color blocked cells
    def m_pattern_for_blockedpaths(self,i,j):
        self.set_maze_blocks(self.screen, i, j)

    def set_maze_blocks(self, screen, i, j):
        self.maze_array[i, j] = 8
        self.maze_generator(screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))
        pygame.display.flip()

    # #Functionality: Converts closed mazes into open deadend spaces
    # def render_maze(self):
    #     num = random.randint(0, 3)
    #     for i in range(2, self.row-2):
    #         for j in range(2, self.col-2):
    #             if self.maze_array[i][j]==0:
    #                 n2 = random.randint(0, 3)
    #                 if num == 1 and n2== 0 and self.maze_array[i-1][j]  == 8:
    #                     self.maze_array[i-1][j] = 1
    #                 if num == 1 and n2== 1 and self.maze_array[i+1][j]  == 8:
    #                     self.maze_array[i+1][j] = 1
    #                 if num == 1 and n2== 2 and self.maze_array[i][j-1]  == 8:
    #                     self.maze_array[i][j-1] = 1
    #                 if num == 1 and n2== 3 and self.maze_array[i][j+1] == 8:
    #                     self.maze_array[i][j+1] = 1
    #                 #self.maze_generator(self.screen, (0, 128, 0), i * (self.box_width + 1), j * (self.box_height + 1))

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

    def mark_start_end(self,start_i,start_j,i,j):
        self.maze_generator(self.screen, (255, 51, 255), start_i * (self.box_width + 1), start_j * (self.box_height + 1))
        self.maze_generator(self.screen , (255, 51, 255), i * (self.box_width + 1), j * (self.box_height + 1))

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
        pygame.display.flip()

        b =  move(ThingsToAppearOnScreen_Display, self.get_arr() , obj)
        pygame.display.flip()

        #b.new_target()

        # ####### ******** STRATEGY ONE Uniform cost search ******** ##################
        # l = b.uniform_cost_search([1,1])
        # for i in l:
        #     if l.get(i) != None:
        #         cn_i = l.get(i)
        #         c_i = cn_i[0]
        #         c_j = cn_i[1]
        #         self.player_movement(c_i, c_j, (0, 0, 0), "player")


        #
        # ###### ******** STRATEGY ONE For A STAR ******** ##################
        # move_player = b.player_init()
        # move_player = b.a_star_SOne(move_player)
        # b.init_fire()
        # i = 0
        # j = 0
        # status = False
        # if type(move_player) == bool:
        #     if move_player==False:
        #         print(" Target Not Reachable! ")
        # if type(move_player) == list:
        #     while i<5 or status == False:
        #
        #         if j == len(move_player):
        #             print(" Target Reached! ")
        #             break
        #
        #         status = b.fire_movement_process(status, i)
        #         current_move = move_player[j]
        #
        #         if self.maze_array[ current_move[0] ][ current_move[1] ] == 4:
        #             print(" DIED! ")
        #             break
        #
        #         if j < len(move_player):
        #             self.player_movement(current_move[0], current_move[1], (0, 0, 255), "player")
        #             self.player_movement(current_move[0], current_move[1], (255, 255, 102), "player")
        #             if status == True:
        #                 print(" Game Over! ")
        #                 break
        #         i += 1
        #         j += 1
        #         if i==5:
        #             i=0


        # ###### ******** STRATEGY TWO For A STAR ******** ################## RECOMPUTE

        # i run one outside the while loop
        # use that list as my steps
        # if it returns true - keep using orignal list and pop
        # if false - pop(0) from orignal and keep popping until you have True
        # one you have True - replace orignal list with where you got the true
        # now use that list

        move_player = b.player_init()
        b.init_fire()
        i = 0
        status = False
        already_visited = []
        new_move = []
        rs = []
        moves_list = []
        moves_list = b.recompute_a_star_Two(move_player,'returnList')

        if type(moves_list) == bool:
            print("Target Not reachable")
        if moves_list==66:
            print("Target Not reachable")

        else:
            print(moves_list)
            currentmove = moves_list.pop(0)
            print("current move : ", currentmove)

        while i < 5 or status == False:
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
                print("current move : " , currentmove)
            else:
                print("PATH CHANGED ****************************************************")
                moves_list = b.recompute_a_star_Two(move_player, 'returnList')
                print(moves_list)
                if type(moves_list) == bool or moves_list == 66:
                    print("Target Not reachable")
                    break
                else:
                    currentmove =  already_visited[-2] #moves_list.pop(0)
                    print("STARTING AGAIN----------------------------------------------------")
                    self.player_movement(currentmove[0], currentmove[1], (0, 0, 255), "player")

            i += 1
            if i == 5:
                i = 0

        for k in already_visited:
            self.player_movement(k[0], k[1], (199, 156, 85), "player")



        ####### ******** MY OWN IMPLEMENTED STRATEGY ******** ##################
        # move_player = b.player_init()
        # b.init_fire()
        # i = 0
        # status = False
        # while i<5 or status == False:
        #     status = b.fire_movement_process(status,i)
        #     move_player = b.player_move_process(move_player)
        #
        #     if type(move_player) == bool:
        #         if move_player==False:
        #             print("Target Not Reachable !")
        #             break
        #
        #     if move_player == [ obj.row - 2, obj.col - 2 ]:
        #         print(" Target Reached")
        #         break
        #
        #     if move_player == 88:
        #         print(" DIED !")
        #         break
        #
        #     if status == True:
        #         print(" DIED")
        #         break
        #
        #     i += 1
        #     if i==5:
        #         i=0





        # b.cls_start_end_points()
        # b.fire_movement()
        #b.player_move_dfs()
        # b.a_star()

        #self.val_for_Astr() # Sets values of 1 to 0 on generated map for developer

        #print(self.maze_array)
        pygame.display.flip()
        #self.generate_maze(a)
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