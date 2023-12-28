# 2048 Main File
# Currently being used for production testing

# Python Modules
from random import randint

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
    # game.grid[0][2] = GameCell(2, 0, 4)
    # for _ in range(10):
    #     if not game.generate_tile():
    #         break
    
    moves = ['r', 'd', 'd', 'd']

    perform_moves(board, moves)

def test2(board: GameBoard):
    board.grid[0][2] = GameCell(2, 0, 8)
    for _ in range(10):
        board.generate_tile()
    print('BEFORE')
    board.print_board()

    print('UP')
    board.print_board(board.get_rotated_board(Direction.UP))

    print('LEFT')
    board.print_board(board.get_rotated_board(Direction.LEFT))

    print('RIGHT')
    board.print_board(board.get_rotated_board(Direction.RIGHT))

if __name__ == '__main__':
    board = GameBoard()
    test1(board)