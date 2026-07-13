import numpy as np

NUM_HIDDEN = 3
NUM_CHANNELS = 128
rows = 8
cols = 8
INPUT_CHANNELS = 2

EXPLORATION = 1

TEMPERATURE = 1

DEFAULT_BOARD = np.array([
  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0, -1,  1,  0,  0,  0,
  0,  0,  0,  1, -1,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0])

ROLLOUT_COUNT = 100
