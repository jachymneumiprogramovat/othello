import pathlib
import sys
import os
import platform

import pygame_gui as pui
import pygame as pg
from loguru import logger


from game.constants import *
from ai.mts_constants import *

def main():
    if platform.system() != "Linux":
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    else:
        os.environ['SDL_VIDEODRIVER'] = 'x11'

    pg.mixer.pre_init(44100, -16, 2, 2048)
    # Initing pygame
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT),pg.SRCALPHA)
    pg.display.set_caption(CAPTION)
    logger.success('Pygame setup')

    manager = pui.UIManager((WIDTH, HEIGHT))

    clock = pg.time.Clock()
    
    # dispaly the question and backgroung
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(TILE_COLOR)
    screen.blit(background,(0,0))

    big_font = pg.font.Font(None, 48)
    small_font = pg.font.Font(None, 20)

    text_surface = big_font.render("Vyber si herní mód", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(400, 300))
    screen.blit(text_surface, text_rect)

    pg.display.flip()

    # choosing the game mode
    mode_choosen = False
    should_run = True
    modes = ['Human vs. Human', 'Human vs. AI']
    mode = None

    ROLLOUT_CONT=100
    SIMULATION_COUNT=5
    
    buttons = [
            pui.elements.UIButton(relative_rect=pg.Rect((150+i*300, 450), (150, 50)),
                                             text=text,
                                             manager=manager)
            for i,text in enumerate(modes) ]
    rollout_field = pui.elements.UITextEntryLine(
    relative_rect=pg.Rect((525, 550), (100, 50)),
    manager=manager,
    initial_text=str(ROLLOUT_CONT)
    )
    rollout_field.set_allowed_characters('numbers')

    rollout_text = small_font.render("Rollout count", True, (255, 255, 255))
    rollout_rect= rollout_text.get_rect(center=(460, 580))
    screen.blit(rollout_text,rollout_rect)

    simulation_field = pui.elements.UITextEntryLine(
    relative_rect=pg.Rect((525, 650), (100, 50)),
    manager=manager,
    initial_text=str(SIMULATION_COUNT)
    )
    simulation_field.set_allowed_characters('numbers')

    simulation_text = small_font.render("Simulation count", True, (255, 255, 255))
    simulation_rect= simulation_text.get_rect(center=(460, 680))
    screen.blit(simulation_text,simulation_rect)

    while not mode_choosen and should_run :

        time_delta = clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                should_run = False

            if event.type == pui.UI_BUTTON_PRESSED:
                if event.ui_element in buttons:
                    mode = buttons.index(event.ui_element)
                    mode_choosen = True

            if event.type == pui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == rollout_field:
                    print(f"User typed: {event.text}")
                    ROLLOUT_CONT= int(event.text)

            if event.type == pui.UI_TEXT_ENTRY_FINISHED:
                if event.ui_element == simulation_field:
                    print(f"User typed: {event.text}")
                    SIMULATION_COUNT = int(event.text)

            manager.process_events(event)


        manager.update(time_delta)
        manager.draw_ui(screen)
        pg.display.update()

    from ai_main import ai_main
    from normal_main import normal_main
    if mode_choosen:
        logger.info(f'Byl vybrán mód {modes[mode]}')
        if mode==0:
            normal_main(screen)
        else:
            ai_main(
                screen,
                simulation_count=SIMULATION_COUNT,
                rollout_count=ROLLOUT_CONT
            )





if __name__ == "__main__":
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
    # logger.add(
    #     sys.stdout,
    #     colorize=True,
    #     format="<green>{file}/{function}/{line}</green> <level>{message}</level>",
    #     filter=info_filter,
    # )
    logger.add(
        os.path.join(base_dir, "main.log"),
        colorize=True,
        format="<yellow>{file} {message} </yellow>",
        filter=success_filter
    )
    # logger.add(
    #     sys.stdout,
    #     colorize=True,
    #     format="<yellow>{file} {message} </yellow>",
    #     filter=success_filter
    # )
    logger.add(
        os.path.join(base_dir, "main.log"),
        colorize=True,
        format="<red>{file}/{function}/{line} {message}</red>",
        filter=error_filter,
    )
    # logger.add(
    #     sys.stdout,
    #     colorize=True,
    #     format="<red>{file}/{function}/{line} {message}</red>",
    #     filter=error_filter,
    # )
    logger.add(
        os.path.join(base_dir, "main.log"),
        colorize=True,
        format="<green>{file}/{function}/{line} {message}</green>",
        filter=debug_filter,
    )
    # logger.add(
    #     sys.stdout,
    #     colorize=True,
    #     format="<green>{file}/{function}/{line} {message}</green>",
    #     filter=debug_filter,
    # )
    main()
