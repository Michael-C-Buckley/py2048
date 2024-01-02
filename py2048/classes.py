# 2048 Classes Module

# Python Modules
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from random import randint


class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @classmethod
    def get_inverse(cls, direction: 'Direction') -> 'Direction':
        direction_inversion = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return direction_inversion[direction]


@dataclass
class GameCell:
    x: int = None
    y: int = None
    value: int = None

    def __repr__(self) -> str:
        return f'({self.x},{self.y}): {self.value}'
    
    def __str__(self) -> str:
        return self.value


class GameBoard:
    def __init__(self, x: int = 4, y: int = 4) -> None:
        self.grid = [[GameCell(x_pos, y_pos) for x_pos in range(x)] for y_pos in range(y)]
        self.last_grid = None
        self.score = 0
        self.x_length = x
        self.y_length = y

    def __repr__(self) -> str:
        return f'{self.x_length}x{self.y_length} GameBoard'
    
    # Board Management
    def print_board(self, grid = None):
        """
        Prints a representation of the board out to the console
        """
        if grid is None:
            grid = self.grid
        
        max_value = self.get_max_value(grid)
        max_width = None
        if max_value:
            max_width = len(str(max_value))
        
        for row in grid:
            row_string = '|'
            for cell in row:
                value = ' ' if cell.value is None else str(cell.value)
                value = value.rjust(max_width) if max_width else value
                row_string = f'{row_string} ({value}) '
            print(f'{row_string}|')

    def get_rotated_board(self, direction: Direction) -> list[list[GameCell]]:
        """
        Returns a transformed version of the board aligned to be iterable by row
        """
        result_map = {
            Direction.UP: lambda: [list(col) for col in zip(*self.grid[::-1])],
            Direction.DOWN: lambda: [list(reversed(col)) for col in zip(*self.grid)],
            Direction.LEFT: lambda: [row[::-1] for row in reversed(self.grid)],
            Direction.RIGHT: lambda: self.grid
        }
        return result_map[direction]()
    
    def get_row(self, index: int, direction: Direction) -> list[GameCell]:
        """
        Returns a list of `GameCell` pieces aligned with a direction and the
        index relative to the direction supplied
        """
        result_map = {
            Direction.RIGHT: lambda: self.grid[index],
            Direction.LEFT: lambda: [x for x in reversed(self.grid[index])],
            Direction.UP: lambda: [x[index] for x in reversed(self.grid)],
            Direction.DOWN: lambda: [x[index] for x in self.grid],
        }
        return result_map[direction]()
    
    def fill_grid(self, value: int|bool = None) -> None:
        """
        Fill the grid with value(s)

        Value Info:
        * `int` will fill with that value
        * `None` will clear the grid, an int will fill with that amount,
        * `True` will fill with random values between 2 and 2048
        * `False` will fill with random values, mainly for testing
        """
        case_dict = {
            True: lambda: 2**(randint(1,11)),
            False: lambda: randint(1,10000),
            None: lambda: None
        }
        
        for row in self.grid:
            for cell in row:
                if (func := case_dict.get(value)):
                    cell.value = func()
                else:
                    cell.value = value

    # Cell Management
    def get_cell(self, x: int, y: int) -> GameCell:
        """
        Returns the cell at index location
        """
        if x+1 > self.x_length or x < 0:
            return None
        if y+1 > self.y_length or y < 0:
            return None
        return self.grid[y][x]
    
    def set_cell(self, x: int, y: int, value: int) -> GameCell:
        """
        Method for setting cell attributes at a location
        """
        cell = self.grid[y][x]
        cell.value = value
        return cell
    
    def move_pieces(self, direction: Direction) -> bool:
        """
        Moves all the pieces of the board in a direction per 2048's rules
        """

        if not self.check_valid_move(direction):
            return False

        self.last_grid = deepcopy(self.grid)
        dx, dy = direction.value
        limit = self.x_length if dx else self.y_length

        for row_index in range(0, limit):
            row = self.get_row(row_index, direction)

            row_values: list[int] = []
            for cell in row:
                if cell.value is not None:
                    row_values.append(cell.value)

            # Condense adjacent values
            for i, value in enumerate(row_values):
                if i+1 < len(row_values): 
                    if value == row_values[i+1]:
                        row_values[i] = value + row_values.pop(i+1)
                
            # reiterate, translate values
            for cell in reversed(row):
                if row_values:
                    cell.value = row_values.pop(0)
                else:
                    cell.value = None
        return True

    def undo(self):
        """
        Undoes the last move
        """
        if self.last_grid is None:
            return
        
        self.grid = self.last_grid
        self.last_grid = None

    def generate_tile(self, value: int = None) -> bool:
        """
        Generates a tile randomly on an empty tile of the board.
        Follows the pattern of 90% being 2 and 10% being 4.
        """
        if value is None:
            value = 4 if randint(1,10) == 10 else 2

        self.score = self.score + value

        empty_cells: list[GameCell] = []
        occupied_cells: list[GameCell] = []

        for row in self.grid:
            for cell in row:
                if cell.value is None:
                    empty_cells.append(cell)
                else:
                    occupied_cells.append(cell)

        if empty_cells:
            random = randint(0, len(empty_cells)) - 1
            random_cell = empty_cells[random]
            random_cell.value = value
            return True
        else:
            return False
        
    # Status
    def get_max_value(self, grid = None) -> int:
        """
        Scans the board and returns the maximum value found
        """
        if grid is None:
            grid = self.grid

        max_value = 0
        
        for row in self.grid:
            for cell in row:
                if cell.value:
                    if cell.value > max_value:
                        max_value = cell.value

        return max_value

    def check_valid_move(self, direction: Direction, end: bool = False) -> bool:
        """
        Returns bool on if a directional move will change the board for 
        determining if the game has concluded
        """

        rows_len = self.x_length if direction.value[0] else self.y_length

        for i in range(rows_len):
            row = self.get_row(i, direction)
            row_values = self.get_row_values(row, False)

            # First criteria is any empty space encountered
            if end:
                if None in row_values:
                    return True

            # Can the existing pieces move
            found_none = False
            for row_value in reversed(row_values):
                if row_value is None:
                    found_none = True
                elif row_value is not None and found_none:
                    return True
            
            row_value_numbers = [i for i in row_values if not None]

            for i, row_value in enumerate(row_value_numbers):
                if row_value is None:
                    continue
                if i+1 == len(row_value_numbers):
                    break
                if row_value == row_value_numbers[i+1]:
                    return True
        
        return False
    
    def check_game_over(self) -> bool:
        """
        Performs checks on each move direction to determine if the game is over
        """
        for direction in Direction:
            if self.check_valid_move(direction, True):
                return False
        return True


    def get_row_values(self, row: list[GameCell],
                       condensed: bool = True) -> list[int]:
        """
        Returns a list of the values of the row.
        `condensed` removes `None` and just returns the real values.
        """
        row_values: list[int] = []
        for cell in row:
            if not cell.value:
                if condensed:
                   continue
            row_values.append(cell.value)
        return row_values 