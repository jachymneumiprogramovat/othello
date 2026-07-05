from time import time
import numpy as np
from loguru import logger
from tqdm import tqdm

from mts import MTS
from mts_node import MTSNode
mts = MTS()
mts.train()
