import os
import sys
import time

import pygame

from config.settings import (
    BOARD_SIZE, BLANK_COUNT, WINDOW_HEIGHT, WINDOW_WIDTH, CLICK_SOUND_PATH,
    CORRECT_SOUND_PATH, MUSIC_PATH, GAME_BANNER, COLOR_WHITE, COLOR_BLACK, QUIT_EVENT, SOLVE_KEY, RESET_KEY,
    PLAY_AGAIN_YES, PLAY_AGAIN_NO, PLAY_AGAIN_FONT_SIZE, PLAY_AGAIN_MESSAGE
)
from core.entities.grid import Grid
from core.logic.sudoku_solver import SudokuSolver
from gui.render import redraw_window
from use_cases.sudoku_generator import SudokuGenerator


def initialize_pygame():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def load_sounds():
    pygame.mixer.music.load(resource_path(MUSIC_PATH))
    pygame.mixer.music.play(-1)
    click_sound = pygame.mixer.Sound(resource_path(CLICK_SOUND_PATH))
    correct_sound = pygame.mixer.Sound(resource_path(CORRECT_SOUND_PATH))
    return click_sound, correct_sound


def create_game_window():
    pygame.display.set_caption(GAME_BANNER)
    return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def generate_new_game(win):
    sudoku_board_generator = SudokuGenerator(BOARD_SIZE, BLANK_COUNT)
    sudoku_board_generator.generate_board()
    board = sudoku_board_generator.board
    grid = Grid(BOARD_SIZE, BOARD_SIZE, WINDOW_WIDTH, WINDOW_WIDTH, board, win)
    return grid, board


def handle_events(grid, click_sound, correct_sound, strikes):
    key = None
    run = True
    for event in pygame.event.get():
        if event.type == QUIT_EVENT:
            return False, key, strikes

        if event.type == pygame.KEYDOWN:
            run, key, strikes = handle_keydown(event, grid, correct_sound, strikes)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked = grid.click(pos)
            if clicked:
                click_sound.play()
                grid.select(clicked[0], clicked[1])
                key = None

    return run, key, strikes


def handle_keydown(event, grid, correct_sound, strikes):
    key = None
    run = True
    if event.key in range(pygame.K_1, pygame.K_9 + 1):
        key = event.key - pygame.K_0
    elif event.key == pygame.K_DELETE:
        grid.clear()
    elif event.key == pygame.K_RETURN:
        run = handle_return_key(grid, correct_sound)
    elif event.key == SOLVE_KEY:
        run = handle_solve_key(grid)
    elif event.key == RESET_KEY:
        grid.reset(grid.board)

    return run, key, strikes


def handle_return_key(grid, correct_sound):
    i, j = grid.selected
    if grid.cubes[i][j].temp != 0:
        if grid.place(grid.cubes[i][j].temp):
            correct_sound.play()
            if grid.is_finished():
                return ask_to_play_again(grid)
    return True


def handle_solve_key(grid):
    SudokuSolver.solve_live(grid)
    if grid.is_finished():
        return ask_to_play_again(grid)
    return True


def ask_to_play_again(grid):
    font = pygame.font.SysFont(None, PLAY_AGAIN_FONT_SIZE)
    grid.win.fill(COLOR_WHITE)
    text = font.render(PLAY_AGAIN_MESSAGE, True, COLOR_BLACK)
    grid.win.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT_EVENT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == PLAY_AGAIN_YES:
                    return True
                elif event.key == PLAY_AGAIN_NO:
                    return False


def update_game_state(grid, key):
    if grid.selected and key is not None:
        grid.sketch(key)


def main():
    initialize_pygame()
    click_sound, correct_sound = load_sounds()
    win = create_game_window()
    grid, board = generate_new_game(win)

    run = True
    start_time = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start_time)
        run, key, strikes = handle_events(grid, click_sound, correct_sound, strikes)
        update_game_state(grid, key)
        redraw_window(grid, play_time, strikes)
        pygame.display.update()

        if grid.is_finished() and run:
            grid, board = generate_new_game(win)
            start_time = time.time()

    pygame.quit()