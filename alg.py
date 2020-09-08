import numpy as np
import main
from main import maze
#from main import maze
from collections import deque
import random

# # Functionality: We use BFS to expand the whole map and on each exploring cell we use probability  (0<p<1) if cell is filled or not


class BFS:
    m = None    # empty object
    maze_array = []
    screen = None
    q = deque() # where list of active nodes are stored

    q_visited = [] #[[1, 1]]  # stack to store visited nodes
    q_list_of_visited_nodes = [] #[[1,1]]
    start_i = 5  # starting index i for current node (parent node)
    start_j = 5  # starting index j for current node (parent node)

    def __init__(self , x, arr, obj):
        self.m = obj    #Copy the ref address in an empty obj -> point towards the orignal address
        self.screen = x #obj.get_screen()
        self.maze_array = np.copy(arr)  # (obj.get_arr())

    # This calcs prob of cell being blocked or not
    def calc(self):
        # prob = number of filled cells/NxN -> number of filled cells = prob * (NxN) - have an int set to number of filled cells , random whenever you num = 1 ,
        # set cell as filled and decrement number of filled cells n--
        #p = random.uniform(0, 1)
        p = 0.2
        filled_cells = ( self.m.row * self.m.col) * p
        return  int(filled_cells)

    def maze_generate_with_probability_BFS(self):
        filled_cells = self.calc()
        print(filled_cells)
        filled_cells = self.visit_Neighbor_bfs(self.screen, self.start_i, self.start_j,filled_cells+1)    # This function sets the parent node
        self.current_node(self.start_i, self.start_j)   # This function sets the current node
        while self.q:
            self.q_visited.pop()
            cur_n = self.q.popleft()
            start_point = cur_n[0] #get index i for current node
            end_point = cur_n[1]    #get index j for current node

            self.highlight_cur_node(start_point,end_point)  # This function highlights current active nodes

            self.current_node(start_point, end_point)    #adds it in the visited node
            filled_cells = self.visit_Neighbor_bfs(self.screen, start_point - 1, end_point, filled_cells)  # check up
            filled_cells = self.visit_Neighbor_bfs(self.screen, start_point + 1, end_point, filled_cells)  # check down
            filled_cells = self.visit_Neighbor_bfs(self.screen, start_point, end_point - 1, filled_cells)  # check left
            filled_cells = self.visit_Neighbor_bfs(self.screen, start_point, end_point + 1, filled_cells)  # check right

    def visit_Neighbor_bfs(self, scrn, i, j, filled_cells):
        num = random.randint(0, 1)
        if [i,j] not in self.q_list_of_visited_nodes:
            if self.maze_array[i][j] == 0:
                if num == 1 and filled_cells > 0:
                    filled_cells = filled_cells - 1
                    pos = [i, j]
                    #self.q.append(pos)
                    color = (0,128,0)
                    self.m.m_pattern(i, j, color)   # This paints the neighbouring blocks of the active node
                    self.maze_array[i][j] = 8
                else:  # elif filled_cells <=0:    # if filled cells are empty run this condition
                    pos = [i, j]
                    self.q.append(pos)
                    color = (255, 0, 255)
                    self.m.m_pattern(i, j, color)  # shows current node being traversed
                    self.maze_array[i][j] = 1
        return filled_cells

    # This function highlights the current active node
    def highlight_cur_node(self, i ,j):
        self.m.m_pattern(i, j , (125, 0, 255))

    # Functionality: this method iterates over 2d array and over each array checks prob and fills it - no algorithm
    def generate_maze_no_alg(self):
        filled_cells = self.calc()
        for index_i in range( 1, self.m.col-1):
            for index_j in range(1,self.m.col-1):
                filled_cells = self.visit_Neighbor_generate_maze_no_alg(index_i, index_j, filled_cells)

    def visit_Neighbor_generate_maze_no_alg(self, i, j, filled_cells):
        num = random.randint(0, 1)
        if self.maze_array[i][j] == 0:
            if num == 1 and filled_cells> 0 :
                filled_cells = filled_cells - 1
                pos = [i , j]
                self.q.append(pos)  # adds the index to the queue
                self.m.m_pattern_for_blockedpaths( i , j )   # If a cell is to be blocked then it would color that block and set its position to physical = 8
                self.maze_array[i][j] = 8
            else:   #elif filled_cells <=0:    # if filled cells are empty run this condition
                pos = [i , j]
                self.q.append(pos)
                color = (255, 0, 255)
                self.m.m_pattern( i , j , color)   # shows current node being traversed
                self.maze_array[i][j] = 1
        return filled_cells

    # Adds the current active node in the visited list
    def current_node(self,i,j):
        self.q_visited.append([i,j])
        self.q_list_of_visited_nodes.append([i,j])
