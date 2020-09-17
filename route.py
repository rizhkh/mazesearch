import numpy as np
import main
import alg
#from main import maze
from collections import deque
import random
import time

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
    cur_n_fire = []


    open_list = deque()
    closed_list = []
    restricted_cells = []
    a_visit = []
    net_cost = []
    est_cost = [] #dict()  # stores [index,cost]
    current_move = [ ]

    rcmp_open_list = deque()
    rcmp_closed_list = []
    rcmp_restricted_cells = []      # MIGHT NOT USE THIS
    rcmp_a_visit = []
    rcmp_net_cost = []
    rcmp_est_cost = [] #dict()  # stores [index,cost]
    rcmp_current_move = [ ]


    non_repeat = []
    prev_steps = []
    restrct_cells = []

    number = [1]
    prev = []

    def __init__(self , scrn, arr, obj):
        self.m = obj    #Copy the ref address in an empty obj -> point towards the orignal address
        self.screen = scrn #obj.get_screen()
        self.maze_array = np.copy(arr)  # (obj.get_arr())
        self.target_i = obj.row - 2
        self.target_j = obj.col - 2

    def calc_heuristic(self,current_i,current_j,goal_i,goal_j,distance):
        dx = abs(current_i - goal_i)
        dy = abs(current_j - goal_j)
        h = distance  * (dx + dy)
        return (dx + dy) # LOOOOOOK AT THISESSSSSSSSSSSSSSSSSSSSSSSSSS

    # Returns the cell value of the current explored neighbor cell from map
    def visit_neighbor_astar(self, i, j):
        return self.maze_array[i][j]

    # CHANGE THIS FUNCTION TO WHERE A LIST STORES INDEX POSITION and F(N)
    # def expand_neighbor_astar(self, i, j, current_node, array, clsed_list, restrcted_cells, opn_list):#, prev_gn):
    #     n_cost =9000
    #     if self.visit_neighbor_astar(i,j) != 8:
    #         if [i,j] not in clsed_list:
    #             if [i,j] not in restrcted_cells:
    #                 cn_i = current_node[0]
    #                 cn_j = current_node[1]
    #                 g_prev = array[cn_i][cn_j] #self.get_gVal( [cn_i,cn_j] ) # g(n) of current cell currently stored
    #                 g = g_prev + array[i][j]
    #                 array[i][j] = g
    #                 #dist = self.visit_neighbor_astar(i, j)
    #                 h = self.calc_heuristic(i, j, self.target_i, self.target_j, g)
    #                 n_cost = g + h
    #                 if [i,j] not in opn_list:
    #                     opn_list.append( [i, j] )
    #
    #
    #     # if self.visit_neighbor_astar(i, j) == 8:
    #     #     restrcted_cells.append( [i ,j] )
    #     return  n_cost

    def expand_neighbor_astar(self, i, j, current_node, array, clsed_list, restrcted_cells, opn_list):  # , prev_gn):
        n_cost = 1000
        if self.visit_neighbor_astar(i, j) != 8:
            if [i, j] not in clsed_list:
                if [i, j] not in restrcted_cells:
                    cn_i = current_node[0]
                    cn_j = current_node[1]
                    g_prev = array[cn_i][cn_j]  # self.get_gVal( [cn_i,cn_j] ) # g(n) of current cell currently stored
                    g = g_prev + array[i][j]
                    array[i][j] = g
                    #dist = self.visit_neighbor_astar(i, j)
                    h = self.calc_heuristic(i, j, self.target_i, self.target_j, g)
                    n_cost = g + h
                    if [i, j] not in opn_list:
                        opn_list.append([i, j])
                if [i,j] in restrcted_cells:
                    n_cost = 9000
                    #self.m.player_movement(result[1][0], result[1][1], (255, 0, 255), "player")

        # if self.visit_neighbor_astar(i, j) == 8:
        #     restrcted_cells.append( [i ,j] )
        return n_cost


    # returns smallest f(n) of the nodes being checked
    # NOTE: ONE PROBLEM IS - YOU ONLY BACKTRACK WHEN YOU ARE SURROUNDED BY BOLDERS OR PREVIOUS VISITED CELLS BUT WHAT IF THE NEXT OPEN CELL IS FIRE? IT GOES TOWARDS IT
    def get_net_cost(self, list, current_node,rstrcted_cells, clsed_list):
        pos_i = pos_j = 0
        cost = 9999
        inc_backtrack = 0
        for i in list:
            if i[0] <= cost and i[0] != 9000:
                cost = i[0]
                pos_i = i[1]
                pos_j = i[2]
            if i[0] == 9000:
                inc_backtrack += 1

        if inc_backtrack==4:
            position = self.backtracking(current_node, rstrcted_cells, clsed_list) #self.backtracking( [i[1],i[2]] )
            pos_i = position[0]
            pos_j = position[1]
            cost = 9000

        index = [ pos_i, pos_j ]
        return [ cost, index ]



    def backtracking(self, pos, rstrcted_cells, clsed_list):
        print(" I WAS HERE ")
        self.m.player_movement(pos[0], pos[1], (255, 0, 0), "open")
        self.m.player_movement(pos[0], pos[1], (160, 160, 160), "player")
        rstrcted_cells.append(pos)
        clsed_list.pop()
        if clsed_list:
            index = clsed_list[-1]
        else:
            index = [0,0]
        #index = self.closed_list[-1]
        return index


    # NOTE: WHEN YOU ARE ABOUT TO BACKTRACK - ADD THAT CURRENT NODE TO CLOSED NODES
    # TO BACKTRACK KEEP A TRACK OF PREV_NODE AND CHECK AT THE TIME OF BACKTRACKING IF ITS IN CLOSED_LIST OR OPEN_LIST AND CHANGE CURRENT NODE TO THAT

    def player_init(self):
        self.open_list.append([1, 1])
        self.closed_list.append([1,1])
        current_node = [1, 1]
        self.current_move.append( current_node )
        move = self.player_move_process([1,1])
        return move

    def new_target(self):
        pos = self.fire_pos[-1]
        self.target_i = pos[0]
        self.target_j = pos[1]


    # def player_move_process(self,current_node):
    #     nList = deque()
    #     print()
    #     print()
    #     print("=============================================")
    #     print("current node is : " , current_node)
    #     nList = self.recompute_a_star(nList, current_node)
    #     print("returned: " , nList)
    #     print(" STEPS ALREADY TAKEN :", self.non_repeat)
    #
    #     if nList != 88:
    #         for i in self.non_repeat:
    #             if i in nList:
    #                 nList.remove(i)
    #         index = nList[0]  # nList[1]
    #
    #         print("restricted cells ", self.restrct_cells)
    #         if index not in self.non_repeat:
    #             if index not in self.restrct_cells:
    #                 self.non_repeat.append(index)
    #             # if index in self.restrct_cells:
    #             #     nList.pop()
    #             #     self.non_repeat.append(index)
    #         else:
    #             index = nList[1]
    #
    #         print(" [index] : " , index)
    #         nList.clear()
    #         self.m.player_movement(index[0], index[1], (0, 0, 0), "player")
    #         self.m.player_movement(index[0], index[1], (255, 255, 153), "player")
    #
    #         self.prev_steps.append(index)
    #         print(" Prev steps:  ", self.prev_steps)
    #
    #     if nList == 88:
    #         print("Its True #################################################      Current Node ", current_node)
    #         #self.non_repeat.clear()
    #         self.non_repeat.pop()
    #         print(" Prev steps XXXXX:  " , self.prev_steps)
    #         if current_node == self.prev_steps[-1]:
    #             print("YESSS")
    #             if len(self.prev_steps) > 1:
    #                 self.prev_steps.pop()
    #             current_node = self.prev_steps[-1]
    #             if current_node not in self.restrct_cells:
    #                 self.restrct_cells.append(current_node)
    #             else:
    #                 self.prev_steps.pop()
    #                 current_node = self.prev_steps[-1]
    #         index = current_node
    #         print("----> " , index)
    #     return index

        # keep index in a new list and make sure that index is not repeated

        # current_node = self.a_star(current_node)
        # print(self.maze_array)
        # return current_node


    def player_move_process(self,current_node):
        next_step_astar = self.a_star(current_node)
        self.m.player_movement(current_node[0], current_node[1], (0, 0, 0), "player")
        nList = deque()
        i = self.number[0]  # DONT TOUCH THIS
        nList = self.recompute_a_star(nList, next_step_astar,i)
        self.number.pop()# DONT TOUCH THIS
        i += 1# DONT TOUCH THIS
        self.number.append(i)# DONT TOUCH THIS

        print(nList)
        item = nList[0]
        if len(nList) == 1:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX: " , nList[0])
            next_step_astar = nList[0]
            #break

        next_step_recompute = nList[0]

        print("current step: ", current_node)
        print("next step: " , next_step_astar )
        print("next step in recompute: ", next_step_recompute)

        if next_step_astar != next_step_recompute:
            if next_step_recompute not in self.closed_list:
                print("- - - - - - - - - - -- - - - - - -- - - -- - - - > this step : " , next_step_recompute)

        return next_step_astar

    def a_star(self, current_node):
        if self.open_list:
            #print("this is the real array in a_star :  ", self.maze_array)

            status = False

            if (current_node in self.fire_cells) or (current_node in self.last_fire_cells):
                print(self.maze_array)
                print("***********************************************************************************************")
                return 88

            if current_node == [0,0]:
                return True

            if current_node == [self.target_i,self.target_j]: #IF CURRENT NODE IS GOAL CELL
                print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
                return 88
            index_i = current_node[0]
            index_j = current_node[1]
            self.net_cost.append( [ self.expand_neighbor_astar( index_i + 1, index_j, current_node, self.maze_array, self.closed_list , self.restricted_cells, self.open_list), index_i + 1, index_j ] ) # down
            self.net_cost.append( [ self.expand_neighbor_astar( index_i, index_j - 1, current_node, self.maze_array, self.closed_list , self.restricted_cells, self.open_list) , index_i, index_j - 1 ] ) # right
            self.net_cost.append( [ self.expand_neighbor_astar( index_i - 1, index_j, current_node, self.maze_array, self.closed_list , self.restricted_cells, self.open_list) , index_i - 1, index_j ] ) # up
            self.net_cost.append( [ self.expand_neighbor_astar( index_i, index_j + 1, current_node, self.maze_array, self.closed_list , self.restricted_cells, self.open_list) , index_i, index_j + 1 ] ) # left

            result = self.get_net_cost(self.net_cost, current_node, self.restricted_cells, self.closed_list)  # results is [cost,index]

            if result[0] == 9000:
                current_node = self.closed_list[-1]
                if current_node not in self.open_list:
                    self.open_list.append(current_node)

                status = True
            self.net_cost.clear()   # we clear the last list so new nodes and their fn is saved

            if result[0] != 9000 and result[1] in self.closed_list:
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print(result[1])
                self.m.player_movement(result[1][0], result[1][1], (255, 0, 255), "player")

            if status == False:
                np = result[1]
                self.open_list.remove( [current_node[0] , current_node[1] ] )
                current_node = np
                #self.m.player_movement(np[0], np[1], (0, 0, 255), "open")
                #self.m.player_movement(np[0], np[1], (255, 255, 102), "open")
                self.m.player_movement(np[0], np[1], (0, 0, 255), "player")
                self.m.player_movement(np[0], np[1], (255, 255, 102), "player")

                self.a_visit.append( [np[0], np[1]] )   # THIS LIST HAS THE ROUTE YOUR PLAYER HAS TAKEN
                self.closed_list.append(np)
                self.est_cost.append([np, result[0]])  # [index,cost]
                if self.current_move:
                    self.current_move.clear()
                self.current_move.append( np )
        return current_node

    def recompute_a_star(self, sList, current_node, i):
        self.rcmp_open_list.append(current_node)
        self.rcmp_closed_list.append(current_node)
        #current_node = [1, 1]
        self.rcmp_current_move.append( current_node )
        array = self.maze_array.copy()

        check = False

        while self.rcmp_open_list:
            status = False
            #self.m.player_movement(current_node[0], current_node[1], (i*8, 246-(i*6), 100+(i*8)), "player")
            self.m.player_movement(current_node[0], current_node[1], (255,255,255), "player")
            if (current_node in self.fire_cells) or (current_node in self.last_fire_cells):
                #print(self.maze_array)
                return 88

            if current_node == [0,0]:
                return True

            if current_node == [self.target_i,self.target_j]: #IF CURRENT NODE IS GOAL CELL
                print(current_node , " and target is " , [self.target_i,self.target_j] )
                break

            index_i = current_node[0]
            index_j = current_node[1]
            # self.rcmp_net_cost.append(
            #     [self.expand_neighbor_astar(index_i + 1, index_j, current_node, array, self.rcmp_closed_list , self.rcmp_restricted_cells, self.rcmp_open_list), index_i + 1, index_j])  # down
            # self.rcmp_net_cost.append(
            #     [self.expand_neighbor_astar(index_i, index_j - 1, current_node, array, self.rcmp_closed_list , self.rcmp_restricted_cells, self.rcmp_open_list), index_i, index_j - 1])  # right
            # self.rcmp_net_cost.append(
            #     [self.expand_neighbor_astar(index_i - 1, index_j, current_node, array, self.rcmp_closed_list , self.rcmp_restricted_cells, self.rcmp_open_list), index_i - 1, index_j])  # up
            # self.rcmp_net_cost.append(
            #     [self.expand_neighbor_astar(index_i, index_j + 1, current_node, array, self.rcmp_closed_list , self.rcmp_restricted_cells, self.rcmp_open_list), index_i, index_j + 1])  # left

            #result = self.get_net_cost(self.rcmp_net_cost, current_node, self.rcmp_restricted_cells, self.rcmp_closed_list)  # results is [cost,index]

            self.rcmp_net_cost.append(
                [self.expand_neighbor_astar(index_i + 1, index_j, current_node, array, self.rcmp_closed_list , self.restricted_cells, self.rcmp_open_list), index_i + 1, index_j])  # down
            self.rcmp_net_cost.append(
                [self.expand_neighbor_astar(index_i, index_j - 1, current_node, array, self.rcmp_closed_list , self.restricted_cells, self.rcmp_open_list), index_i, index_j - 1])  # right
            self.rcmp_net_cost.append(
                [self.expand_neighbor_astar(index_i - 1, index_j, current_node, array, self.rcmp_closed_list , self.restricted_cells, self.rcmp_open_list), index_i - 1, index_j])  # up
            self.rcmp_net_cost.append(
                [self.expand_neighbor_astar(index_i, index_j + 1, current_node, array, self.rcmp_closed_list , self.restricted_cells, self.rcmp_open_list), index_i, index_j + 1])  # left

            result = self.get_net_cost(self.rcmp_net_cost, current_node, self.restricted_cells, self.rcmp_closed_list)  # results is [cost,index]

            if result[0] == 9000:
                current_node = self.rcmp_closed_list[-1]
                if current_node not in self.rcmp_open_list:
                    self.rcmp_open_list.append(current_node)
                status = True
            self.rcmp_net_cost.clear()  # we clear the last list so new nodes and their fn is saved
            if status == False:

                #HERE IS WHERE YOU HAVE TO MAKE THE ORIGNAL A STAR TURN AROUND
                if result[1] in self.closed_list:
                    self.m.player_movement(current_node[0], current_node[1], (255, 255, 255), "player")
                    self.closed_list.append(result[1])
                    self.restricted_cells.append(result[1])
                    # self.restricted_cells.append(result[1])
                    # sList = result[1]
                    # print("TRUIEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
                    # return sList
                    check = True

                if result[1] not in self.closed_list and check==True:
                    print("TRUIEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
                    self.m.player_movement(current_node[0], current_node[1], (255, 153, 51), "player")
                    print(result[1])
                    #check = False
                    sList.append(result[1])
                    return sList

                np = result[1]
                self.rcmp_open_list.remove([current_node[0], current_node[1]])
                current_node = np
                # self.m.player_movement(np[0], np[1], (0, 0, 255), "open")
                # self.m.player_movement(np[0], np[1], (255, 255, 102), "open")
                self.rcmp_a_visit.append([np[0], np[1]])  # THIS LIST HAS THE ROUTE YOUR PLAYER HAS TAKEN
                self.rcmp_closed_list.append(np)
                self.rcmp_est_cost.append([np, result[0]])  # [index,cost]
                if self.rcmp_current_move:
                    self.rcmp_current_move.clear()
                self.rcmp_current_move.append(np)
        #print(" $ " , self.open_list)
        sList = self.rcmp_a_visit.copy()

        self.rcmp_open_list.clear()
        self.rcmp_closed_list.clear()
        #self.rcmp_restricted_cells.clear()  ###########################################################
        self.rcmp_a_visit.clear()
        self.rcmp_net_cost.clear()
        self.rcmp_est_cost.clear()
        #print("value of passed list sList : " ,sList)


        print()
        print()
        # print("this is self.maze_array : ",self.maze_array)
        # print()
        # print("this is the copied array :  ")
        # print(array)

        return sList



    # def recompute_a_star(self, sList, current_node):
    #     self.open_list.append([1, 1])
    #     self.maze_array[3][1] = 8
    #     self.maze_array[1][1] = 0
    #     self.closed_list.append([1, 1])
    #     current_node = [1, 1]
    #
    #     while self.open_list:
    #         status = False
    #         if current_node == [0, 0]:
    #             break
    #         if current_node == [self.target_i, self.target_j]:  # IF CURRENT NODE IS GOAL CELL
    #             break
    #         index_i = current_node[0]
    #         index_j = current_node[1]
    #         self.net_cost.append(
    #             [self.expand_neighbor_astar(index_i + 1, index_j, current_node), index_i + 1, index_j])  # down
    #         self.net_cost.append(
    #             [self.expand_neighbor_astar(index_i, index_j - 1, current_node), index_i, index_j - 1])  # right
    #         self.net_cost.append(
    #             [self.expand_neighbor_astar(index_i - 1, index_j, current_node), index_i - 1, index_j])  # up
    #         self.net_cost.append(
    #             [self.expand_neighbor_astar(index_i, index_j + 1, current_node), index_i, index_j + 1])  # left
    #         result = self.get_net_cost(self.net_cost, current_node)  # results is [cost,index]
    #
    #         if result[0] == 9000:
    #             current_node = self.closed_list[-1]
    #             if current_node not in self.open_list:
    #                 self.open_list.append(current_node)
    #             status = True
    #         self.net_cost.clear()  # we clear the last list so new nodes and their fn is saved
    #         if status == False:
    #             np = result[1]
    #             self.open_list.remove([current_node[0], current_node[1]])
    #             current_node = np
    #             self.m.player_movement(np[0], np[1], (0, 0, 255), "open")
    #             self.m.player_movement(np[0], np[1], (255, 255, 102), "open")
    #             self.a_visit.append([np[0], np[1]])  # THIS LIST HAS THE ROUTE YOUR PLAYER HAS TAKEN
    #             self.closed_list.append(np)
    #             self.est_cost.append([np, result[0]])  # [index,cost]
    #             if self.current_move:
    #                 self.current_move.clear()
    #             self.current_move.append(np)
    #     print(self.open_list)
    #     sList = self.a_visit.copy()
    #
    #     self.open_list.clear()
    #     self.closed_list.clear()
    #     self.restricted_cells.clear()
    #     self.a_visit.clear()
    #     self.net_cost.clear()
    #     self.est_cost.clear()
    #     return sList

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
        #return p
        return 1 #p

    def fire_start_pos(self , arr):
        i = j = self.m.col-1
        while arr[ i ][ j ] == 8:
            i = random.randint(1, self.m.col - 2)  # This would generate the random position of the fire
            j = random.randint(1, self.m.col - 2)
        return [i,j]

    fire_pos = []

    def init_fire(self):
        pos = [7,11] #self.fire_start_pos(self.m.get_arr())
        self.fire_pos.append( pos )
        status = False  # This boolean variable will be utilized to stop traversing when target is reached
        self.visit_Neighbor_bfs(pos[0], pos[1], status)   #<- function that adds parent node to list of visited cells to be tracked

############ &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
############### BFS & DFS MOVEMENT FOR PLAYER ########################

    def fire_movement_process(self, status, number):
        status = self.player_move_BFS(status, number)
        return status

    def player_move_BFS(self, status, number):
        if self.q:
            if number == 0 :
                cur_n = self.q.popleft()    # Takes the element present at start in queue(where it stores neighbor) as active node and removes to tackle duplicate nodes
                self.cur_n_fire.append(cur_n)
                start_point = cur_n[0]  # get index i for current node
                end_point = cur_n[1]  # get index j for current node
                #self.highlight_fire_node(start_point, end_point, (255, 0, 0))
                self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )  # add the prob. value of cell being on fire in a list for next time step
                status = self.visit_Neighbor_bfs(start_point - 1, end_point, status)  # move up

            if number == 1:
                cur_n = self.cur_n_fire[-1]
                start_point = cur_n[0]  # get index i for current node
                end_point = cur_n[1]  # get index j for current node
                #self.highlight_fire_node(start_point, end_point, (255, 0, 0))
                self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
                status = self.visit_Neighbor_bfs(start_point + 1, end_point, status)  # move down

            if number == 2:
                cur_n = self.cur_n_fire[-1]
                start_point = cur_n[0]  # get index i for current node
                end_point = cur_n[1]  # get index j for current node
                #self.highlight_fire_node(start_point, end_point, (255, 0, 0))
                self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
                status = self.visit_Neighbor_bfs(start_point, end_point - 1, status)  # move left

            if number == 3:
                cur_n = self.cur_n_fire[-1]
                start_point = cur_n[0]  # get index i for current node
                end_point = cur_n[1]  # get index j for current node
                #self.highlight_fire_node(start_point, end_point, (255, 0, 0))
                self.fire_cells.append( self.fire_prob(start_point - 1, end_point, self.m.get_arr()) )
                status = self.visit_Neighbor_bfs(start_point, end_point + 1, status)  # move right
                self.cur_n_fire.pop()

        else:   # This condition checks if prob. value of 0 for the open cell then that cell is added in queue again for future estimation (this cell is neighbor of fire cells)
            if self.last_fire_cells:    # last position of cell on fire - func. above will check its neighbor(determine that if they are open) and start from there just incase queue gets empty
                print(" q  is empty - append away: " , self.q)
                if self.last_fire_cells:
                    cur_n = self.last_fire_cells[-1]
                else:
                    cur_n = self.fire_start_pos(self.m.get_arr())
                self.q.append(cur_n)
                print("IM HERE 111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
            else:   #just incase queue gets emptied. Last open cell gets added to queue of nodes to be checked - This should not be reached
                cur_n = self.cur_n_fire[-1]
                self.q.append( cur_n )
                self.cur_n_fire.pop()
                print("IM HERE 2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
        return status

    def highlight_fire_node(self, i ,j, color):
        self.m.player_movement(i, j , color, 'fire')

    def visit_Neighbor_bfs(self,i, j , status):
        prob = self.fire_cells[-1]  # retrieves the prob to generate a fire cell

        if status == True:  # if Target state is reached in other neighbors - This would return True as well instead of traversing (this should not be reached)
            return True

        if [i , j] == self.current_move[-1]: #self.current_move:   # Returns true to stop fire traverse if it reaches player
            color = (0, 0, 0)#(178, 103, 100)
            self.highlight_fire_node(i, j, (255, 0, 0))
            #self.m.player_movement(i, j, color, "fire")
            return True

        if prob >=0.5:  # if probability is more than 0.5 generate fire cell
            #if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
            if self.maze_array[i][j] != 8:
                if [i,j] not in self.f_list_of_visited_nodes:   # Checks if current cell has not been visited already
                    pos = [i,j]
                    # p = self.fire_prob(i, j, self.m.get_arr())  # generate prob
                    # self.fire_cells.append(p)
                    self.q.append(pos)  # adds node in the list of nodes that still has to be set as current nodes - in this func its the neighbor being explored
                    self.current_node(self.f_visit, self.f_list_of_visited_nodes,i, j)
                    #self.current_node(i, j)
                    color = (255, 128, 0)
                    self.maze_array[i][j] =  500
                    self.highlight_fire_node(i, j, (255, 0, 0))
                    self.last_fire_cells.append( [i,j] )
                    self.fill_fire_neighbor(i - 1,j)   # upper cell
                    self.fill_fire_neighbor(i + 1, j)  # down cell
                    self.fill_fire_neighbor(i, j - 1)  # left cell
                    self.fill_fire_neighbor(i, j + 1)  # right cell
        else:
            if self.maze_array[i][j] == 0 or self.maze_array[i][j] == 1:
                if [i,j] not in self.q:
                    self.q.append([i,j])    # the empty cell where there is no fire is again added to list of nodes that has to be visited in the future
        self.fire_cells.pop(-1)
        return status

    # Increases cell value for any open cell next to burning cell - creates the heat effect where the player knows its bad to go
    def fill_fire_neighbor(self,i,j):
        if self.maze_array[i][j] == 1:
            self.maze_array[i][j] = 100

    def highlight_cur_node(self, i ,j, color):
        self.m.player_movement(i, j , color, "open")

    def current_node(self,q_v,q_l_v,i,j):
        q_v.append([i,j])   # queues visited # not really used - might use it in future - self.q_visited.append([i,j])
        q_l_v.append([i,j]) # queue of all list of visited nodes - self.q_list_of_visited_nodes.append([i,j])

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