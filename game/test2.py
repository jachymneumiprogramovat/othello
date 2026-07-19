from tqdm import tqdm
import pathlib
import os
import sys
from loguru import logger
import torch


base_dir = pathlib.Path(__file__).parent.resolve()
logger.remove()
info_filter = lambda record: record["level"].name == "INFO"
success_filter = lambda record: record["level"].name == "SUCCESS"
error_filter = lambda record: record["level"].name == "ERROR"
debug_filter = lambda record: record["level"].name == "DEBUG"

logger.add(
    os.path.join(base_dir, "main.log"),
    colorize=True,
    format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
    filter=info_filter,
)
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
    filter=info_filter,
)
logger.add(
    os.path.join(base_dir, "main.log"),
    colorize=True,
    format="<yellow>{file} {message} </yellow>",
    filter=success_filter
)
logger.add(
    sys.stdout, 
    colorize=True,
    format="<yellow>{file} {message} </yellow>",
    filter=success_filter
)
logger.add(
    os.path.join(base_dir, "main.log"),
    colorize=True,
    format="<red>{file}/{function}/{line} {message}</red>",
    filter=error_filter,
)
logger.add(
    sys.stdout,
    colorize=True,
    format="<red>{file}/{function}/{line} {message}</red>",
    filter=error_filter,
)
# logger.add(
#     os.path.join(base_dir, "main.log"),
#     colorize=True,
#     format="<green>{file}/{function}/{line} {message}</green>",
#     filter=debug_filter,
# )
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{file}/{function}/{line} {message}</green>",
    filter=debug_filter,
)


from alphazero.alpha_mcts import AMCTS
from alphazero.model import Model
from alphazero.state import State
from alphazero.alpha_constants import *
from alphazero.alpha_zero import AlphaZero

board = [0, np.zeros(64), np.zeros(64)]
board[-1][3*8 + 3] = 1
board[-1][4*8+4]=1

board[1][3*8+4]=1
board[1][4*8+3]=1


model = Model(num_channels=NUM_CHANNELS,num_hidden=NUM_HIDDEN,device='cpu')

root = State(board=board,player=1,move=None,parent=None)

alphazero = AlphaZero(model=model)

for _ in tqdm(range(10)):
    alphazero.selfplay()

