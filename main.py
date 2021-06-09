import pygame as pg
import pygame_widgets as pw
import search
from colour import Color
import sys


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
search_actions = [K_UP, K_DOWN, K_LEFT, K_RIGHT]


# color constants
RED = (193, 98, 102)
GREEN = (144, 176, 97)
WHITE = (251, 250, 245)
YELLOW = (253, 253, 150)
BLACK = (41, 45, 52)
GREY = (41, 45, 52)
SCALE = 255


# screen/grid constants
WIDTH = 800
MARGIN = 1
SQ_WIDTH = 20
GRID_LENGTH = 38


# set up square screen/grid
pg.init()
screen = pg.display.set_mode((WIDTH + 200, WIDTH))
# button_arr = pw.ButtonArray(screen, 850, 300, 50, 50, (2, 2),
#                           border=100, texts=('1', '2', '3', '4'),
#                          colour=YELLOW)
clear_button = pw.Button(
        screen, 850, 300, 100, 30, text='Clear Grid',
        margin=20, font = pg.font.SysFont("consolas", 15),
        inactiveColour=RED,
        pressedColour=WHITE, radius=5,
        onClick=lambda: print('Click')
     )
dfs_button = pw.Button(
        screen, 850, 200, 100, 30, text='Depth-First',
        margin=20, font = pg.font.SysFont("consolas", 15),
        inactiveColour=RED,
        pressedColour=WHITE, radius=5,
        onClick=lambda: print('Click')
     )
bfs_button = pw.Button(
        screen, 850, 300, 100, 30, text='Breadth-First',
        margin=20, font = pg.font.SysFont("consolas", 15),
        inactiveColour=RED,
        pressedColour=WHITE, radius=5,
        onClick=lambda: print('Click')
     )
ucs_button = pw.Button(
        screen, 850, 400, 100, 30, text='Uniform-Cost',
        margin=20, font = pg.font.SysFont("consolas", 15),
        inactiveColour=RED,
        pressedColour=WHITE, radius=5,
        onClick=lambda: print('Click')
     )
astar_button = pw.Button(
        screen, 850, 500, 100, 30, text='A*',
        margin=20, font = pg.font.SysFont("consolas", 15),
        inactiveColour=RED,
        pressedColour=WHITE, radius=5,
        onClick=lambda: print('Click')
     )
buttons = [clear_button, dfs_button, bfs_button, ucs_button, astar_button]
clock = pg.time.Clock()
grid = []
start = (3, 5)
end = (29, 29)
sys.setrecursionlimit(10 ** 6)


# a square on the grid
class Square:


    # initialize a square
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.neighbors = []


    # getter for neighbor list
    def get_neighbors(self):
        return self.neighbors


    # getter for position
    def get_pos(self):
        return self.row, self.col


    # getter for color
    def get_color(self):
        return self.color


    # setter for color
    def set_color(self, color):
        self.color = color


    # setter for neighbor list
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors


    # string representation of Square object:
    # Square at: (y, x)
    def __str__(self):
        return "\nSquare at: (" + str(self.row) + ", " + str(self.col) + ")"


    # string representation of Square object when iterating
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
        for x in range(GRID_LENGTH):
            square = Square(y, x)
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
# path marked as YELLOW on the grid
def display_path(squares):
    for sq in squares:
        color = sq.get_color()
        # recolor squares chosen as path squares
        if color != GREEN and color != RED and color != GREY:
            y, x = sq.get_pos()
            color = YELLOW
            grid[y][x].set_color(color)
            draw_square(color, x, y)
            pg.time.delay(5)


# erase any path squares displayed on the grid
def clear_path():
    for y in range(GRID_LENGTH):
        for x in range(GRID_LENGTH):
            color = grid[y][x].get_color()
            # override squares that aren't start, end, or wall squares
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
    # length of coordinate list for display purposes
    total = len(coords)
    g = (GREEN[0] / SCALE, GREEN[1] / SCALE, GREEN[2] / SCALE)
    green = Color(rgb = g)
    r = (RED[0] / SCALE, RED[1] / SCALE, RED[2] / SCALE)
    red = Color(rgb = r)

    # creates a range of colors to use for display
    colors = list(green.range_to(red, total))
    count = 0

    # loop through all of the coordinates given
    for y, x in coords:
        square = grid[y][x]
        sq_color = square.get_color()
        
        # avoid coloring over start and end nodes
        if sq_color != RED and sq_color != GREEN and sq_color != GREY:
            # get the rgb values for the current square
            # and convert them to be in the 255 range
            raw_rgb = list(colors[count].rgb)
            adjusted_rgb = tuple([c_val * SCALE for c_val in raw_rgb])
            rect = pg.draw.rect(screen, adjusted_rgb, \
                [(MARGIN + SQ_WIDTH) * x + MARGIN, \
                    (MARGIN + SQ_WIDTH) * y + MARGIN, SQ_WIDTH, SQ_WIDTH])
            pg.display.update(rect)
        
        count += 1
        pg.time.delay(5)


# helper function for transferring mouse coordinates
# to grid coordinates
def get_coords():
    pos = pg.mouse.get_pos()
                    
    # Change the x/y screen coordinates to grid coordinates
    x = pos[0] // (SQ_WIDTH + MARGIN)
    y = pos[1] // (SQ_WIDTH + MARGIN)

    # bounds check
    if x not in range(GRID_LENGTH) or y not in range(GRID_LENGTH):
        x = -1

    return x, y


# helper function to perform the specified type
# of search dependent on keyboard input
def search_handler(type):
    # clear any path on grid if existing
    clear_path()
    y = start[0]
    x = start[1]
    
    # up arrow key: BFS
    if type == pg.K_UP:
        path, squares = search.bfs(grid[y][x])
    # down arrow key: DFS
    elif type == pg.K_DOWN:
        path, squares = search.dfs(grid[y][x])
    # left arrow key: UCS
    elif type == pg.K_LEFT:
        path, squares = search.ucs(grid[y][x])
    # right arrow key: A*
    elif type == pg.K_RIGHT:
        path, squares = search.astar(grid[y][x], end)
    
    # display pathfinding process and resulting path found
    draw_squares_at(squares)
    display_path(path)


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
        events = pg.event.get()
        # loop through event queue
        for event in events:
            global start
            global end
            
            # key pressed
            if event.type == KEYDOWN:
                # escape key: EXIT
                if event.key == K_ESCAPE:
                    running = False
                    pg.quit()

                # arrow keys: SEARCH
                elif event.key in search_actions:
                    search_handler(event.key)
            
            # window close button: EXIT
            elif event.type == QUIT:
                running = False
                pg.quit()

            # mouse moving
            elif event.type == pg.MOUSEMOTION:
                # left click held while moving
                if pg.mouse.get_pressed()[0]:
                    # translate mouse coordinates to grid coordinates
                    x, y = get_coords()

                    # bounds check
                    if x == -1:
                        continue

                    # Set that location to GREY
                    color = grid[y][x].get_color()
                    
                    # if not start or ending square or being dragged, make wall
                    if color != GREEN and color != RED and not drag:
                        make_wall(x, y)
            
            # mouse clicked
            elif event.type == pg.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    # translate mouse coordinates to grid coordinates
                    x, y = get_coords()

                    # bounds check
                    if x == -1:
                        continue

                    # set that location to GREY
                    color = grid[y][x].get_color()
                    
                    # click and drag start or ending square to move
                    if color == GREEN or color == RED:
                        drag = True
                        rect_x = x
                        rect_y = y
                        rect_color = color

                    # otherwise, make wall
                    else:
                        make_wall(x, y)
                
                # right click, clear grid
                elif event.button == 3:
                    setup()
            
            # mouse button released
            elif event.type == pg.MOUSEBUTTONUP:
                pressed = False
                
                # handle dragging start and end squares
                if drag:
                    # translate mouse coordinates to grid coordinates
                    x, y = get_coords()

                    # bounds check
                    if x == -1:
                        continue

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

        # button handler
        if running:
            for button in buttons:
                button.listen(events)
                button.draw()
            pg.display.update()


if __name__ == "__main__":
    main()