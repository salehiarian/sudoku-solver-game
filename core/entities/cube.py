import pygame
from config.settings import (
    BOARD_SIZE,
    FONT_NAME,
    FONT_SIZE,
    COLOR_GRAY,
    COLOR_BLACK,
    COLOR_WHITE,
    COLOR_RED,
    COLOR_GREEN, CELL_BORDER_WIDTH, COLOR_BLUE,
)


class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        """Draw the cube on the window."""
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        gap = self.width / BOARD_SIZE
        x, y = self._calculate_position(gap)

        if self.temp != 0 and self.value == 0:
            self._draw_text(win, font, str(self.temp), COLOR_GRAY, x + 5, y + 5)
        elif self.value != 0:
            self._draw_centered_text(win, font, str(self.value), COLOR_BLACK, x, y, gap)

        if self.selected:
            self._draw_border(win, COLOR_BLUE, x, y, gap)

    def draw_change(self, win, check):
        """Draw the cube with changes."""
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        gap = self.width / BOARD_SIZE
        x, y = self._calculate_position(gap)

        self._draw_background(win, COLOR_WHITE, x, y, gap)
        self._draw_centered_text(win, font, str(self.value), COLOR_BLACK, x, y, gap)

        border_color = COLOR_GREEN if check else COLOR_RED
        self._draw_border(win, border_color, x, y, gap)

    def set(self, val):
        """Set the permanent value of the cube."""
        self.value = val

    def set_temp(self, val):
        """Set the temporary value of the cube."""
        self.temp = val

    def _calculate_position(self, gap):
        """Calculate the x and y position of the cube."""
        x = self.col * gap
        y = self.row * gap
        return x, y

    @staticmethod
    def _draw_text(win, font, text, color, x, y):
        """Draw text at a specific position."""
        rendered_text = font.render(text, True, color)
        win.blit(rendered_text, (x, y))

    @staticmethod
    def _draw_centered_text(win, font, text, color, x, y, gap):
        """Draw text centered within the cube."""
        rendered_text = font.render(text, True, color)
        win.blit(
            rendered_text,
            (
                x + (gap / 2 - rendered_text.get_width() / 2),
                y + (gap / 2 - rendered_text.get_height() / 2),
            ),
        )

    @staticmethod
    def _draw_border(win, color, x, y, gap):
        """Draw a border around the cube."""
        pygame.draw.rect(win, color, (x, y, gap, gap), CELL_BORDER_WIDTH)

    @staticmethod
    def _draw_background(win, color, x, y, gap):
        """Draw the background of the cube."""
        pygame.draw.rect(win, color, (x, y, gap, gap), 0)