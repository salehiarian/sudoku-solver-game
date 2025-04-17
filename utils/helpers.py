from tkinter import messagebox
import tkinter as tk

from config.settings import TK_TOPMOST_ATTRIBUTE


def format_time(seconds: int) -> str:
    """
    Format time in seconds to a MM:SS string format.
    :param seconds: Time in seconds.
    :return: Formatted time string.
    """
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

def show_message_box(subject: str, content: str):
    """
    Display a message box with a given subject and content.
    :param subject: Title of the message box.
    :param content: Content of the message box.
    """
    root = tk.Tk()
    root.attributes(TK_TOPMOST_ATTRIBUTE, True)
    root.withdraw()  # Hide the root window
    try:
        messagebox.showinfo(subject, content)
    finally:
        root.destroy()


def is_safe_to_place(board, num, position):
    """
    Check if placing a number in a specific position is valid.
    :param board: 2D list representing the Sudoku board.
    :param num: Number to place.
    :param position: Tuple (row, col) of the position.
    :return: True if safe, False otherwise.
    """
    row, col = position

    # Check row
    if num in board[row]:
        return False

    # Check column
    if num in [board[i][col] for i in range(len(board))]:
        return False

    # Check 3x3 box
    box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_start_row, box_start_row + 3):
        for j in range(box_start_col, box_start_col + 3):
            if board[i][j] == num:
                return False

    return True


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