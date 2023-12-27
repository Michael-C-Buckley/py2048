# 2048 Main File
# Currently being used for production testing

# Local Modules
from py2048.classes import GameBoard, GameCell, Direction

def test1(game: GameBoard):
    for i in range(4):
        for j in range(2):
            game.grid[i][j] = GameCell(j, i, 2)
    game.grid[0][2] = GameCell(2, 0, 4)
    # for _ in range(10):
    #     if not game.generate_tile():
    #         break
    print('BEFORE')
    game.print_board()

    game.move_pieces(Direction.RIGHT)
    print('STEP 1')
    game.print_board()
    print('AFTER')
    game.move_pieces(Direction.DOWN)
    game.print_board()

def test2(game: GameBoard):
    game.grid[0][2] = GameCell(2, 0, 8)
    for _ in range(10):
        game.generate_tile()
    print('BEFORE')
    game.print_board()

    print('UP')
    game.print_board(game.get_rotated_board(Direction.UP))

    print('LEFT')
    game.print_board(game.get_rotated_board(Direction.LEFT))

    print('RIGHT')
    game.print_board(game.get_rotated_board(Direction.RIGHT))

if __name__ == '__main__':
    game = GameBoard()
    test1(game)