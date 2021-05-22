import pygame as pg
import math

# key constants from pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# color constants
# TODO: find prettier colors
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


# set up square screen
WIDTH = 800
MARGIN = 1
SQ_WIDTH = 20
pg.init()  
screen = pg.display.set_mode((WIDTH, WIDTH))
clock = pg.time.Clock()
grid = []

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

    def get_pos(self):
        return self.row, self.col

    def get_color(self):
        return self.color
    
    def get_width(self):
        return self.width

    def get_total_rows(self):
        return self.total_rows

    def set_color(self, color):
        self.color = color

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors


# basic screen management
def setup_screen():
    screen.fill(BLACK)
    pg.display.set_caption("Path Finding Algorithms")

# setup grid of Square objects
def setup_grid():
    for y in range(38):
        grid.append([])
        for x in range(38):
            square = Square(y, x, SQ_WIDTH, 38)
            grid[y].append(square)
    grid[19][10].set_color(GREEN)
    grid[19][28].set_color(RED)
            
def populate_neighbors():
    for y in range(38):
        for x in range(38):
            neighbors = []
            if x-1 in range(38): neighbors.append(grid[y][x-1])
            if x+1 in range(38): neighbors.append(grid[y][x+1])
            if y-1 in range(38): neighbors.append(grid[y-1][x])
            if y+1 in range(38): neighbors.append(grid[y+1][x])
            grid[y][x].set_neighbors(neighbors)

def main():
    setup_screen()
    setup_grid()
    populate_neighbors()
    running = True
    # game loop
    while running:
        for event in pg.event.get():
            if event.type == KEYDOWN:
                # escape key
                if event.key == K_ESCAPE:
                    running = False
            # window close button
            elif event.type == QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                # TODO: click and drag for walls
                # TODO: click and drag for start and end point
                pos = pg.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                x = pos[0] // (SQ_WIDTH + MARGIN)
                y = pos[1] // (SQ_WIDTH + MARGIN)
                
                # Set that location to grey
                color = grid[y][x].get_color()
                if color == WHITE:
                    grid[y][x].set_color(GREY)

        #setup_screen()
        # grid setup
        for y in range(38):
            for x in range(38):
                color = grid[y][x].get_color()
                pg.draw.rect(screen, color, \
                    [(MARGIN + SQ_WIDTH) * x + MARGIN, \
                        (MARGIN + SQ_WIDTH) * y + MARGIN, SQ_WIDTH, SQ_WIDTH])

        clock.tick(60)
        pg.display.flip()
    
    pg.quit()

if __name__ == "__main__":
    main()