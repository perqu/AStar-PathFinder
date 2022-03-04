import pygame
import CellClass
from queue import PriorityQueue

def diagonal_distance(current_cell, goal):
    x1, y1 = current_cell
    x2, y2 = goal
    return (abs(x1-x2) ** 2 + abs(y1-y2) ** 2) ** (1/2)

def reconstruct_path(came_from, current, draw_lambda):
    while current in came_from:
        current = came_from[current]
        if current.is_start() == False: 
            current.make_path()
        draw_lambda()


def algorithm(draw_lambda, grid, start_cell, end_cell):
    open_set = PriorityQueue()
    open_set.put((0, start_cell))
    came_from = {}

    g_score = {cell: float('inf') for row in grid for cell in row}
    g_score[start_cell] = 0

    f_score = {cell: float('inf') for row in grid for cell in row}
    f_score[start_cell] = diagonal_distance(start_cell.get_pos(), end_cell.get_pos())

    open_set_hash = {start_cell}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[1]

        if current == end_cell:
            reconstruct_path(came_from, end_cell, draw_lambda)
            return True

        for neighbor in current.neighbors:
            if neighbor.is_closed() == False:
                tentative_g_score = g_score[current] + diagonal_distance(current.get_pos(), neighbor.get_pos())

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + diagonal_distance(neighbor.get_pos(), end_cell.get_pos())
                    if neighbor not in open_set_hash:
                        open_set.put((f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
                        if neighbor != end_cell:
                            neighbor.make_queue() 
                    
        draw_lambda()

        if current != start_cell:
            current.make_closed()
    else:
        return False

def make_grid(cells_amount, window_size):
    grid = []
    cell_size = window_size // cells_amount
    for i in range(cells_amount):
        grid.append([])
        for j in range(cells_amount):
            cell = CellClass.Cell(i,j, cell_size)
            if i == 0 or j == 0 or i == cells_amount - 1 or j == cells_amount - 1:
                cell.make_wall()
            grid[i].append(cell)

    return grid

def draw_grid(win, cells_amount, window_size):
    cell_size = window_size // cells_amount
    for i in range(cells_amount):
        pygame.draw.line(win, (128,128,128), (0, i * cell_size), (window_size, i * cell_size))

    for j in range(cells_amount):
        pygame.draw.line(win, (128,128,128), (j * cell_size, 0), (j * cell_size, window_size))

def draw_cells(win, grid):
    for row in grid:
        for cell in row:
            cell.draw(win)

def draw(win, grid, cells_amount, window_size):
    win.fill(CellClass.WHITE)

    draw_cells(win,grid)
    draw_grid(win, cells_amount, window_size)

    pygame.display.update()

def get_clicked_cell(pos, cell_size):
    y, x = pos

    col = x // cell_size
    row = y // cell_size
    
    return row, col
