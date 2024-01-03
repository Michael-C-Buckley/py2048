import pygame
from py2048.classes import GameBoard, Direction

# Official 2048 colors
hex_color_map = {
    None: '#cdc1b4',
    2: '#eee4da',
    4: '#ede0c8',
    8: '#f2b179',
    16: '#f59563',
    32: '#f67c5f',
    64: '#f65e3b',
    128: '#edcf72',
    256: '#edcc61',
    512: '#edc850',
    1024: '#edc53f',
    2048: '#edc22e',
}

def hex_to_rgb(color_input: str) -> tuple[int, int, int]:
    """
    Converts hex color codes to RGB color codes
    """
    color_input = color_input.lstrip('#')
    return tuple(int(color_input[i:i+2], 16) for i in (0, 2, 4))

# Constants
SCREEN_SIZE = 600
TILE_SIZE = SCREEN_SIZE // 4
TILE_COLORS = {k:hex_to_rgb(v) for k,v in hex_color_map.items()}
BACKGROUND_COLOR = TILE_COLORS.get(None)

pygame.init()
game_board = GameBoard(4, 4)
# game_board.generate_tile()
for i in range(3):
    game_board.set_cell(i, 0, 2)
game_board.set_cell(3, 0, 4)

# Set up the display
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048')
tile_font = pygame.font.SysFont('arial', 36)
score_font = pygame.font.SysFont('arial', 18)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key_mapping = {
                pygame.K_UP: Direction.UP,
                pygame.K_DOWN: Direction.DOWN,
                pygame.K_LEFT: Direction.LEFT,
                pygame.K_RIGHT: Direction.RIGHT,
            }
            if event.key == pygame.K_z:
                game_board.undo()
            elif event.key in key_mapping:
                if not game_board.move_pieces(key_mapping[event.key]):
                    continue
                game_board.generate_tile()
                
                if game_board.check_game_over():
                    print(f'GAME OVER - Final Score: {game_board.score}')
                    running = False
                    

    # Draw the game board
    screen.fill(BACKGROUND_COLOR)
    for y, row in enumerate(game_board.grid):
        for x, cell in enumerate(row):
            tile_color = TILE_COLORS.get(cell.value)
            pygame.draw.rect(screen, tile_color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            # Draw the number on the tile
            if cell.value is not None:
                text_surface = tile_font.render(str(cell.value), True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

    # Score Display
    score_surface = score_font.render(f'Score: {game_board.score}', True, (0, 0, 0))
    score_rect = score_surface.get_rect(topright=(SCREEN_SIZE - 20, 10))
    screen.blit(score_surface, score_rect)

    pygame.display.flip()

pygame.quit()
