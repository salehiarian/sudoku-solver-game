import math
import random
from core.logic.sudoku_solver import SudokuSolver
from utils.helpers import print_board


class SudokuGenerator:
    """
    A class to represent the Sudoku generator.
    """

    def __init__(self, grid_size, blanks_count):
        """
        Initialize the Sudoku game.
        :param grid_size: Size of the Sudoku grid (e.g., 9 for a 9x9 grid).
        :param blanks_count: Number of blank cells to remove for the puzzle.
        """
        if not math.isqrt(grid_size) ** 2 == grid_size:
            raise ValueError("Grid size must be a perfect square (e.g., 4, 9, 16).")
        if not (0 <= blanks_count <= grid_size * grid_size - 17):
            raise ValueError("Blanks count must be between 0 and the total number of cells minus 17.")

        self.grid_size = grid_size
        self.blanks_count = blanks_count
        self.board = None

    def generate_board(self):
        while True:
            self._generate_random_board()
            if SudokuSolver.solve([row[:] for row in self.board]):
                break

    def _generate_random_board(self):
        """
        Generate a Sudoku puzzle by filling the board and removing blanks.
        """
        self.board = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self._fill_diagonal_subgrids()
        self._fill_remaining_cells()
        self._remove_blank_cells()

    def _fill_diagonal_subgrids(self):
        """
        Fill the diagonal subgrids of the Sudoku board.
        """
        subgrid_size = int(self.grid_size ** 0.5)
        for i in range(0, self.grid_size, subgrid_size):
            self._fill_subgrid(i, i)

    def _fill_subgrid(self, start_row, start_col):
        """
        Fill a single subgrid with unique numbers.
        :param start_row: Starting row of the subgrid.
        :param start_col: Starting column of the subgrid.
        """
        subgrid_size = int(self.grid_size ** 0.5)
        nums = list(range(1, self.grid_size + 1))
        random.shuffle(nums)
        for i in range(subgrid_size):
            for j in range(subgrid_size):
                self.board[start_row + i][start_col + j] = nums.pop()

    def _fill_remaining_cells(self):
        """
        Fill the remaining cells of the Sudoku board using the solver.
        """
        SudokuSolver.solve(self.board)

    def _remove_blank_cells(self):
        """
        Remove a specified number of cells to create the puzzle, ensuring
        that blanks are evenly distributed across the board.
        """
        region_size = int(self.grid_size ** 0.5)
        blanks_per_region = self.blanks_count // (region_size * region_size)
        extra_blanks = self.blanks_count % (region_size * region_size)

        blanks = set()

        # Distribute blanks evenly across regions
        for region_row in range(region_size):
            for region_col in range(region_size):
                region_blanks = blanks_per_region
                if extra_blanks > 0:
                    region_blanks += 1
                    extra_blanks -= 1

                region_cells = [
                    (region_row * region_size + r, region_col * region_size + c)
                    for r in range(region_size)
                    for c in range(region_size)
                ]
                random.shuffle(region_cells)

                for _ in range(region_blanks):
                    row, col = region_cells.pop()
                    self.board[row][col] = 0
                    blanks.add((row, col))

        self.blank_positions = list(blanks)

    def _print_board(self):
        """
        Print the Sudoku board in a readable format.
        """
        print_board(self.board)