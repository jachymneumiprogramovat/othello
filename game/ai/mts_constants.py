"""Json can suck my disk"""
import numpy as np
import math 
EXPLORATION = math.sqrt(2)
ROLLOUT_COUNT = 100
SIMULATION_COUNT = 5


DEFAULT_BOARD = np.array([
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0, -1,  1,  0,  0,  0],
 [ 0,  0,  0,  1, -1,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0],
 [ 0,  0,  0,  0,  0,  0,  0,  0]])

GOODBYE_MESSAGES = ['Bro to vzdal proti AI','Trapáku','Týpka porazili nuly a jedničky','čus']
