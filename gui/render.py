import pygame

from config.settings import COLOR_WHITE, COLOR_BLACK, TIME_TEXT_POSITION, COLOR_RED, STRIKES_TEXT_POSITION, FONT_NAME, \
    FONT_SIZE
from utils.helpers import format_time


def redraw_window(grid, time: int, strikes: int):
    """
    Redraw the game window with updated elements.
    :param grid: Grid object containing the game state.
    :param time: Current time in seconds.
    :param strikes: Number of strikes.
    """
    grid.win.fill(COLOR_WHITE)

    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    time_text = font.render(f"Time: {format_time(time)}", True, COLOR_BLACK)
    _calculate_position_and_blit(grid.win, time_text, TIME_TEXT_POSITION)

    strikes_text = font.render("X " * strikes, True, COLOR_RED)
    _calculate_position_and_blit(grid.win, strikes_text, STRIKES_TEXT_POSITION)

    grid.draw()

def _calculate_position_and_blit(win, text_surface, position):
    """
    Calculate the position and blit the text surface onto the window.
    :param win: Pygame window surface.
    :param text_surface: Rendered text surface.
    :param position: Tuple (x, y) for the position.
    """
    win.blit(text_surface, position)