import pygame

GREEN = (0, 255, 0)
RED = (220, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165 ,0)
BLUE = (0, 0, 255)

class Cell():
    def __init__(self, x, y, size):
        self.__x = x
        self.__y = y
        self.__color = WHITE
        self.neighbors = []
        self.__size = size

    def get_pos(self):
        return self.__x, self.__y
    
    def is_closed(self):
        return self.__color == ORANGE

    def is_queue(self):
        return self.__color == YELLOW

    def is_wall(self):
        return self.__color == BLACK

    def is_start(self):
        return self.__color == GREEN

    def is_end(self):
        return self.__color == BLUE

    def reset(self):
        self.__color = WHITE

    def make_closed(self):
        self.__color = ORANGE
    
    def make_queue(self):
        self.__color = YELLOW
    
    def make_wall(self):
        self.__color = BLACK
    
    def make_start(self):
        self.__color = GREEN
    
    def make_end(self):
        self.__color = BLUE

    def make_path(self):
        self.__color = RED

    def draw(self, win):
        pygame.draw.rect(win, self.__color, (self.__x * self.__size, self.__y * self.__size, self.__size, self.__size))

    def update_neighbors(self, grid):
        TOP = not grid[self.__x - 1][self.__y].is_wall()
        RIGHT = not grid[self.__x][self.__y + 1].is_wall()
        DOWN = not grid[self.__x + 1][self.__y].is_wall()
        LEFT = not grid[self.__x][self.__y - 1].is_wall()
        if TOP: # TOP
            self.neighbors.append(grid[self.__x - 1][self.__y])

        if RIGHT: # RIGHT
            self.neighbors.append(grid[self.__x][self.__y + 1])

        if DOWN: # DOWN
            self.neighbors.append(grid[self.__x + 1][self.__y])

        if LEFT: # LEFT
            self.neighbors.append(grid[self.__x][self.__y - 1])

        if TOP or RIGHT:
            if grid[self.__x - 1][self.__y+1].is_wall() == False: # TOP-RIGHT
                self.neighbors.append(grid[self.__x - 1][self.__y + 1])

        if RIGHT or DOWN:
            if grid[self.__x+1][self.__y + 1].is_wall() == False: # DOWN-RIGHT
                self.neighbors.append(grid[self.__x + 1][self.__y + 1])

        if DOWN or LEFT:
            if grid[self.__x+1][self.__y - 1].is_wall() == False: # DOWN-LEFT
                self.neighbors.append(grid[self.__x + 1][self.__y - 1])

        if TOP or LEFT:
            if grid[self.__x -1][self.__y - 1].is_wall() == False: # TOP-LEFT
                self.neighbors.append(grid[self.__x - 1][self.__y - 1])

    def  __lt__(self, other):
        return False