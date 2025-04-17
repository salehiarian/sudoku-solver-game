import pygame

from config.settings import COLOR_BLACK
from core.entities.cube import Cube
from core.logic.sudoku_solver import SudokuSolver

from utils.helpers import is_safe_to_place


class Grid:
    def __init__(self, rows, cols, width, height, board, win):
        """
        Initialize the Grid.
        :param rows: Number of rows in the grid.
        :param cols: Number of columns in the grid.
        :param width: Width of the grid.
        :param height: Height of the grid.
        :param win: Pygame display surface.
        """
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.board = board
        self.cubes = [
            [Cube(self.board[i][j], i, j, self.width, self.height) for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.model = None
        self.answer = None
        self.selected = None
        self.win = win
        self.update_model()
        self._solve_and_store_answer()


    def _solve_and_store_answer(self):
        """Solve the board and store the solution in self.answer."""
        self.answer = [row[:] for row in self.model]  # Create a copy of the current board
        SudokuSolver.solve(self.answer)

    def update_model(self):
        """Update the internal model of the grid based on cube values."""
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        """
        Place a value in the selected cube if valid.
        :param val: Value to place.
        :return: True if the value is valid and placed, False otherwise.
        """
        if not self.selected:
            return False

        row, col = self.selected
        if self.cubes[row][col].value == 0:
            if is_safe_to_place(self.model, val, (row, col)) and self.answer[row][col] == val:
                self.cubes[row][col].set(val)
                self.update_model()
                return True

            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        """Set a temporary value in the selected cube."""
        if self.selected:
            row, col = self.selected
            self.cubes[row][col].set_temp(val)

    def draw(self):
        """Draw the grid and its cubes."""
        self._draw_grid_lines()
        for row in self.cubes:
            for cube in row:
                cube.draw(self.win)

    def _draw_grid_lines(self):
        """Draw the grid lines."""
        gap = self.width / self.rows
        for i in range(self.rows + 1):
            thickness = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.win, COLOR_BLACK, (0, i * gap), (self.width, i * gap), thickness)
            pygame.draw.line(self.win, COLOR_BLACK, (i * gap, 0), (i * gap, self.height), thickness)

    def select(self, row, col):
        """Select a cube at the given row and column."""
        self._clear_selection()
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def _clear_selection(self):
        """Clear the selection of all cubes."""
        for row in self.cubes:
            for cube in row:
                cube.selected = False

    def clear(self):
        """Clear the temporary value of the selected cube."""
        if self.selected:
            row, col = self.selected
            if self.cubes[row][col].value == 0:
                self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        Handle a click event and return the selected cube's position.
        :param pos: (x, y) position of the click.
        :return: (row, col) of the selected cube or None if out of bounds.
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / self.rows
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        return None

    def is_finished(self):
        """Check if the grid is completely filled."""
        return all(cube.value != 0 for row in self.cubes for cube in row)

    def reset(self, board):
        """
        Reset the grid with a new board.
        :param board: New Sudoku board (2D list).
        """
        self.__init__(self.rows, self.cols, self.width, self.height, board, self.win)

    def find_empty(self):
        """Find an empty cell in the grid."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.model[i][j] == 0:
                    return i, j
        return None