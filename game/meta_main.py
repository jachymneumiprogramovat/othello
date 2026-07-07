import pathlib
import sys
import os

from loguru import logger

from ai_main import ai_main
from normal_main import normal_main

def correct_input(input_value):
    try:
        input_value = int(input_value)
        if input_value in [1,2]:
            return True
        print('Dej mi číslo mezi 1,2 bro')
        return False
    except:
        print('Dej mi číslo kkt')
        return False
        
def main():
    game_mode = input('1. Hra s fyzickým kamarádem \n 2. Hra s AI kamarádem \n ')

    while not correct_input(game_mode):
        game_mode = input('1. Hra s fyzickým kamarádem \n 2. Hra s AI kamarádem \n ')

    if game_mode==1:
        normal_main()
    else:
        ai_main()



if __name__ == "__main__":
    base_dir = pathlib.Path(__file__).parent.resolve()
    logger.remove()
    info_filter = lambda record: record["level"].name == "INFO"
    success_filter = lambda record: record["level"].name == "SUCCESS"
    error_filter = lambda record: record["level"].name == "ERROR"

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
    main()
