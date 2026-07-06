from time import time

from time import time
import numpy as np
from loguru import logger
from tqdm import tqdm

from ai.mts import MTS
from ai.mts_node import MTSNode

mts = MTS()
root = MTSNode(board = np.array([
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  -1,  1,  0,  0,  0],
            [ 0,  0,  0,  1,  -1,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
            ]),player=1,move=None)
for i in range(10):
    print(i)
    mts.rollout(root=root)
print(root.children)
child = mts.select_best_child(root)
print(child.board,child.move)


