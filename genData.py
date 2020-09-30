import matplotlib.pyplot as plt

class generateData:

    # Data from Strategy One
    def strategy_one(self):
        data_strategy_one_0 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        data_strategy_one_2 = [2, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        data_strategy_one_4 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        data_strategy_one_6 = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
        data_strategy_one_8 = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
        data_strategy_one_10 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]

        plt.figure(figsize=(7, 4))  # 10 is width, 7 is height
        plt.plot([0.0, 0.2, 0.4, 0.6, 0.8, 1],
                 [9,  8,     9,   6,   6,   5], 'go', label='Success', linestyle='-')  # success rate
        plt.plot([0.0, 0.2, 0.4, 0.6, 0.8, 1],
                 [1,   2,   1,   4,   4,   5], 'ro', label='Died')  # blocked path
        plt.title(' Strategy One')
        plt.xlabel(" 'q' flammability rate ")
        plt.ylabel('Success Rate')
        # plt.xlim(0, 10)
        # plt.ylim(0, 12)
        plt.xlim(-0.1, 1.1)
        plt.ylim(0, 10)
        plt.legend(loc='best')
        plt.show()

    # Data from Strategy Two
    def strategy_Two(self):
        data_strategy_Two_0 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        error_strategy_Two_0 = 3
        data_strategy_Two_2 = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        error_strategy_Two_2 = 5
        data_strategy_Two_4 = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        error_strategy_Two_4 = 5
        data_strategy_Two_6 = [1, 1, 1, 1, 1, 1, 1, 1, 3, 3]
        error_strategy_Two_6 = 5
        data_strategy_Two_8 = [1, 1, 1, 1, 1, 1, 3, 3, 3, 3]
        error_strategy_Two_8 = 5
        data_strategy_Two_10 = [1, 1, 1, 1, 1, 1, 3, 3, 3, 3]
        error_strategy_Two_10 = 5

        plt.figure(figsize=(7, 4))  # 10 is width, 7 is height
        plt.plot([0.0, 0.2, 0.4, 0.6, 0.8, 1],
                 [10,  9,     9,   8,   6,   6], 'go', label='Success', linestyle='-')  # success rate
        plt.plot([0.0, 0.2, 0.4, 0.6, 0.8, 1],
                 [0,   1,   2,   3,   4,   4], 'ro', label='Path Blocked To Target / Died')  # blocked path
        plt.title(' Strategy Two')
        plt.xlabel(" 'q' flammability rate ")
        plt.ylabel('Success Rate')
        # plt.xlim(0, 10)
        # plt.ylim(0, 12)
        plt.xlim(-0.1, 1.1)
        plt.ylim(0, 11)
        plt.legend(loc='best')
        plt.show()

    # Data from SSE Strategy
    def strategy_Own(self):
        data_strategy_Own_Alg_0 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        error_strategy_Two_0 = 2
        data_strategy_Own_Alg_2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        error_strategy_Two_2 = 2
        data_strategy_Own_Alg_4 = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2]
        error_strategy_Two_4 = 2
        data_strategy_Own_Alg_6 = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2]
        error_strategy_Two_6 = 3
        data_strategy_Own_Alg_8 = [1, 1, 1, 1, 1, 1, 1, 3, 3, 3]
        error_strategy_Two_8 = 3
        data_strategy_Own_Alg_10 = [1, 1, 1, 1, 1, 1, 3, 3, 3, 3]
        error_strategy_Two_10 = 3

        plt.figure(figsize=(7, 4))  # 10 is width, 7 is height
        plt.plot([0.0, 0.2, 0.4, 0.6, 0.8, 1],
                 [10,  9,     8,   8,   7,   7], 'go', label='Success', linestyle='-')  # success rate
        plt.plot([0.0, 0.2, 0.4, 0.6, 0.8, 1],
                 [0,   1,   2,   2,   3,   4], 'ro', label='Path Blocked To Target / Died', linestyle='-')  # blocked path
        plt.title(' SSE')
        plt.xlabel(" 'q' flammability rate ")
        plt.ylabel('Success Rate')
        # plt.xlim(0, 10)
        # plt.ylim(0, 12)
        plt.xlim(-0.1, 1.1)
        plt.ylim(0, 11)
        plt.legend(loc='best')
        plt.show()

    # data of avg of all strategiess
    def avg_of_all(self):
        strategy_one =  ( (9+8+9+6+6+5)/ 60) * 100
        strategy_two = ((10 + 9 + 9 + 8 + 6 + 6) / 60) * 100
        strategy_own = ((10 + 9 + 9 + 8 + 7 + 7) / 60) * 100

        plt.figure(figsize=(7, 2.5))  # 10 is width, 7 is height
        plt.plot([0, 'Strategy One' , 'Strategy Two' , 'SSE Strategy', ],
                 [-5, strategy_one,  strategy_two,     strategy_own], 'go', label='Success', linestyle='-')  # success rate
        # plt.plot([0.0, 0.2, 0.4, 0.6, 0.8, 1],
        #          [0,   1,   2,   2,   3,   4], 'ro', label='Path Blocked To Target / Died')  # blocked path
        plt.title(' Average Success Rate')
        plt.xlabel(" Avg. success rate ")
        # plt.xlim(0, 10)
        # plt.ylim(0, 12)
        plt.xlim(0, 4)
        plt.ylim(0, 100)
        plt.legend(loc='best')
        plt.show()

    # Contains all data from manual testing
    def generate_Graph(self):
        # REACHED = 1
        # DEAD = 2
        # PATH BLOCKED = 3
        data_strategy_one_0 = [2, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        data_strategy_one_2 = [2, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        data_strategy_one_4 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        data_strategy_one_6 = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
        data_strategy_one_8 = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
        data_strategy_one_10 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]



        data_strategy_Two_0 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        error_strategy_Two_0 = 3
        data_strategy_Two_2 = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        error_strategy_Two_2 = 5
        data_strategy_Two_4 = [2, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        error_strategy_Two_4 = 5
        data_strategy_Two_6 = [1, 1, 1, 1, 1, 1, 1, 1, 3, 3]
        error_strategy_Two_6 = 5
        data_strategy_Two_8 = [1, 1, 1, 1, 1, 1, 3, 3, 3, 3]
        error_strategy_Two_8 = 5
        data_strategy_Two_10 = [1, 1, 1, 1, 1, 1, 3, 3, 3, 3]
        error_strategy_Two_10 = 5



        data_strategy_Own_Alg_0 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        error_strategy_Two_0 = 2
        data_strategy_Own_Alg_2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        error_strategy_Two_2 = 2
        data_strategy_Own_Alg_4 = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2]
        error_strategy_Two_4 = 2
        data_strategy_Own_Alg_6 = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2]
        error_strategy_Two_6 = 3
        data_strategy_Own_Alg_8 = [1, 1, 1, 1, 1, 1, 1, 3, 3, 3]
        error_strategy_Two_8 = 3
        data_strategy_Own_Alg_10 = [1, 1, 1, 1, 1, 1, 3, 3, 3, 3]
        error_strategy_Two_10 = 3
