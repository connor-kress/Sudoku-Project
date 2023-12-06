import math
import random
from typing import Iterable, Iterator

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/
"""


def flatten(__data: Iterable[Iterable]) -> Iterator:
    for row in __data:
        for val in row:
            yield val


class SudokuGenerator:
    def __init__(self, row_length: int = 9, removed_cells: int = 0) -> None:
        """create a sudoku board - initialize class variables
        and set up the 2D board.
        This should initialize:
        - `self.row_length`		- the length of each row
        - `self.removed_cells`	- the total number of cells to be removed
        - `self.board`			- a 2D list of ints to represent the board
        - `self.box_length`		- the square root of row_length

        ### Parameters:
        - `row_length` - is the number of rows/columns of the board (always 9 for this project)
        - `removed_cells` - is an integer value - the number of cells to be removed
        """
        self.row_length = row_length
        self.removed_cells = min(removed_cells, row_length**2)
        box_length = math.sqrt(row_length)
        if not box_length.is_integer():
            raise ValueError('`row_length` must be a perfect square.')
        self.box_length = int(box_length)
        self.board = [[0 for _ in range(row_length)]
                         for _ in range(row_length)]

    def get_board(self) -> list[list[int]]:
        """Returns a 2D python list of numbers which represents the board.
        # Pointless Java Boilerplate in the Wrong Language
        """
        return self.board

    def __str__(self) -> str:
        return '\n'.join(
            ' '.join(str(val) if val else '-' for val in row)
            for row in self.board
        )

    def box_start(self, row: int, col: int) -> tuple[int, int]:
        """Returns the 2D index of the start of
        the box of the cell with index (row, col).
        """
        return (row - row%self.box_length,
                col - col%self.box_length)

    def box(self, row: int, col: int) -> list[list[int]]:
        """Returns the box that the cell with index (row, col) is in."""
        row_start, col_start = self.box_start(row, col)
        row_end = row_start + self.box_length
        col_end = col_start + self.box_length
        return [row[col_start:col_end] for row in self.board[row_start:row_end]]
    
    def valid_in_row(self, row: int, num: int) -> bool:
        """Determines if num is contained in the specified row
        (horizontal) of the board. If num is already in the
        specified row, return False. Otherwise, return True.

        ### Parameters:
        - `row` is the index of the row we are checking
        - `num` is the value we are looking for in the row
        """
        return num not in self.board[row]

    def valid_in_col(self, col: int, num: int) -> bool:
        """Determines if num is contained in the specified column
        (vertical) of the board. If num is already in the specified
        col, return False. Otherwise, return True.

        ### Parameters:
        - `col` is the index of the column we are checking
        - `num` is the value we are looking for in the column
        """
        return num not in tuple(zip(*self.board))[col]

    def valid_in_box(self, row: int, col: int, num: int) -> bool:
        """Determines if num is contained in the 3x3 box specified on the board
        If num is in the specified box starting at (row_start, col_start), return False.
        Otherwise, return True

        ### Parameters:
        - `row` and `col` are the indices of a cell in the box to check
        - `num` is the value we are looking for in the box
        """
        return num not in flatten(self.box(row, col))
    
    def is_valid(self, row: int, col: int, num: int) -> bool:
        """Determines if it is valid to enter num at (row, col) in the board
        This is done by checking that num is unused in the appropriate, row, column, and box

        ### Parameters:
        row and col are the row index and col index of the cell to check in the board
        num is the value to test if it is safe to enter in this cell
        """
        box_row, box_col = self.box_start(row, col)
        return self.valid_in_row(row, num)\
           and self.valid_in_col(col, num)\
           and self.valid_in_box(box_row, box_col, num)

    def fill_box(self, row_start: int, col_start: int) -> None:
        """Fills the specified 3x3 box with values.
        For each position, generates a random digit which has not
        yet been used in the box.

        ### Parameters:
        - `row_start` and `col_start` are the starting indices of the box to check
        i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
        """
        n = self.box_length
        arr = list(range(1, self.row_length+1))
        random.shuffle(arr)
        for i in range(n):
            for j in range(n):
                self.board[i+row_start][j+col_start] = arr.pop()
    
    def fill_diagonal(self) -> None:
        """Fills the three boxes along the main diagonal of the board
        These are the boxes which start at (0,0), (3,3), and (6,6)
        """
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    def fill_remaining(self, row: int, col: int) -> bool:
        """DO NOT CHANGE!
        Fills the remaining cells of the board
        Should be called after the diagonal boxes have been filled
        
        ### Parameters:
        - `row`, `col` specify the coordinates of the first empty (0) cell

        ### Return:
        - `boolean` (whether or not we could solve the board)
        """
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self) -> None:
        """DO NOT CHANGE!
        Constructs a solution by calling
        `fill_diagonal` and `fill_remaining`.
        """
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self) -> None:
        """Removes the appropriate number of cells from the board
        This is done by setting some values to 0
        Should be called after the entire solution has been constructed
        i.e. after fill_values has been called
        
        ### NOTE:
        Be careful not to 'remove' the same cell multiple times
        i.e. if a cell is already 0, it cannot be removed again
        """
        idxs = tuple((i, j) for i in range(self.row_length)
                            for j in range(self.row_length))
        for i, j in random.sample(idxs, self.removed_cells):
            self.board[i][j] = 0


def generate_sudoku(size: int = 9,
                    removed: int = 0) -> list[list[int]]:
    """DO NOT CHANGE!
    Given a number of rows and number of cells to remove, this function:
    1. creates a SudokuGenerator
    2. fills its values and saves this as the solved state
    3. removes the appropriate number of cells
    4. returns the representative 2D Python Lists of the board and solution

    ### Parameters:
    - `size` is the number of rows/columns of the board (9 for this project)
    - `removed` is the number of cells to clear (set to 0)

    ### Return:
    - `list[list[Cell]]` (a 2D Python list to represent the board)
    """
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board


def main() -> None:
    sudoku = SudokuGenerator(removed_cells=20)
    sudoku.fill_values()
    sudoku.remove_cells()
    print(sudoku)


if __name__ == '__main__':
    main()
