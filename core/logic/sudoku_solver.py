import pygame
from config.logging_config import logging
from config.settings import VISUALIZATION_DELAY_MS
from utils.helpers import is_safe_to_place

class SudokuSolver:

    @staticmethod
    def solve(board):
        """
        Solve the Sudoku board using backtracking with optimizations.
        :param board: 2D list representing the Sudoku board.
        :return: True if solved, False otherwise.
        """
        candidates = SudokuSolver._initialize_candidates(board)

        return SudokuSolver._backtrack(board, candidates)


    @staticmethod
    def solve_live(grid):
            """
            Solve the Sudoku board using backtracking with live updates.
            :param grid: Grid object for rendering the board.
            :return: True if solved, False otherwise.
            """
            empty = grid.find_empty()
            if not empty:
                return True
            row, col = empty

            for num in range(1, 10):
                if is_safe_to_place(grid.model, num, (row, col)):
                    grid.model[row][col] = num
                    grid.cubes[row][col].set(num)
                    grid.update_model()
                    grid.cubes[row][col].draw_change(grid.win, True)
                    pygame.display.update()
                    pygame.time.delay(VISUALIZATION_DELAY_MS)

                    if SudokuSolver.solve_live(grid):
                        return True

                    grid.model[row][col] = 0
                    grid.cubes[row][col].set(0)
                    grid.update_model()
                    grid.cubes[row][col].draw_change(grid.win, False)
                    pygame.display.update()
                    pygame.time.delay(VISUALIZATION_DELAY_MS)

            return False

    @staticmethod
    def _initialize_candidates(board):
        """
        Initialize a dictionary of possible candidates for each empty cell.
        :param board: 2D list representing the Sudoku board.
        :return: Dictionary with cell positions as keys and sets of candidates as values.
        """
        candidates = {}
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0:
                    candidates[(row, col)] = SudokuSolver._get_candidates(board, row, col)
        return candidates

    @staticmethod
    def _get_candidates(board, row, col):
        """
        Get possible candidates for a specific cell.
        :param board: 2D list representing the Sudoku board.
        :param row: Row index of the cell.
        :param col: Column index of the cell.
        :return: Set of valid numbers for the cell.
        """
        used = set(board[row])
        used.update(board[i][col] for i in range(len(board)))

        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_start_row, box_start_row + 3):
            for j in range(box_start_col, box_start_col + 3):
                used.add(board[i][j])

        return {num for num in range(1, 10) if num not in used}

    @staticmethod
    def _backtrack(board, candidates):
        """
        Backtracking algorithm with optimizations.
        :param board: 2D list representing the Sudoku board.
        :param candidates: Dictionary of possible candidates for each empty cell.
        :return: True if solved, False otherwise.
        """
        logging.debug("Candidates: %s", candidates)

        if not SudokuSolver.is_valid_sudoku(board):
            return False

        if not candidates:
            logging.debug("No candidates left. Puzzle solved. Exiting _backtrack.")
            return True


        cell = min(candidates, key=lambda k: len(candidates[k]))
        row, col = cell
        logging.debug("Trying to solve cell (%d, %d) with candidates: %s", row, col, candidates[cell])

        for num in candidates[cell]:
            if SudokuSolver._is_safe_to_place(board, num, (row, col)):
                logging.debug("Placing number %d in cell (%d, %d)", num, row, col)
                board[row][col] = num
                new_candidates = SudokuSolver._update_candidates(candidates, cell, num)

                if SudokuSolver._backtrack(board, new_candidates):
                    return True

                logging.debug("Backtracking: Removing number %d from cell (%d, %d)", num, row, col)
                board[row][col] = 0

        logging.debug("Exiting _backtrack: No solution found for cell (%d, %d)", row, col)
        return False

    @staticmethod
    def _update_candidates(candidates, cell, num):
        """
        Update the candidates dictionary after placing a number.
        :param candidates: Current candidates' dictionary.
        :param cell: Cell where the number was placed.
        :param num: Number placed in the cell.
        :return: Updated candidates dictionary.
        """
        row, col = cell
        new_candidates = {k: v.copy() for k, v in candidates.items() if k != cell}

        for r, c in new_candidates:
            if r == row or c == col or (r // 3 == row // 3 and c // 3 == col // 3):
                new_candidates[(r, c)].discard(num)

        return {k: v for k, v in new_candidates.items() if v}

    @staticmethod
    def _is_safe_to_place(board, num, position):
        """
        Check if placing a number in a specific position is valid.
        :param board: 2D list representing the Sudoku board.
        :param num: Number to place.
        :param position: Tuple (row, col) of the position.
        :return: True if safe, False otherwise.
        """
        row, col = position

        if num in board[row]:
            return False

        if num in [board[i][col] for i in range(len(board))]:
            return False

        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_start_row, box_start_row + 3):
            for j in range(box_start_col, box_start_col + 3):
                if board[i][j] == num:
                    return False

        return True

    @staticmethod
    def print_board(board):
        """
        Print the Sudoku board in a readable format.
        :param board: 2D list representing the Sudoku board.
        """
        for row in range(len(board)):
            if row % 3 == 0 and row != 0:
                print("-" * 21)

            for col in range(len(board[0])):
                if col % 3 == 0 and col != 0:
                    print(" | ", end="")

                if col == 8:
                    print(board[row][col])
                else:
                    print(f"{board[row][col]} ", end="")

    @staticmethod
    def has_minimal_clues(board):
        """
        Check if the Sudoku board has the minimal number of clues required to solve it.
        :param board: 2D list representing the Sudoku board.
        :return: True if the board has at least 17 clues, False otherwise.
        """
        clue_count = sum(1 for row in board for cell in row if cell != 0)
        return clue_count >= 17

    @staticmethod
    def is_valid_sudoku(board):
        """
        Check if the Sudoku board is valid.
        :param board: 2D list representing the Sudoku board.
        :return: True if valid, False otherwise.
        """

        def has_duplicates(values):
            """Helper function to check for duplicates ignoring zeros."""
            values = [v for v in values if v != 0]
            return len(values) != len(set(values))

        if not SudokuSolver.has_minimal_clues(board):
            logging.debug("Board is invalid. Board does not have minimal clues.")
            return False

        for i in range(9):
            if has_duplicates(board[i]) or has_duplicates([board[j][i] for j in range(9)]):
                logging.debug("Board is invalid. Board has duplicates in row or column.")
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                subgrid = [
                    board[r][c]
                    for r in range(box_row, box_row + 3)
                    for c in range(box_col, box_col + 3)
                ]
                if has_duplicates(subgrid):
                    logging.debug("Board is invalid. Board has duplicates in 3x3 subgrid.")
                    return False

        return True


