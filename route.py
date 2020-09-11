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
    fire_cells = [1]
    last_fire_cells = []    # index of last fire cell to be on fire
    screen = None
    q = deque() # where list of active nodes are stored
    q_visited = []
    q_list_of_visited_nodes = [] #[[1,1]]
    start_i = 1    # starting index i for current node (parent node)
    start_j = 1    # starting index j for current node (parent node)

    target_i = 0
    target_j = 0

    dup = 0


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

        # DFS: when this function starts traversing, it keeps travelling in one direction until no neighbor can be visited
        # or it is already visited, in that case it backtracks to the previous node (removing current node from top of stack
        # and setting the active node to it - does the same if no neighbor is able to be visited)

        color = (0, 0, 204)   # blue color for starting point
        self.m.m_pattern(self.start_i , self.start_j, (0, 0, 204), "start")
        target = [self.target_i, self.target_j]
        color = (204, 0, 102)
        self.m.m_pattern(self.target_i, self.target_j, color, "open")

        self.q.append( [self.start_i, self.start_j] )   # adds parent node to list of nodes
        self.current_node(self.start_i, self.start_j)   # adds parent node to list of visited nodes and as active node
        pos = self.q[-1]  # peek the top most element on stack ( in this sit. get index of parent node to start traversing)
        i = pos[0]
        j = pos[1]
        p = deque()
        p = self.visit_neighbor_dfs( i , j, target,False)
        print("end : " , self.q)

    def visit_neighbor_dfs(self, i , j, target, status):
        if status is not True:  # If target state is fou,d traverse_dfs would return true to stop traversing any further
            status = self.traverse_dfs(i - 1, j, target, status)  # up

        if status is not True:
            status = self.traverse_dfs(i + 1, j, target, status) # down

        if status is not True:
            status = self.traverse_dfs(i , j + 1, target, status)  # right

        if status is not True:
            status = self.traverse_dfs(i, j - 1, target, status) # left

        if  status == True: #To step further traversing when target state is reached
            return True

        if self.q:
            self.q.pop()    # the element will only pop after checking the moves to its neighbor are completed or not
            color = (255,255,255) #   (55,0,255) # blue color when backtracked
            self.m.player_movement(i, j, color, "back track")
        return False

    # Functionality:  To check cell is visited or not
    def traverse_dfs(self, i, j , target, status):
        if status == True:  # if Target state is reached in other neighbors - This would return True as well instead of traversing (this should not be reached)
            return True

        if [i , j] == target:   # Returns True and changes color of target when it is reached
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

        ##########


## FIRE GENERATION

    f_steps = []  # Stores the position of cells currently on fire

        # Functionality:
    # def fire_prob(self, b_neighbor):
    #     # b_neigbor is the number of burning neigbors to an empty cell
    #     q = random.uniform(0, 1)
    #     q_pow = pow((1 - q), b_neighbor)
    #     p = 1 - q_pow
    #     return p

    def fire_prob(self, i,j,arr):
        n = 0   # number of neighbors
        if  arr[i-1][j] == 1 or arr[i-1][j] == 0:   # check neighbor on top
            n += 1

        if  arr[i+1][j] == 1 or arr[i+1][j] == 0:   # check neighbor on bottom
            n += 1

        if  arr[i][j-1] == 1 or arr[i][j-1] == 0:   # check neighbor on left
            n += 1

        if  arr[i][j+1] == 1 or arr[i][j+1] == 0:   # check neighbor on right
            n += 1
        q = random.uniform(0, 1)
        q_pow = pow((1 - q), n)
        p = 1 - q_pow
        return p

    #
    # def check_cells(self, arr, i, j):
    #     if arr[i][j] == 1:  # check up
    #         if arr[i][j] == 1:

    # freecells = [] # list of free cells next to fire - remove the index when fire advances
    # firecells = [] # index of cells with fire

    # two algs to check fire:
    # BFS
    # from the first fire move -  keep a list of open cells neighbouring it - randomly select one calc prob and that way keep adding deleting cells

    def fire_start_pos(self , arr):
        i = j = self.m.col-1
        while arr[ i ][ j ] == 8:
            print("true " , arr[ i ][ j ] )

            i = random.randint(1, self.m.col - 2)  # This would generate the random position of the fire
            j = random.randint(1, self.m.col - 2)
        return [i,j]

    def fire_movement(self):
        pos = self.fire_start_pos(self.m.get_arr())

        self.player_move_BFS( pos[0], pos[1])

        # make a function that would check the open cells around the fire
        # if 4 are open then use dir_4
        # if 3 then dir_3
        # if 2 then dir_2
        # if 1 then dir
        dir_4 = random.randint(0, 4)  # This is for the fire to randomly decide its own direction

        # check number of free neighbors
        map = self.m.get_arr()
        # check these neighbors
        #    ,8,
        #   4   6
        #    ,2,

#########

############ &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
############### BFS ########################

    def player_move_BFS(self, i , j):
        # self.q has the list of current fire  cells
        color = (0, 0, 204)   # blue color for starting point
        #self.m.m_pattern(i , j, (255, 128, 0), "start")
        target = [1, 1] # **************************** THIS WILL CONSTANTLY CHANGE
        status = False  # This boolean variable will be utilized to stop traversing when target is reached
        self.visit_Neighbor_bfs(i, j, target ,status)   #<- function that adds parent node to list of visited cells to be tracked

        while self.q or status == False:
            if self.q:
                cur_n = self.q.popleft()    # Takes the element present at start in queue(where it stores neighbor) as active node and removes to tackle duplicate nodes
                start_point = cur_n[0]  # get index i for current node
                end_point = cur_n[1]  # get index j for current node
                self.highlight_cur_node(start_point,end_point, (255, 0, 0)) # CAN BE REMOVED: THIS IS TO HIGHLIGH CURRENT CELL
                #self.current_node(start_point,end_point)
                status = self.visit_Neighbor_bfs(start_point - 1, end_point, target, status)  # move up
                status = self.visit_Neighbor_bfs(start_point + 1, end_point, target, status)  # move down
                status = self.visit_Neighbor_bfs(start_point, end_point - 1, target, status)  # move left
                status = self.visit_Neighbor_bfs(start_point, end_point + 1, target, status)  # move right
            else:
                print(cur_n , " is not on fire")
                if self.last_fire_cells:
                    print("setting pos to last fire cell position:" , self.last_fire_cells[-1])
                    cur_n = self.last_fire_cells[-1]
                    self.q.append(cur_n)
                else:
                    print("about to try again")
                    self.q.append( cur_n )
                print(" -> " , self.q)
                #self.q.append(cur_n)
                #print(self.q)
                #status = True
        print(" List of visited nodes " , self.q_list_of_visited_nodes)
        print("duplicate nodes:" , self.dup)

        self.q_visited.clear()
        self.q_list_of_visited_nodes.clear()
        self.q.clear()


    def visit_Neighbor_bfs(self,i, j , target, status):
        prob = self.fire_cells[-1]
        #self.fire_cells.remove(-1)
        if status == True:  # if Target state is reached in other neighbors - This would return True as well instead of traversing (this should not be reached)
            return True

        if prob >=0.5:
            if [i , j] == target:   # Returns True and changes color of target when it is reached
                color = (178, 103, 100)
                self.m.player_movement(i, j, color, "open")
                return True
            if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
                if [i,j] not in self.q_list_of_visited_nodes:
                    self.highlight_cur_node(i, j, (0, 0, 0))
                    pos = [i,j]

                    p = self.fire_prob(i, j, self.m.get_arr())  # if prob is close to 0 and cell is not on fire this gen fire for the next traverse
                    self.fire_cells.append(p)

                    # if pos not in self.q:
                    #     print(" $#%#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%")
                    #     print(pos , " in self.q [duplicate]")
                    #     print(" $#%#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%")
                    #     self.dup += 1
                    #     self.q.append(pos)
                    self.q.append(pos)
                    self.current_node(i, j)
                    color = (255, 128, 0)
                    self.m.player_movement(i, j, color, "fire")
                    self.m.player_movement(i, j, (255, 128, 0), "fire")
                    self.last_fire_cells.append( [i,j] )

        else:
            if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
                p = self.fire_prob(i, j, self.m.get_arr()) # if prob is close to 0 and cell is not on fire this gen fire for the next traverse
                self.fire_cells.append(p)

                self.q.append([i,j])    # the empty cell where there is no fire is again added to list of nodes that has to be visited in the future
                print(i, "," , j , "  had prob less than 0.5 - New prob generated")
        return status

    def highlight_cur_node(self, i ,j, color):
        self.m.player_movement(i, j , color, "open")

    def current_node(self,i,j):
        self.q_visited.append([i,j])
        self.q_list_of_visited_nodes.append([i,j])
