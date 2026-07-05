from time import time
import numpy as np
from loguru import logger
from tqdm import tqdm
import pathlib
import sys
import os
import math 

from ai.mts import MTS
from ai.mts_node import MTSNode

mts = MTS()
root = mts.train()
logger.remove()

print(root.board)
best_child = mts.select_best_child(root)
for child in root.children:
    print('dite')
    print(child.board)
    print(child.results,child.visited,child.calculate_score(math.log(root.visited)))
print('nejlepsi dite je')
print(best_child.board,best_child.results)

best_child = mts.select_best_child(best_child)
print('printuju vystup')
for child in best_child.children:
    print(child.results)
print(best_child.board,best_child.results,child.visited)



if __name__ == "__main__":
    logger.remove()
    base_dir = pathlib.Path(__file__).parent.resolve()
    logger.remove()
    logger.add(
        os.path.join(base_dir, "mts.log"),
        colorize=True,
        format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
        level="INFO",
    )
    logger.add(
        sys.stdout,
        format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
        level="INFO",
    )

