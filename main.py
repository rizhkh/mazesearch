import pygame as pygame
import startprgm
import numpy as np
import genData
#import random
#import alg
import time
from alg import *
from ast import literal_eval
from route import *
from sys import exit
from collections import deque

if __name__ == '__main__':
    pygame.init()  # initializes the pygame object - Required to run the window on screen
    resolution = (600, 600)  # screen resolution
    flags = pygame.DOUBLEBUF  # Dont use noframe - easier when you update the screen
    ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution,flags)  # This sets the width and height of the screen that pops up
    m = startprgm.start(ThingsToAppearOnScreen_Display)
    # m passed to start_game is for ref so no new object is called/copied instead I deal with the one I want to deal with
    flamability_rate = 1

# To run maze
    #m.start_algorithm(m, 'StrategyOne', flamability_rate) # StrategyOne , StrategyTwo, Own
    m.start_algorithm(m, 'StrategyTwo', flamability_rate) # StrategyOne , StrategyTwo, Own
    #m.start_algorithm(m, 'Own', flamability_rate) # StrategyOne , StrategyTwo, Own

#To generate graphs
    # g = genData.generateData()
    # g.avg_of_all()

# References:
# https://stackoverflow.com/questions/19882415/closing-pygame-window
# https://www.machinelearningplus.com/plots/matplotlib-tutorial-complete-guide-python-plot-examples/