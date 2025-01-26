import pygame
import sys
import numpy as np

def display_sudoku_board(original_grid, solved_grid):
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 560, 560  # Added space for edges
    GRID_SIZE = 9
    CELL_SIZE = (WIDTH - 40) // GRID_SIZE  # Leave a 20px margin on each side
    FONT = pygame.font.Font(pygame.font.match_font('arial'), 36)  # More beautiful font
    LINE_COLOR = (0, 0, 0)
    BG_COLOR = (255, 255, 255)
    ORIGINAL_NUM_COLOR = (0, 0, 0)  # Black for original numbers
    SOLVED_NUM_COLOR = (0, 0, 255)  # Blue for solution numbers

    # Create the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Board")

    def draw_grid():
        screen.fill(BG_COLOR)

        # Draw the edge border
        pygame.draw.rect(screen, LINE_COLOR, (20, 20, WIDTH - 40, HEIGHT - 40), 5)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                rect = pygame.Rect(20 + col * CELL_SIZE, 20 + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, LINE_COLOR, rect, 1)

                # Render original grid numbers in black
                if original_grid[row][col] != 0:
                    num_text = FONT.render(str(original_grid[row][col]), True, ORIGINAL_NUM_COLOR)
                    screen.blit(num_text, (20 + col * CELL_SIZE + CELL_SIZE // 4, 20 + row * CELL_SIZE + CELL_SIZE // 4))
                # Render solved grid numbers in blue if not in the original grid
                elif solved_grid[row][col] != 0:
                    num_text = FONT.render(str(solved_grid[row][col]), True, SOLVED_NUM_COLOR)
                    screen.blit(num_text, (20 + col * CELL_SIZE + CELL_SIZE // 4, 20 + row * CELL_SIZE + CELL_SIZE // 4))

        # Thicker lines for 3x3 subgrids
        for i in range(1, GRID_SIZE):
            if i % 3 == 0:
                pygame.draw.line(screen, LINE_COLOR, (20, 20 + i * CELL_SIZE), (WIDTH - 20, 20 + i * CELL_SIZE), 3)
                pygame.draw.line(screen, LINE_COLOR, (20 + i * CELL_SIZE, 20), (20 + i * CELL_SIZE, HEIGHT - 20), 3)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Example usage
if __name__ == "__main__":
    original_grid = np.array([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])

    solved_grid = np.array([
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ])

    display_sudoku_board(original_grid, solved_grid)
