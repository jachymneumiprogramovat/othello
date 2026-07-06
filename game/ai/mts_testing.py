from time import time
import numpy as np
from loguru import logger
from tqdm import tqdm

from mts import MTS
from mts_node import MTSNode

mts = MTS()
root = MTSNode(board = np.array([
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
            ]),player=-1,move=None)
mts.rollout(root=root)
print(mts.select_best_child(root))

