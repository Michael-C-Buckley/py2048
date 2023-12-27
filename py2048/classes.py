# 2048 Classes Module

# Python Modules
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
        self.x_length = x
        self.y_length = y
    
    # Board Management
    def print_board(self, grid = None):
        if grid is None:
            grid = self.grid
        for row in grid:
            row_string = '|'
            for cell in row:
                value = ' ' if cell.value is None else cell.value
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

    # Cell Management
    def get_cell(self, x: int, y: int) -> GameCell:
        if x+1 > self.x_length or x < 0:
            return None
        if y+1 > self.y_length or y < 0:
            return None
        return self.grid[y][x]
    
    def set_cell(self, x: int, y: int, value: int) -> GameCell:
        cell = self.grid[y][x]
        cell.value = value
        return cell
    
    def shift_piece(self, cell: GameCell, direction: Direction):
        dx, dy = direction.value
        if (new_cell := self.get_cell(cell.x + dx, cell.y + dy)):
            if not new_cell.value:
                new_cell.value = cell.value
                cell.value = None
                # print(f'Move {cell.x},{cell.y} to {new_cell.x},{new_cell.y}')
                self.shift_piece(new_cell, direction)
            else:
                if cell.value == new_cell.value:
                    new_cell.value = new_cell.value * 2
                    cell.value = None
        
    def move_pieces(self, direction: Direction):
        """"""
        dx, dy = direction.value
        limit = self.x_length if dx else self.y_length

        for row_index in range(0, limit):
            row = self.get_row(row_index, direction)

            row_values: list[int] = []
            for cell in reversed(row):
                if cell.value is not None:
                    row_values.append(cell.value)

            # Condense adjacent values
            for i, value in enumerate(row_values):
                if i < len(row_values): 
                    if value == row_values[i+1]:
                        row_values[i] = value + row_values.pop(i+1)
                
            # reiterate, translate values
            for cell in reversed(row):
                if row_values:
                    cell.value = row_values.pop()
                else:
                    cell.value = None

    def generate_tile(self, value: int = 2):
        empty_cells: list[GameCell] = []
        occupied_cells: list[GameCell] = []
        for row in self.grid:
            for cell in row:
                if cell.value is None:
                    empty_cells.append(cell)
                else:
                    occupied_cells.append(cell)

        random = randint(0, len(empty_cells)) - 1
        random_cell = empty_cells[random]
        random_cell.value = value
