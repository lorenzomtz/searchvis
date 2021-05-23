from main import Square
from queue import PriorityQueue, Queue
import main
import pygame as pg

RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen = main.screen
clock = main.clock
MARGIN = main.MARGIN
SQ_WIDTH = main.SQ_WIDTH


def dfs(square):
    start = square.get_pos()
    visited = []
    actions = []
    # trivial solution check
    if square.get_color() == RED:
        return []
    visited.append(start)
    # find solution recursively
    return dfs_recur(square, (start,'Undefined'), actions, visited, 255)
    
def dfs_recur(square, node, actions, visited, b):
    coord, direc = node
    visited.append(coord)
    # check if current position is goal
    if square.get_color() == RED:
        return actions
    # loop through neighbors
    for neighbor, nDirec in square.get_neighbors():
        nCoord = neighbor.get_pos()
        if nCoord not in visited:
            # update action and visited list
            actions.append(nDirec)
            visited.append(nCoord)
            # mark as visited on screen
            rect = pg.draw.rect(screen, (180, 180, b), \
                [(MARGIN + SQ_WIDTH) * nCoord[1] + MARGIN, \
                    (MARGIN + SQ_WIDTH) * nCoord[0] + MARGIN, SQ_WIDTH, SQ_WIDTH])
            pg.display.update(rect)
            pg.time.delay(10)
            path = dfs_recur(neighbor, (nCoord, nDirec), actions, visited, b)
            # if path with goal found, return it
            if len(path) > 0:
                return path
            # if not found, delete this choice from path
            del actions[len(actions)-1]

    # no goal found
    return ''

def bfs(square):
    start = square.get_pos()
    visited = []
    path = []
    # tracker = {}
    # goal = ()
    q = Queue(maxsize = 100)
    # trivial solution check
    if square.get_color() == RED:
        return []
    # set initial conditions
    q.put((square, start, path))
    visited.append(start)

    while not q.empty():
        sq, coord, actions = q.get()
        # check is current position is goal
        #sq = main.get_square_at(coord)
        if sq.get_color() == RED:
            return actions
        # loop through kids
        for neighbor, nDirec in sq.get_neighbors():
            nCoord = neighbor.get_pos()
            if nCoord not in visited:
                # update visited, path, and push to the queue
                visited.append(nCoord)
                nextPath = actions + [nDirec]
                q.put((neighbor, nCoord, nextPath))
                rect = pg.draw.rect(screen, (180, 180, 255), \
                    [(MARGIN + SQ_WIDTH) * nCoord[1] + MARGIN, \
                        (MARGIN + SQ_WIDTH) * nCoord[0] + MARGIN, SQ_WIDTH, SQ_WIDTH])
                pg.display.update(rect)
                pg.time.delay(10)

    return []

def ucs():
    return None

def astar():
    return None

