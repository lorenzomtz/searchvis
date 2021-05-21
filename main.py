import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# color constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# a square on the grid
class Square:

    # initialize a square
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_neighbors(self):
        return self.neighbors

    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col

    def get_color(self):
        return self.color

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def get_width(self):
        return self.width

    def get_total_rows(self):
        return self.total_rows

    def main():
        pygame.display.set_caption("Path Finding Algorithms")

    if __name__ == "__main__":
        main()