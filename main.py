import pygame as pg
import math
import search
from colour import Color

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
GRID_LENGTH = 38
SCALE = 255
pg.init()  
screen = pg.display.set_mode((WIDTH, WIDTH))
clock = pg.time.Clock()
grid = []
rects = []
start = (3, 5)
end = (10, 29)

# a square on the grid
class Square:

    # initialize a square
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
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

    def set_color(self, color):
        self.color = color

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def __str__(self):
        return "\nSquare at: (" + str(self.row) + ", " + str(self.col) + ")"

    def __repr__(self):
        return "\nSquare at: (" + str(self.row) + ", " + str(self.col) + ")"


# basic screen management
def setup_screen():
    screen.fill(BLACK)
    pg.display.set_caption("Path Finding Algorithms")
    clock.tick(60)


# setup grid of Square objects
def setup_grid():
    for y in range(GRID_LENGTH):
        grid.append([])
        rects.append([])
        for x in range(GRID_LENGTH):
            square = Square(y, x, SQ_WIDTH, GRID_LENGTH)
            grid[y].append(square)
            color = WHITE
            # change start colors
            if y == start[0] and x == start[1] \
                or y == end[0] and x == end[1]:
                color = GREEN if x == start[1] and y == start[0] else RED
            grid[y][x].set_color(color)
            rect = pg.draw.rect(screen, color, \
                [(MARGIN + SQ_WIDTH) * x + MARGIN, \
                    (MARGIN + SQ_WIDTH) * y + MARGIN, SQ_WIDTH, SQ_WIDTH])
            rects[y].append(rect)

    pg.display.flip()


# link all adjacent squares together as neighbors
# neighbors of (x,y): [(x,y+1), (x,y-1), (x+1,y), (x-1,y)]
def populate_neighbors():
    for y in range(GRID_LENGTH):
        for x in range(GRID_LENGTH):
            neighbors = []
            if x+1 in range(GRID_LENGTH): neighbors.append((grid[y][x+1], 1))
            if x-1 in range(GRID_LENGTH): neighbors.append((grid[y][x-1], 1))
            if y-1 in range(GRID_LENGTH): neighbors.append((grid[y-1][x], 1))
            if y+1 in range(GRID_LENGTH): neighbors.append((grid[y+1][x], 1))
            grid[y][x].set_neighbors(neighbors)


# create a block in all pathfinding algorithms, cannot pass through
# walls are marked as GREY on the grid
def make_wall(x, y):
    color = GREY
    grid[y][x].set_color(color)
    draw_square(color, x, y)


# use the list of squares returned from pathfinding to display the path found
# path marked as BLACK on the grid
def display_path(squares):
    for sq in squares:
        color = sq.get_color()
        if color != GREEN and color != RED and color != GREY:
            y, x = sq.get_pos()
            color = BLACK
            grid[y][x].set_color(color)
            draw_square(color, x, y)
            pg.time.delay(5)


# erase any path (BLACK) squares displayed on the grid
def clear_path():
    for y in range(GRID_LENGTH):
        for x in range(GRID_LENGTH):
            color = grid[y][x].get_color()
            if color != GREEN and color != RED and color != GREY:
                color = WHITE
                grid[y][x].set_color(color)
                draw_square(color, x, y)


# helper function for drawing a square on the screen
def draw_square(color, x, y):
    rect = pg.draw.rect(screen, color, \
                [(MARGIN + SQ_WIDTH) * x + MARGIN, \
                    (MARGIN + SQ_WIDTH) * y + MARGIN, SQ_WIDTH, SQ_WIDTH])
    pg.display.update(rect)


# draws the squares at the coordinates given on the screen
# with a color transition from beginning to end
def draw_squares_at(coords):
    total = len(coords)
    green = Color("green")
    red = Color("red")
    # creates a range of colors to use for display
    colors = list(green.range_to(red, total))
    count = 0
    # loop through all of the coordinates given
    for y, x in coords:
        square = grid[y][x]
        sq_color = square.get_color()
        # avoid coloring over start and end nodes
        if sq_color != RED and sq_color != GREEN:
            # get the rgb values for the current square
            # and convert them to be in the 255 range
            rgb = list(colors[count].rgb)
            scaled_color = tuple([c * SCALE for c in rgb])
            rect = pg.draw.rect(screen, scaled_color, \
                [(MARGIN + SQ_WIDTH) * x + MARGIN, \
                    (MARGIN + SQ_WIDTH) * y + MARGIN, SQ_WIDTH, SQ_WIDTH])
            pg.display.update(rect)
        count += 1
        pg.time.delay(5)


def set_start(x, y):
    global start
    start = (x, y)

    
def set_end(x, y):
    global end
    end = (x, y)


def get_start():
    return start


def get_end():
    return end


# initialize/reset display grid
def setup():
    setup_screen()
    setup_grid()
    populate_neighbors()


def main():
    setup()
    running = True
    drag = False
    rect_x = None
    rect_y = None
    rect_color = None
    # game loop
    while running:
        for event in pg.event.get():
            global start
            global end
            if event.type == KEYDOWN:
                # escape key: EXIT
                if event.key == K_ESCAPE:
                    running = False
                    pg.quit()
                # up arrow key: BFS
                elif event.key == K_UP:
                    clear_path()
                    path, squares = search.bfs(grid[start[0]][start[1]])
                    draw_squares_at(squares)
                    display_path(path)
                # down arrow key: DFS
                elif event.key == K_DOWN:
                    clear_path()
                    path, squares = search.dfs(grid[start[0]][start[1]])
                    draw_squares_at(squares)
                    display_path(path)
                # left arrow key: UCS
                elif event.key == K_LEFT:
                    clear_path()
                    path, squares = search.ucs(grid[start[0]][start[1]])
                    draw_squares_at(squares)
                    display_path(path)
                # right arrow key: A*
                elif event.key == K_RIGHT:
                    clear_path()
                    path, squares = search.astar(grid[start[0]][start[1]], end)
                    draw_squares_at(squares)
                    display_path(path)
            # window close button: EXIT
            elif event.type == QUIT:
                running = False
                pg.quit()
            # mouse moving
            elif event.type == pg.MOUSEMOTION:
                # left click held while moving
                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    x = pos[0] // (SQ_WIDTH + MARGIN)
                    y = pos[1] // (SQ_WIDTH + MARGIN)
                    # Set that location to GREY
                    color = grid[y][x].get_color()
                    # if not start or ending square or being dragged, make wall
                    if color != GREEN and color != RED and not drag:
                        make_wall(x, y)
            elif event.type == pg.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    pos = pg.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    x = pos[0] // (SQ_WIDTH + MARGIN)
                    y = pos[1] // (SQ_WIDTH + MARGIN)
                    # Set that location to GREY
                    color = grid[y][x].get_color()
                    # click and drag start or ending square to move
                    if color == GREEN or color == RED:
                        drag = True
                        rect_x = x
                        rect_y = y
                        rect_color = color
                # right click, clear grid
                elif event.button == 3:
                    setup()
            elif event.type == pg.MOUSEBUTTONUP:
                pressed = False
                # handle dragging start and end squares
                if drag:
                    pos = pg.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    x = pos[0] // (SQ_WIDTH + MARGIN)
                    y = pos[1] // (SQ_WIDTH + MARGIN)
                    # update colors of dragged start and endpoint squares
                    draw_square(WHITE, rect_x, rect_y)
                    draw_square(rect_color, x, y)
                    grid[rect_y][rect_x].set_color(WHITE)
                    grid[y][x].set_color(rect_color)
                    # set new start or end coords
                    if rect_color == GREEN:
                        start = (y, x)
                    elif rect_color == RED:
                        end = (y, x)
                    # clear dragging information
                    rect_x = None
                    rect_y = None
                    rect_color = None
                    drag = False

if __name__ == "__main__":
    main()