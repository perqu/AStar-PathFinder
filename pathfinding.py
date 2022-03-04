import pygame
import function

# CONSTANTS
CELLS_AMOUNT = 50
WINDOW_SIZE = 800
CELL_SIZE = WINDOW_SIZE // CELLS_AMOUNT
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

# WINDOW NAME
pygame.display.set_caption('ASTAR by PP')

# POSITION CELLS
start_cell = None
end_cell = None

# BOLLEANS
running = True
algorithm_done = False

# CREATING GRID
grid = function.make_grid(CELLS_AMOUNT, WINDOW_SIZE)

# CREATE CLOCK - FPS
clock = pygame.time.Clock()
while running:
    # SET FPS
    clock.tick(60)

    # DRAWING
    function.draw(WINDOW, grid, CELLS_AMOUNT, WINDOW_SIZE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # MOUSE BLOCK
        if pygame.mouse.get_pressed()[0]: # LEFT
            pos = pygame.mouse.get_pos()
            row, col = function.get_clicked_cell(pos, CELL_SIZE)
            cell = grid[row][col]

            if algorithm_done:
                grid = function.make_grid(CELLS_AMOUNT, WINDOW_SIZE)
                start_cell = None
                end_cell = None
                algorithm_done = False

            elif not start_cell and cell != end_cell:
                start_cell = cell
                start_cell.make_start()

            elif not end_cell and cell != start_cell:
                end_cell = cell
                end_cell.make_end()

            elif cell != end_cell and cell != start_cell:
                cell.make_wall()

        elif pygame.mouse.get_pressed()[1]: # MIDDLE
            grid = function.make_grid(CELLS_AMOUNT, WINDOW_SIZE)
            start_cell = None
            end_cell = None

        elif pygame.mouse.get_pressed()[2]: # RIGHT
            pos = pygame.mouse.get_pos()
            row, col = function.get_clicked_cell(pos, CELL_SIZE)
            cell = grid[row][col]
            cell.reset()
            if cell == start_cell:
                start_cell = None
            elif cell == end_cell:
                end_cell = None

        # KEYBOARD BLOCK
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                start_cell = None
                end_cell = None
                grid = function.make_grid(CELLS_AMOUNT, WINDOW_SIZE)
                
            if event.key == pygame.K_SPACE and start_cell and end_cell:
                for row in grid:
                    for cell in row:
                        if not cell.is_wall():
                            cell.update_neighbors(grid)
                found_path = function.algorithm(lambda: function.draw(WINDOW, grid, CELLS_AMOUNT, WINDOW_SIZE), grid, start_cell, end_cell)

                if found_path:
                    print('endpoint reached')
                elif not found_path:
                    print('endpoint is not reachable')

                algorithm_done = True

#END WHILE
pygame.quit()
