import numpy as np
from collections import deque
import random


class mazeGen:
    m = None    # empty object
    maze_array = []
    screen = None
    q = deque() # where list of active nodes are stored
    q_visited = []
    q_list_of_visited_nodes = []    #[[1,1]]
    start_i = 5    # starting index i for current node (parent node)
    start_j = 5    # starting index j for current node (parent node)

    def __init__(self , x, arr, obj):
        self.m = obj    #Copy the ref address in an empty obj -> point towards the orignal address
        self.screen = x
        self.maze_array = np.copy(arr)  # (obj.get_arr())

    # Functionality: Calculates the number of cell blocks to be included in the map using random generated probabily and dimension of the map
    def calc_prob(self):
        # prob = number of filled cells/NxN -> number of filled cells = prob * (NxN) - have an int set to number of filled cells , random whenever you num = 1 ,
        # set cell as filled and decrement number of filled cells n--
        p = random.uniform(0, 1)
        filled_cells = ( self.m.row * self.m.col) * p
        return  int(filled_cells)



### ************ DFS  ************ ###

    # NOTE: IF YOU USE THIS, MAKE SURE YOU SET THE STARTING SELF.MAZEARRAY=1 IN MAIN.PY
    def maze_generate_DFS(self):
        # Algorithm: Add the starting position as parent node
        # Go to neighbor (using function call visit_neighbor_dfs)
        # that function calls func that checks if cell is visited or not
        inc = 0
        filled_cells = self.calc_prob()
        self.maze_array[self.start_i, self.start_j] = 1
        self.q.append( [self.start_i, self.start_j] )
        self.current_node(self.start_i, self.start_j)
        pos = self.q[-1]  # peek the top most element on stack
        i = pos[0]
        j = pos[1]
        self.visit_neighbor_dfs( i , j , filled_cells, inc)    # down

    def visit_neighbor_dfs(self, i , j, filled_cells, inc):
        self.traverse_dfs(i - 1, j , filled_cells, inc) # up
        self.traverse_dfs(i + 1, j , filled_cells, inc)  # down
        self.traverse_dfs(i , j + 1 , filled_cells, inc)   # right
        self.traverse_dfs(i, j - 1 , filled_cells, inc)  # left
        if self.q:
            self.q.pop()    # the element will only pop after checking the moves to its neighbor are completed or not

    # Functionality:  To check cell is visited or not
    def traverse_dfs(self, i, j, filled_cells, inc):
        num = random.randint(0, 1)
        if self.maze_array[i][j] == 0:
            inc += 1
            if [i,j] not in self.q_list_of_visited_nodes:
                if num == 1 and filled_cells > 0 and inc % 2 > 0:    # Note: remove inc%2 to remove more random generation aspect of block generation
                    filled_cells = filled_cells - 1
                    color = (0,128,0)
                    self.m.m_pattern(i, j, color, "blocked")
                    self.maze_array[i][j] = 8
                    #self.visit_neighbor_dfs(i,j , filled_cells, inc)
                else:
                    pos = [i, j]
                    self.q.append(pos)
                    self.current_node(i, j)
                    color = (255, 255, 255)
                    self.m.m_pattern(i, j, color, "open")
                    self.maze_array[i][j] = 1
                    self.visit_neighbor_dfs(i, j, filled_cells, inc)

### ************ BFS  ************ ###

    # ********* MAKE SURE THE BFS PSEUDOCODE MATCHES WITH DESCRIPTION
    # Functionality: Follows BFS algorithm to generaze path. Whenever a random blocked cell is during the search process, BFS algorithm jumps to next neighbor in queue
    def maze_generate_with_probability_BFS(self):
        filled_cells = self.calc_prob()
        filled_cells = self.visit_Neighbor_bfs(self.screen, self.start_i, self.start_j,filled_cells+1, 0)    # Sets the parent node - Look at start_i for index position
        self.current_node(self.start_i, self.start_j)   # Sets parent node as current node
        inc = 0
        while self.q:
            self.q_visited.pop()
            cur_n = self.q.popleft()
            start_point = cur_n[0] #get index i for current node
            end_point = cur_n[1]    #get index j for current node
            self.highlight_cur_node(start_point,end_point)  # This function highlights current active nodes
            self.current_node(start_point, end_point)    #adds it in the visited node
            filled_cells = self.visit_Neighbor_bfs(self.screen, start_point - 1, end_point, filled_cells, inc)  # move up
            filled_cells = self.visit_Neighbor_bfs(self.screen, start_point + 1, end_point, filled_cells, inc)  # move down
            filled_cells = self.visit_Neighbor_bfs(self.screen, start_point, end_point - 1, filled_cells, inc)  # move left
            filled_cells = self.visit_Neighbor_bfs(self.screen, start_point, end_point + 1, filled_cells, inc)  # move right
            inc += 1
        self.q_visited.clear()
        self.q_list_of_visited_nodes.clear()
        self.q.clear()

    def visit_Neighbor_bfs(self, scrn, i, j, filled_cells, inc):
        num = random.randint(0, 1)
        if [i,j] not in self.q_list_of_visited_nodes:
            if self.maze_array[i][j] == 0:
                # Blocked cells are generated on every odd inc and random number is 1
                if num == 1 and filled_cells > 0 and inc%2>0:    # Note: remove inc%2 to remove more random generation aspect of block generation
                    filled_cells = filled_cells - 1
                    pos = [i, j]    # index i and j are stored in as [i,j] in the fringe
                    #self.q.append(pos)
                    color = (0,128,0)   # color of the block
                    self.m.m_pattern(i, j, color, "blocked")   # Colors the neighbouring blocks of the active node
                    self.maze_array[i][j] = 8
                else:  # if filled_cells<=0 then only open cells are generated
                    pos = [i, j]
                    self.q.append(pos)
                    color = (255, 0, 255)
                    self.m.m_pattern(i, j, color , "open")  # shows current node being traversed
                    self.maze_array[i][j] = 1
        return filled_cells

    # This function highlights the current active node
    def highlight_cur_node(self, i ,j):
        color = (255, 255, 255)# purple -(125, 0, 255)
        self.m.m_pattern(i, j , color, "open")

### ************ NO ALGORITHM MAZE  ************ ###

    # Functionality: this method iterates over 2d array and over each array checks prob and fills it - no algorithm
    def generate_maze_no_alg(self):
        inc = 0
        filled_cells = self.calc_prob()
        for index_i in range( 1, self.m.col-1):
            for index_j in range(1,self.m.col-1):
                filled_cells = self.visit_Neighbor_generate_maze_no_alg(index_i, index_j, filled_cells, inc)
                inc += 1

    def visit_Neighbor_generate_maze_no_alg(self, i, j, filled_cells, inc):
        num = random.randint(0, 1)
        if self.maze_array[i][j] == 0:
            if num == 1 and filled_cells> 0 and inc%2>0:    # Note: remove inc%2 to remove more random generation aspect of block generation
                filled_cells = filled_cells - 1
                pos = [i , j]
                self.q.append(pos)  # adds the index to the queue
                self.m.m_pattern_for_blockedpaths( i , j )   # If a cell is to be blocked then it would color that block and set its position to physical = 8
                self.maze_array[i][j] = 8
            else:   #elif filled_cells <=0:    # if filled cells are empty run this condition
                pos = [i , j]
                self.q.append(pos)
                color =  (255, 255, 255)    #White color in path generation in maze
                self.m.m_pattern( i , j , color, "open")   # shows current node being traversed
                #self.maze_array[i][j] = 1
        return filled_cells

    # Adds the current active node in the visited list for the Fringe
    def current_node(self,i,j):
        self.q_visited.append([i,j])
        self.q_list_of_visited_nodes.append([i,j])
