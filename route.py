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

    f_visit = []  # fire cell
    f_list_of_visited_nodes = []
    dup = 0


    open_list = deque()
    closed_list = []
    val = []
    node_key_val_h = []
    node_key = []
    node_gval = []
    node_fval = []
    h_val = []
    book_list = {} # To book keep index and their func values

    def __init__(self , scrn, arr, obj):
        self.m = obj    #Copy the ref address in an empty obj -> point towards the orignal address
        self.screen = scrn #obj.get_screen()
        self.maze_array = np.copy(arr)  # (obj.get_arr())
        self.target_i = 10#obj.row - 2
        self.target_j = 10#obj.col - 2

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

    def calc_heuristic(self,current_i,current_j,goal_i,goal_j,distance):
        dx = abs(current_i - goal_i)
        dy = abs(current_j - goal_j)
        h = distance  * (dx + dy)
        return h

    # Functionality: returns g(n) of current_node during the expanding process to calc g(n) => g(n)=valuefromthisFunc + exploredcellvalue
    def get_gVal(self,pos):

        print(self.node_key)
        print(pos)
        index = self.node_key.index(pos)  # gets the index of the value so it can be traced to the position of index in node_key
        current_gValue = self.node_gval[index]  # current node is set to the node with the lowest func value
        return current_gValue

    # Returns the cell value of the current explored neighbor cell from map
    def visit_neighbor_astar(self, i, j):
        return self.maze_array[i][j]
        # if self.maze_array[i][j] != 8:
        #     return self.maze_array[i][j]
        # if self.maze_array[i][j] == 8:
        #     return 1000


    def expand_neighbor_astar(self, i, j, current_node):
        if [i,j] not in self.closed_list:
            if self.visit_neighbor_astar(i,j) != 8:
                print("node not in closed list ready to be explored : ", [i, j])
                print("current node  : ", current_node)
                # print("current node being processed : ", [i, j])
                cn_i = current_node[0]
                cn_j = current_node[1]
                dist = self.visit_neighbor_astar(i, j)  # returns value of current explored cell
                h = self.calc_heuristic(i, j, self.target_i, self.target_j, dist)
                g_prev = self.get_gVal( [cn_i,cn_j] ) # g(n) of current cell currently stored
                g = g_prev + self.maze_array[i][j]
                # print("g_prev ", g_prev)
                # print("self.maze_array[i][j] ", self.maze_array[i][j])
                # print("g(n) ", g)
                n_cost = g + h

                print("f(n) : ", n_cost)
                print()
                if [i,j] not in self.open_list:
                    self.open_list.append( [i, j] )
                    self.node_key.append( [i,j] )
                    self.node_gval.append(g)  #   cell value
                    self.node_fval.append(n_cost)  # cell value
                    self.h_val.append(h) # heuristic value
        #return [n_cost,g]

    # Functionality: returns the smallest f(n) value of all the nodes in open list so we can select the next current node
    def get_smallest_fn(self, cn):
        # print("in get_smallest_fn()")
        print(self.node_fval)
        print(self.node_key)
        min_val = min(self.node_fval)  # gets the lowest value of all func(n) that is stored in list node_val
        # print("tttt")
        # print(min_val)
        # print(self.node_fval)
        index = self.node_fval.index(min_val)  # gets the index of the value so it can be traced to the position of index in node_key
        # print("got the index for fval", index)
        if cn == self.node_key[index]:
            index += 1
        current_node = self.node_key[index]  # current node is set to the node with the lowest func value
        return current_node

    # Functionality: removes the heuristic and fn value for the new current node from list
    def clearItem_new_current_node(self, i, j):
        index = self.node_key.index( [i,j] )
        self.node_fval.pop(index)
        self.node_gval.pop(index)
        self.h_val.pop(index)
        self.node_key.pop(index)


    def a_star(self):
        print()

        #notes:
        # start from position 0,0 (say our start_pos has three neighbors)

        # calculate total distance and heurisitcs from start pos to neighbor a and add it to queue (priority queue)

        # calculate total distance and heurisitcs from start pos to neighbor b and add it to queue - if the total dist is greater than A then add after neigh a if smaller then add before neigh a (priority queue)

        # Basically if the total dist is greatest then add it on right if smallest left

        # when a node is expanded - remove it from open list and add it to closed_list

        # now note if you have new func value greater than the smallest one you  change the current node to that node with the smallest func value and expand from their

        # open : nodes that are visited but not expanded ( successor have not been explored yet ) This is list of pending tasks
        # closed : Nodes that have been visited and expandeed (successor have beene explored already and included
        # in the open list
        # f(n) = total distance from node to current node g(n) + heuristic of the current node you are travelling to h(n)

        #put starting node in OPEN_LIST with the function f(start_node) = h(start_node)
        self.open_list.append( [1,1] )
        self.node_key.append( [1,1] )
        self.node_gval.append(0)  #   cell value
        self.node_fval = [5000]
        self.h_val.append(5000) # heuristic value
        #                         ( [index, c_val, heur] )
        self.node_key_val_h.append( [ [1,1], 5000, 5000] )
        current_node = [1,1]
        #self.book_list['1,1'] = 0

        while self.open_list:
            # print("hello $$$$$$$$$$$$$$")
            # min_val = min(self.node_val)    # gets the lowest value of all func(n) that is stored in list node_val
            # index = self.node_val.index(min_val)    # gets the index of the value so it can be traced to the position of index in node_key
            # current_node = self.node_key[index]    # current node is set to the node with the lowest func value
            # print(current_node)

            #self.clearItem_new_current_node(current_node[0], current_node[1])
            if current_node == [self.target_i,self.target_j]: #IF CURRENT NODE IS GOAL CELL
                break

            # temp_a = 0
            # temp_b =0
            # explored_neighbor = 0 # stored in this shape [f(n),g(n)]
            index_i = current_node[0]
            index_j = current_node[1]
            self.expand_neighbor_astar( index_i - 1, index_j, current_node) # up
            self.expand_neighbor_astar( index_i + 1, index_j, current_node) # down
            self.expand_neighbor_astar( index_i, index_j - 1, current_node) # left
            self.expand_neighbor_astar( index_i, index_j + 1, current_node) # right

            # Just add the position in openlist in expand_neighbor_astar
            # in smallest fn using a for loop recalc the f(n) and select the smallest one

            new_current_node = self.get_smallest_fn(current_node)   # Note: I am still not comparing f(n) im straight getting the min f(n)
            print(" new current node is: ",new_current_node)
            print("old current node : " , current_node)
            self.open_list.remove( [current_node[0] , current_node[1] ] )
            self.closed_list.append(current_node)
            self.clearItem_new_current_node(current_node[0], current_node[1])

            current_node = new_current_node

            self.m.player_movement(new_current_node[0], new_current_node[1], (0, 0, 255), "open")
            self.m.player_movement(current_node[0], current_node[1], (255, 255, 255), "open")

            print(self.open_list)
            #self.clearItem_new_current_node(current_node[0], current_node[1])
            self.closed_list.append( new_current_node )


            # for k in neighbors:
            #     h = self.calc_heuristic(k[0], k[1], self.target_i, self.target_j, self.visit_neighbor_astar(k[0], k[1]) ) # w(CURRENT_NODE, SUCCESSOR_NODE) # <----- THESE MIGHT HAVE PROBLEMS
            #     g = self.maze_array[k[0]][k[1]] + self.maze_array[index_i][index_j]
            #     #self.tot_distance(k[0], k[1], current_node, min_val) # g(current_node) not neighbor index   # <----- THESE MIGHT HAVE PROBLEMS
            #     n_cost = g + h
            #     self.open_list.append( [ k[0], k[1] ] )
            #     if k in self.open_list:
            #         print(True)
            #         self.m.player_movement(k[0], k[1], (255, 153, 255), "open")
            #         g_of_neighhbor = self.maze_array[k[0]][k[1]] + min_val
            #         if g_of_neighhbor <= n_cost:
            #             continue
            #         elif [k[0],k[1]] in self.closed_list:
            #             if g_of_neighhbor <= n_cost:
            #                 continue
            #             self.closed_list.remove( [k[0]],k[1] )
            #             self.open_list.append([k[0]], k[1])
            #         else:
            #             self.open_list.append( [k[0],k[1]] ) # set h(SUCCESSOR_NODE) to heuristic distance to GOAL_NODE
            #             self.node_key.append( [k[0],k[1]] )
            #             self.node_val.append(0)
            #             self.h_val.append(h)
            #     g_of_neighhbor = n_cost
            #     current_node = [ k[0], k[1]]
            #     index_i = current_node[0]
            #     index_j = current_node[1]
            # self.closed_list.append(current_node)




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
        self.current_node(self.q_visited, self.q_list_of_visited_nodes,self.start_i, self.start_j)   # adds parent node to list of visited nodes and as active node

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
                self.current_node(self.q_visited, self.q_list_of_visited_nodes, i, j)
                color = (178, 0, 178)
                self.m.player_movement(i, j, color, "open")
                self.m.player_movement(i, j, (255, 255, 9), "open")
                status = self.visit_neighbor_dfs(i, j, target, status)
        return status

##########


## FIRE GENERATION
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

    def fire_start_pos(self , arr):
        i = j = self.m.col-1
        while arr[ i ][ j ] == 8:
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
        # dir_4 = random.randint(0, 4)  # This is for the fire to randomly decide its own direction

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
        target = [1, 1] # **************************** THIS WILL CONSTANTLY CHANGE
        status = False  # This boolean variable will be utilized to stop traversing when target is reached
        self.visit_Neighbor_bfs(i, j, target ,status)   #<- function that adds parent node to list of visited cells to be tracked

        while self.q or status == False:
            if self.q:
                cur_n = self.q.popleft()    # Takes the element present at start in queue(where it stores neighbor) as active node and removes to tackle duplicate nodes
                start_point = cur_n[0]  # get index i for current node
                end_point = cur_n[1]  # get index j for current node

                self.highlight_cur_node(start_point,end_point, (255, 0, 0)) # CAN BE REMOVED: THIS IS TO HIGHLIGH CURRENT CELL

                self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )  # add the prob. value of cell being on fire in a list for next time step
                status = self.visit_Neighbor_bfs(start_point - 1, end_point, target, status)  # move up

                self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
                status = self.visit_Neighbor_bfs(start_point + 1, end_point, target, status)  # move down

                self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
                status = self.visit_Neighbor_bfs(start_point, end_point - 1, target, status)  # move left

                self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
                status = self.visit_Neighbor_bfs(start_point, end_point + 1, target, status)  # move right
            else:   # This condition checks if prob. value of 0 for the open cell then that cell is added in queue again for future estimation (this cell is neighbor of fire cells)
                if self.last_fire_cells:    # last position of cell on fire - func. above will check its neighbor(determine that if they are open) and start from there just incase queue gets empty
                    print(" q  is empty - append away: " , self.q)
                    cur_n = self.last_fire_cells[-1]
                    self.q.append(cur_n)
                else:   #just incase queue gets emptied. Last open cell gets added to queue of nodes to be checked - This should not be reached
                    self.q.append( cur_n )
        print(" List of visited nodes " , self.f_list_of_visited_nodes)
        print("duplicate nodes:" , self.dup)
        self.q_visited.clear()
        self.f_list_of_visited_nodes.clear()
        self.q.clear()

    def visit_Neighbor_bfs(self,i, j , target, status):
        prob = self.fire_cells[-1]  # retrieves the prob to generate a fire cell

        if status == True:  # if Target state is reached in other neighbors - This would return True as well instead of traversing (this should not be reached)
            return True

        if [i , j] == target:   # Returns true to stop fire traverse if it reaches player
            color = (0, 0, 0)#(178, 103, 100)
            self.m.player_movement(i, j, color, "open")
            return True

        if prob >=0.5:  # if probability is more than 0.5 generate fire cell
            # if [i , j] == target:   # Returns true to stop fire traverse if it reaches player
            #     color = (0, 0, 0)#(178, 103, 100)
            #     print("FINITO ###########")
            #     self.m.player_movement(i, j, color, "open")
            #     return True
            if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
                if [i,j] not in self.f_list_of_visited_nodes:   # Checks if current cell has not been visited already
                    pos = [i,j]
                    # p = self.fire_prob(i, j, self.m.get_arr())  # generate prob
                    # self.fire_cells.append(p)
                    self.q.append(pos)  # adds node in the list of nodes that still has to be set as current nodes - in this func its the neighbor being explored
                    self.current_node(self.f_visit, self.f_list_of_visited_nodes,i, j)
                    #self.current_node(i, j)
                    color = (255, 128, 0)
                    self.m.player_movement(i, j, color, "fire")
                    #self.highlight_cur_node(i, j, (51, 153, 255))
                    self.last_fire_cells.append( [i,j] )
        else:
            if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
                # print(" prob less than 0.5 : " , [i,j])
                #
                # if [i, j] in self.q:
                #     print("[DUPLICATE] : " , [i,j] , "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                #     self.highlight_cur_node(i, j, (0, 0, 0))
                # p = self.fire_prob(i, j, self.m.get_arr()) # if prob is close to 0 and cell is not on fire this gen fire for the next traverse
                # self.fire_cells.append(p)
                if [i,j] not in self.q:
                    self.q.append([i,j])    # the empty cell where there is no fire is again added to list of nodes that has to be visited in the future

        self.fire_cells.pop(-1)
        return status

    #
    # def player_move_BFS(self, i , j):
    #     # self.q has the list of current fire  cells
    #     color = (0, 0, 204)   # blue color for starting point
    #     #self.m.m_pattern(i , j, (255, 128, 0), "start")
    #     target = [1, 1] # **************************** THIS WILL CONSTANTLY CHANGE
    #     status = False  # This boolean variable will be utilized to stop traversing when target is reached
    #     self.visit_Neighbor_bfs(i, j, target ,status)   #<- function that adds parent node to list of visited cells to be tracked
    #
    #     while self.q or status == False:
    #         if self.q:
    #             cur_n = self.q.popleft()    # Takes the element present at start in queue(where it stores neighbor) as active node and removes to tackle duplicate nodes
    #             start_point = cur_n[0]  # get index i for current node
    #             end_point = cur_n[1]  # get index j for current node
    #
    #             self.highlight_cur_node(start_point,end_point, (255, 0, 0)) # CAN BE REMOVED: THIS IS TO HIGHLIGH CURRENT CELL
    #
    #             #self.current_node(start_point,end_point)
    #
    #             #p = self.fire_prob(start_point - 1, end_point, self.m.get_arr())  # generate prob
    #             self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )  # add the prob. value of cell being on fire in a list for next time step
    #             status = self.visit_Neighbor_bfs(start_point - 1, end_point, target, status)  # move up
    #
    #             #p = self.fire_prob(i, j, self.m.get_arr())  # generate prob
    #             self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
    #             status = self.visit_Neighbor_bfs(start_point + 1, end_point, target, status)  # move down
    #
    #             #p = self.fire_prob(i, j, self.m.get_arr())  # generate prob
    #             self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
    #             status = self.visit_Neighbor_bfs(start_point, end_point - 1, target, status)  # move left
    #
    #             #p = self.fire_prob(i, j, self.m.get_arr())  # generate prob
    #             self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
    #             status = self.visit_Neighbor_bfs(start_point, end_point + 1, target, status)  # move right
    #         else:   # This condition checks if prob. value of 0 for the open cell then that cell is added in queue again for future estimation (this cell is neighbor of fire cells)
    #             if self.last_fire_cells:    # last position of cell on fire - func. above will check its neighbor(determine that if they are open) and start from there just incase queue gets empty
    #                 print(" q  is empty - append away: " , self.q)
    #                 cur_n = self.last_fire_cells[-1]
    #                 self.q.append(cur_n)
    #             else:   #just incase queue gets emptied. Last open cell gets added to queue of nodes to be checked - This should not be reached
    #                 self.q.append( cur_n )
    #             #self.q.append(cur_n)
    #             #print(self.q)
    #             #status = True
    #     print(" List of visited nodes " , self.f_list_of_visited_nodes)
    #     print("duplicate nodes:" , self.dup)
    #     self.q_visited.clear()
    #     self.f_list_of_visited_nodes.clear()
    #     self.q.clear()
    #
    # def visit_Neighbor_bfs(self,i, j , target, status):
    #     prob = self.fire_cells[-1]  # retrieves the prob to generate a fire cell
    #
    #     if status == True:  # if Target state is reached in other neighbors - This would return True as well instead of traversing (this should not be reached)
    #         return True
    #
    #     if [i , j] == target:   # Returns true to stop fire traverse if it reaches player
    #         color = (0, 0, 0)#(178, 103, 100)
    #         self.m.player_movement(i, j, color, "open")
    #         return True
    #
    #     if prob >=0.5:  # if probability is more than 0.5 generate fire cell
    #         # if [i , j] == target:   # Returns true to stop fire traverse if it reaches player
    #         #     color = (0, 0, 0)#(178, 103, 100)
    #         #     print("FINITO ###########")
    #         #     self.m.player_movement(i, j, color, "open")
    #         #     return True
    #         if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
    #             if [i,j] not in self.f_list_of_visited_nodes:   # Checks if current cell has not been visited already
    #                 pos = [i,j]
    #                 # p = self.fire_prob(i, j, self.m.get_arr())  # generate prob
    #                 # self.fire_cells.append(p)
    #                 self.q.append(pos)  # adds node in the list of nodes that still has to be set as current nodes - in this func its the neighbor being explored
    #                 self.current_node(self.f_visit, self.f_list_of_visited_nodes,i, j)
    #                 #self.current_node(i, j)
    #                 color = (255, 128, 0)
    #                 self.m.player_movement(i, j, color, "fire")
    #                 #self.highlight_cur_node(i, j, (51, 153, 255))
    #                 self.last_fire_cells.append( [i,j] )
    #     else:
    #         if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
    #             # print(" prob less than 0.5 : " , [i,j])
    #             #
    #             # if [i, j] in self.q:
    #             #     print("[DUPLICATE] : " , [i,j] , "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    #             #     self.highlight_cur_node(i, j, (0, 0, 0))
    #             # p = self.fire_prob(i, j, self.m.get_arr()) # if prob is close to 0 and cell is not on fire this gen fire for the next traverse
    #             # self.fire_cells.append(p)
    #             if [i,j] not in self.q:
    #                 self.q.append([i,j])    # the empty cell where there is no fire is again added to list of nodes that has to be visited in the future
    #
    #     self.fire_cells.pop(-1)
    #     return status


    def highlight_cur_node(self, i ,j, color):
        self.m.player_movement(i, j , color, "open")

    def current_node(self,q_v,q_l_v,i,j):
        # self.q_visited.append([i,j])
        # self.q_list_of_visited_nodes.append([i,j])
        q_v.append([i,j])   # queues visited # not really used - might use it in future - self.q_visited.append([i,j])
        q_l_v.append([i,j]) # queue of all list of visited nodes - self.q_list_of_visited_nodes.append([i,j])
