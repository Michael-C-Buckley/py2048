# 2048 Main File
# Currently being used for production testing

# Python Modules
from random import randint

# Third-Party Modules
# from icecream import ic

# Local Modules
from py2048.classes import GameBoard, GameCell, Direction

def convert_string_to_move(input_str: str):
    conversion_map = {
        'r': Direction.RIGHT,
        'u': Direction.UP,
        'd': Direction.DOWN,
        'l': Direction.LEFT
    }
    return conversion_map[input_str]

def perform_moves(board: GameBoard, moves: list[Direction]) -> None:
    """
    Perform a series of moves
    """
    print('START')
    board.print_board()

    for i, move in enumerate(moves):
        if isinstance(move, str):
            move = convert_string_to_move(move)
        print(f'STEP {i+1}')
        board.move_pieces(move)
        board.print_board()

def test1(board: GameBoard):
    for i in range(4):
        for j in range(2):
            value = 2 if j else 4
            board.set_cell(i, j, value)
    
    moves = ['r', 'd', 'd', 'd']

    perform_moves(board, moves)

def test2(board: GameBoard):
    board.fill_grid(2)
    board.print_board()
    checks = [board.check_valid_move(i) for i in Direction if i is True]
    if not checks:
        print('GAME OVER')
    else:
        print('PASSED')

def test3(board: GameBoard):
    board.fill_grid(4)
    print(board.check_game_over())

if __name__ == '__main__':
    board = GameBoard()
    # test2(board)
    test3(board)