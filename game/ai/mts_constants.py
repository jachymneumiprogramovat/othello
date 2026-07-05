"""Json can suck my disk"""
import numpy as np
import math 
EXPLORATION = math.sqrt(2)
ROLLOUT_COUNT = 10
SIMULATION_COUNT = 4


DEFAULT_BOARD = np.array([
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0, -1,  1,  0,  0,  0],
 [ 0,  0,  0,  1, -1,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0]])

