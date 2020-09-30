import pygame as pygame
import startprgm
import numpy as np
import genData
import time
from alg import *
from ast import literal_eval
from route import *


if __name__ == '__main__':
    pygame.init()  # initializes the pygame object - Required to run the window on screen
    resolution = (420, 420)  # screen resolution
    flags = pygame.DOUBLEBUF
    ThingsToAppearOnScreen_Display = pygame.display.set_mode(resolution,flags)  # This sets the width and height of the screen that pops up
    m = startprgm.start(ThingsToAppearOnScreen_Display)
    flamability_rate = 0.6

# To run maze
    #m.start_algorithm(m, 'StrategyOne', flamability_rate) # StrategyOne , StrategyTwo, Own
    #m.start_algorithm(m, 'StrategyTwo', flamability_rate) # StrategyOne , StrategyTwo, Own
    m.start_algorithm(m, 'Own', flamability_rate) # StrategyOne , StrategyTwo, Own

# To generate graphs
    #g = genData.generateData()
    #g.strategy_one()
    #g.strategy_Two()
    #g.strategy_Own()
    #g.avg_of_all()
