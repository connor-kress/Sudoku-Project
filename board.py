import math
import pygame
from typing import Optional, Iterable, Iterator, TypeVar

from consts import (
    WIDTH, HEIGHT,
    LINE_THICKNESS,
    BLACK,
)
from cell import Cell
from sudoku_generator import generate_sudoku

_T = TypeVar('_T')


def flatten(__data: Iterable[Iterable[_T]]) -> Iterator[_T]:
    for row in __data:
        for val in row:
            yield val


class Board:
    def __init__(self, size: int = 9, removed: int = 0) -> None:
        """Constructor for the Board class.
        screen is a window from PyGame.
        """
        assert math.sqrt(size).is_integer()
        data = generate_sudoku(size, removed)
        self.data = data
        self.initial_state = [row.copy() for row in data]
        self.set_board(data)
        self.selection = None
    
    def set_board(self, __data: list[list[int]]) -> None:
        rows = len(__data)
        cols = len(__data[0])
        self.data = __data
        self.cells = [[Cell(val, (i, j), (rows, cols), not val)
                       for j, val in enumerate(row)]
                       for i, row in enumerate(__data)]

    def draw(self, window: pygame.Surface) -> None:
        """Draws an outline of the Sudoku grid,
        with bold lines to delineate the 3x3 boxes.
        Draws every cell on this board.
        """
        for row in self.cells:
            for cell in row:
                cell.draw(window)
        rows, cols = len(self.data), len(self.data[0])
        row_boxes, col_boxes = int(math.sqrt(rows)), int(math.sqrt(cols))
        width, height = WIDTH/cols, HEIGHT/rows
        for i in range(row_boxes+1):
            y = i * row_boxes * height
            rect = pygame.Rect(0, y-LINE_THICKNESS, WIDTH, LINE_THICKNESS*2)
            pygame.draw.rect(window, BLACK, rect)
        for j in range(col_boxes+1):
            x = j * col_boxes * width
            rect = pygame.Rect(x-LINE_THICKNESS, 0, LINE_THICKNESS*2, HEIGHT)
            pygame.draw.rect(window, BLACK, rect)

    # def selected_cell(self) -> Cell:
    #     assert self.selection is not None
    #     row, col = self.selection
    #     return self.cells[row][col]
    
    def clear_selection(self) -> None:
        """Sets the selection back to `None`."""
        if self.selection is None:
            return
        row, col = self.selection
        self.cells[row][col].selected = False
        self.selection = None
    
    def select(self, row: int, col: int) -> None:
        """Marks the cell at (row, col) in the
        board as the current selected cell.
        Once a cell has been selected, the user
        can edit its value or sketched value.
        """
        if self.selection is not None:
            old_row, old_col = self.selection
            self.cells[old_row][old_col].selected = False
        new_cell = self.cells[row][col]
        if new_cell.editable:
            # print(f'Editing {new_cell}')
            self.selection = (row, col)
            new_cell.selected = True
        else:
            # print(f'Failed to edit {new_cell}')
            self.selection = None

    def click(self, x: int, y: int) -> Optional[tuple[int, int]]:
        """If a tuple of (x, y) coordinates is within
        the displayed board, this function returns a tuple
        of the (row, col) of the cell which was clicked.
        Otherwise, this function returns `None`.
        """
        return next((cell.pos for cell in flatten(self.cells)
                     if cell.outer.collidepoint(x, y)), None)

    # def clear(self) -> None:
    #     """Clears the value cell. Note that the user can only
    #     remove the cell values and sketched value that are
    #     filled by themselves.
    #     """
    #     if self.selection is None:
    #         return
    #     row, col = self.selection
    #     self.data[row][col] = 0
    #     self.cells[row][col].clear()

    def set_current(self, __value: int) -> None:
        """Sets the value of the current selected cell equal
        to user entered value.
        Called when the user presses the Enter key.
        """
        if self.selection is None:
            return
        row, col = self.selection
        self.data[row][col] = __value
        self.cells[row][col].set_(__value)

    def reset_to_original(self) -> None:
        """Reset all cells in the board to their original values
        (0 if cleared, otherwise the corresponding digit).
        """
        self.set_board(self.initial_state)

    def is_full(self) -> bool:
        """Returns a Boolean value indicating whether
        the board is full or not.
        """
        return 0 not in flatten(self.data)

    def find_empty(self) -> Optional[tuple[int, int]]:
        """Finds an empty cell and returns its (`row`, `col`).
        Returns `None` if the board is empty.
        """
        return next(((i, j) for i, row in enumerate(self.data)
                            for j, val in enumerate(row) if not val), None)

    def is_solved(self) -> bool:
        """Returns whether the Sudoku board is solved correctly."""
        def box_works(row_start: int, col_start: int) -> bool:
            box = (row[col_start:col_start+n] for row
                   in self.data[row_start:row_start+n])
            return len(set(flatten(box))) == 9
        
        if not self.is_full():
            return False
        
        n = int(math.sqrt(len(self.data)))
        rows = len(self.data)
        cols = len(self.data[0])

        rows_work = all(len(set(row)) == cols for row in self.data)
        cols_work = all(len(set(col)) == rows for col in zip(*self.data))
        boxes_work = all(box_works(i, j) for i in range(0, rows, n)
                                         for j in range(0, cols, n))
        return rows_work and cols_work and boxes_work
