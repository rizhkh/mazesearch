import numpy as np
import main
from main import maze
#from main import maze
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
    screen = None
    # start_point = 1  # row
    # end_point = 1  # col    #m.maze_array[18][18]    #col
    q = deque()
    q_visited = [[1, 1]]  # stack to store visited nodes
    m = None    # empty object

    # Functionality: We use BFS to expand the whole map and on each exploring cell we use probability  (0<p<1) if cell is filled or not

    start_i = 1  # starting index i for current node (parent node)
    start_j = 1  # starting index j for current node (parent node)

    def __init__(self , x, arr, obj):
        self.m = obj    #Copy the ref address in an empty obj -> point towards the orignal address
        self.screen = x #obj.get_screen()
        self.maze_array = np.copy(arr)  # (obj.get_arr())

    def maze_generate_with_probability_BFS(self):
        self.visit_Neighbor(self.screen, self.start_i-1 , self.start_j) # check up
        self.visit_Neighbor(self.screen, self.start_i + 1, self.start_j)  # check down
        self.visit_Neighbor(self.screen, self.start_i, self.start_j-1)  # check left
        self.visit_Neighbor(self.screen, self.start_i, self.start_j+1)  # check right

        while self.q:
            self.q_visited.pop()
            cur_n = self.q.popleft()
            start_point = cur_n[0] #get index i for current node
            end_point = cur_n[1]    #get index j for current node
            self.current_node(start_point, end_point)    #adds it in the visited node
            self.visit_Neighbor(self.screen, start_point - 1, end_point)  # check up
            self.visit_Neighbor(self.screen, start_point + 1, end_point)  # check down
            self.visit_Neighbor(self.screen, start_point, end_point - 1)  # check left
            self.visit_Neighbor(self.screen, start_point, end_point + 1)  # check right

        print(self.maze_array)

    # ADD PROBABILITY CODE HERE OR IN m_pattern() area
    def visit_Neighbor(self,scrn,i,j):
        if self.maze_array[i][j] == 0 :
            pos = [i , j]
            self.q.append(pos)
            #m = maze(scrn)
            self.m.m_pattern( i , j )
            self.maze_array[i][j] = 1

    def current_node(self,i,j):
        self.q_visited.append([i,j])

# maze_generate_with_probability_BFS()