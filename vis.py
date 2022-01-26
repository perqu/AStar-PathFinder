from turtle import width
import db
import pygame

window = pygame.display.set_mode((db.WIDTH, db.WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

class Point:
    def __init__(self, x, y, width, total_rows):
        self.x = x
        self.y = y
        self.color = db.BACKGROUND
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.x, self.y

    def is_closed(self):
        return self.color == db.CLOSED

    def is_open(self):
        return self.color == db.OPEN

    def is_barrier(self):
        return self.color == db.BARRIER

    def is_start(self):
        return self.color == db.START

    def is_end(self):
        return self.color == db.END

    def reset(self):
        self.color = db.BACKGROUND

    def make_start(self):
        self.color = db.START

    def make_closed(self):
        self.color = db.CLOSED

    def make_open(self):
        self.color = db.OPEN

    def make_barrier(self):
        self.color = db.BARRIER

    def make_end(self):
        self.color = db.END

    def make_path(self):
        self.color = db.PATH

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x * self.width, self.y * self.width, self.width, self.width))

    def update_neighbors(self, grid):
        TOP = not grid[self.x - 1][self.y].is_barrier()
        RIGHT = not grid[self.x][self.y + 1].is_barrier()
        DOWN = not grid[self.x + 1][self.y].is_barrier()
        LEFT = not grid[self.x][self.y - 1].is_barrier()
        if TOP: # TOP
            self.neighbors.append(grid[self.x - 1][self.y])

        if RIGHT: # RIGHT
            self.neighbors.append(grid[self.x][self.y + 1])

        if DOWN: # DOWN
            self.neighbors.append(grid[self.x + 1][self.y])

        if LEFT: # LEFT
            self.neighbors.append(grid[self.x][self.y - 1])

        if TOP or RIGHT:
            if grid[self.x - 1][self.y+1].is_barrier() == False: # TOP-RIGHT
                self.neighbors.append(grid[self.x - 1][self.y + 1])

        if RIGHT or DOWN:
            if grid[self.x+1][self.y + 1].is_barrier() == False: # DOWN-RIGHT
                self.neighbors.append(grid[self.x + 1][self.y + 1])

        if DOWN or LEFT:
            if grid[self.x+1][self.y - 1].is_barrier() == False: # DOWN-LEFT
                self.neighbors.append(grid[self.x + 1][self.y - 1])

        if TOP or LEFT:
            if grid[self.x -1][self.y - 1].is_barrier() == False: # TOP-LEFT
                self.neighbors.append(grid[self.x - 1][self.y - 1])

    def __lt__(self, other):
        return False

def make_grid(rows):
	grid = []
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Point(i, j, db.GAP, rows)
			if i == 0 or j == 0 or i == rows - 1 or j == rows - 1:
				spot.make_barrier()
			grid[i].append(spot)
	return grid

def draw(grid, rows):
    window.fill(db.BACKGROUND)
    for row in grid:
        for spot in row:
            spot.draw()
            
    for i in range(rows):
        pygame.draw.line(window, db.LINES, (0, i * db.GAP), (db.WIDTH, i * db.GAP))
        for j in range(rows):
            pygame.draw.line(window, db.LINES, (j * db.GAP, 0), (j * db.GAP, db.WIDTH))
    pygame.display.update()

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if current.is_start() == False: current.make_path()
        draw()

def get_clicked_pos(pos):
	y, x = pos

	row = y // db.GAP
	col = x // db.GAP

	return row, col