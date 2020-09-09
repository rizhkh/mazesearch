import numpy as np
import main
import alg
#from main import maze
from collections import deque
import random


# This class is to move the agent from target to solution

class move:

    m = None    # empty object
    maze_array = []
    screen = None
    q = deque() # where list of active nodes are stored
    q_visited = []
    q_list_of_visited_nodes = [] #[[1,1]]
    start_i = 1    # starting index i for current node (parent node)
    start_j = 1    # starting index j for current node (parent node)

    target_i = 0
    target_j = 0

    def __init__(self , scrn, arr, obj):
        self.m = obj    #Copy the ref address in an empty obj -> point towards the orignal address
        self.screen = scrn #obj.get_screen()
        self.maze_array = np.copy(arr)  # (obj.get_arr())
        self.target_i = obj.row - 2
        self.target_j = obj.col - 2

    # Clears path if surrounding paths are blocked for player at starting position
    # def cls_start_end_points(self):
    #     self.maze_array[1][1] = self.maze_array[2][1] = self.maze_array[1][2] = self.maze_array[2][2] = 0
    #     self.maze_array[self.target_i][self.target_j] = self.maze_array[self.target_i-1][self.target_j] = self.maze_array[self.target_i][self.target_j-1] = self.maze_array[self.target_i-1][self.target_j-1] = 0
    #     c = [ [1,1] , [2,1] , [1,2] , [2,2] ]
    #     c_1 = [
    #         [self.target_i , self.target_j] ,
    #         [self.target_i - 1 , self.target_j] ,
    #         [self.target_i , self.target_j - 1] ,
    #         [self.target_i - 1 , self.target_j - 1]
    #     ]
    #     for i in c:
    #         self.m.m_pattern(i[0], i[1], (255,255,255), "open")
    #     for j in c_1:
    #         self.m.m_pattern(j[0], j[1], (255,255,255), "open")


    def player_move_dfs(self):
        # Algorithm: Add the starting position as parent node
        # Go to neighbor (using function call visit_neighbor_dfs)
        # that function calls func that checks if cell is visited or not
        color = (0, 0, 204)   # blue color for starting point
        self.m.m_pattern(self.start_i , self.start_j, (0, 0, 204), "start")
        target = [self.target_i, self.target_j]
        color = (204, 0, 102)
        self.m.m_pattern(self.target_i, self.target_j, color, "open")

        self.q.append( [self.start_i, self.start_j] )
        self.current_node(self.start_i, self.start_j)
        pos = self.q[-1]  # peek the top most element on stack
        i = pos[0]
        j = pos[1]
        p = deque()
        p = self.visit_neighbor_dfs( i , j, target,False)   # down
        print("end : " , self.q)

    def visit_neighbor_dfs(self, i , j, target, status):
        if status is not True:
            status = self.traverse_dfs(i - 1, j, target, status)  # up

        if status is not True:
            status = self.traverse_dfs(i + 1, j, target, status) # down

        if status is not True:
            status = self.traverse_dfs(i , j + 1, target, status)  # right

        if status is not True:
            status = self.traverse_dfs(i, j - 1, target, status) # left

        if  status == True:
            return True

        if self.q:
            self.q.pop()    # the element will only pop after checking the moves to its neighbor are completed or not
            color = (255,255,255) #   (55,0,255) # blue color when backtracked
            self.m.player_movement(i, j, color, "back track")
        return False

    # Functionality:  To check cell is visited or not
    def traverse_dfs(self, i, j , target, status):
        if status == True:
            return True

        if [i , j] == target:
            color = (178, 103, 100)
            self.m.player_movement(i, j, color, "open")
            return True

        if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
            if [i,j] not in self.q_list_of_visited_nodes:
                pos = [i,j]
                self.q.append(pos)
                self.current_node(i, j)
                color = (178, 0, 178)
                self.m.player_movement(i, j, color, "open")
                self.m.player_movement(i, j, (255, 255, 9), "open")
                status = self.visit_neighbor_dfs(i, j, target, status)
        return status

    def highlight_cur_node(self, i ,j, color):
        self.m.player_movement(i, j , color, "open")

    def current_node(self,i,j):
        self.q_visited.append([i,j])
        self.q_list_of_visited_nodes.append([i,j])
