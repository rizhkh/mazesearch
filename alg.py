import numpy as np
import main
from main import *
from main import maze
from collections import deque


# #screen = m.ThingsToAppearOnScreen_Display
# maze_array = get_arr()
# start_point = maze_array[1][1]    #row
# end_point = maze_array[row-2][col-2]    #col    #m.maze_array[18][18]    #col
# q = deque()
# q_visited = [ [1,1] ]   # stack to store visited nodes
#
# # Functionality: We use BFS to expand the whole map and on each exploring cell we use probability  (0<p<1) if cell is filled or not
#
# start_i = 1 # starting index i for current node (parent node)
# start_j = 1 # starting index j for current node (parent node)

class BFS:
    maze_array = []
    # start_point = 1  # row
    # end_point = 1  # col    #m.maze_array[18][18]    #col
    q = deque()
    q_visited = [[1, 1]]  # stack to store visited nodes

    # Functionality: We use BFS to expand the whole map and on each exploring cell we use probability  (0<p<1) if cell is filled or not

    start_i = 1  # starting index i for current node (parent node)
    start_j = 1  # starting index j for current node (parent node)

    def __init__(self):
        m = maze()
        self.maze_array = np.copy(m.get_arr())

    def printarray(self):
        print(self.maze_array)

    def maze_generate_with_probability_BFS(self):
        # m = maze()
        # m.get_arr()
        #Neighbors are: top, left, right and down

        #first check the top left right down sides - make it better later
        #print(m.maze_array)
        print(self.start_i , " x " , self.start_j)
        print("current: ", "r", " ", "c")
        self.visit_Neighbor(self.start_i-1 , self.start_j) # check up
        self.visit_Neighbor(self.start_i + 1, self.start_j)  # check down
        self.visit_Neighbor(self.start_i, self.start_j-1)  # check left
        self.visit_Neighbor(self.start_i, self.start_j+1)  # check right
        print(self.q)
        print(self.maze_array)

        # while q:
        #     q_visited.pop()
        #     cur_n = q.popleft()
        #     start_point = cur_n[0] #get index i for current node
        #     end_point = cur_n[1]    #get index j for current node
        #     current_node(start_point, end_point)    #adds it in the visited node
        #     visit_Neighbor(start_point - 1, end_point)  # check up
        #     visit_Neighbor(start_point + 1, end_point)  # check down
        #     visit_Neighbor(start_point, end_point - 1)  # check left
        #     visit_Neighbor(start_point, end_point + 1)  # check right

    def visit_Neighbor(self,i,j):
        if self.maze_array[i][j] == 0 :
            pos = [i , j]
            self.q.append(pos)
            self.maze_array[i][j] = 1

    def current_node(self,i,j):
        self.q_visited.append([i,j])


# maze_generate_with_probability_BFS()