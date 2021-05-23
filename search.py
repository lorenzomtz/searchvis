from main import Square
from queue import PriorityQueue, Queue
import main
import pygame as pg
import util

RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen = main.screen
clock = main.clock
MARGIN = main.MARGIN
SQ_WIDTH = main.SQ_WIDTH


def dfs(square):
    start = square.get_pos()
    visited = []
    squares = []
    # trivial solution check
    if square.get_color() == RED:
        return []
    visited.append(start)
    # find solution recursively
    return dfs_recur(square, (start,'Undefined'), squares, visited, 255)
    
def dfs_recur(square, node, squares, visited, b):
    coord, direc = node
    visited.append(coord)
    # check if current position is goal
    if square.get_color() == RED:
        return squares
    # loop through neighbors
    for neighbor, nDirec, nCost in square.get_neighbors():
        nCoord = neighbor.get_pos()
        if nCoord not in visited:
            # update action and visited list
            squares.append(neighbor)
            visited.append(nCoord)
            # mark as visited on screen
            if neighbor.get_color() != RED:
                rect = pg.draw.rect(screen, (180, 180, b), \
                    [(MARGIN + SQ_WIDTH) * nCoord[1] + MARGIN, \
                        (MARGIN + SQ_WIDTH) * nCoord[0] + MARGIN, SQ_WIDTH, SQ_WIDTH])
                pg.display.update(rect)
            pg.time.delay(5)
            path = dfs_recur(neighbor, (nCoord, nDirec), squares, visited, b)
            
            # if path with goal found, return it
            if len(path) > 0:
                return path
            # if not found, delete this choice from path
            del squares[len(squares)-1]

    # no goal found
    return ''

def bfs(square):
    start = square.get_pos()
    visited = []
    squares = []
    # tracker = {}
    # goal = ()
    q = Queue(maxsize = 1000)
    # trivial solution check
    if square.get_color() == RED:
        return []
    # set initial conditions
    q.put((square, start, squares))
    visited.append(start)

    while not q.empty():
        sq, coord, squares = q.get()
        # check is current position is goal
        #sq = main.get_square_at(coord)
        if sq.get_color() == RED:
            return squares
        # loop through kids
        for neighbor, nDirec, nCost in sq.get_neighbors():
            nCoord = neighbor.get_pos()
            if nCoord not in visited:
                # update visited, path, and push to the queue
                visited.append(nCoord)
                nextSquares = squares + [neighbor]
                q.put((neighbor, nCoord, nextSquares))
                if neighbor.get_color() != RED:
                    rect = pg.draw.rect(screen, (180, 180, 255), \
                        [(MARGIN + SQ_WIDTH) * nCoord[1] + MARGIN, \
                            (MARGIN + SQ_WIDTH) * nCoord[0] + MARGIN, SQ_WIDTH, SQ_WIDTH])
                    pg.display.update(rect)
                pg.time.delay(5)

    return []

def ucs(square):
    start = square.get_pos()
    visited = []
    squares = []
    costMap = {}
    pq = util.PriorityQueue()
    # trivial solution check
    if square.get_color() == RED:
        return []
    # set initial conditions
    #visited.append(start)
    pq.push((start, 0, squares, square), 0)
    costMap[start] = 0
    while not pq.isEmpty():
        #if pq.qsize() > 50:
        #    break
        coord, cost, squares, sq = pq.pop()
        #visited.append(coord)
        # check if current position is goal
        if sq.get_color() == RED:
            return squares
        if coord not in visited:
            visited.append(coord)
            # loop through kids
            for neighbor, nDirec, nCost in sq.get_neighbors():
                nCoord = neighbor.get_pos()
                total = cost + nCost
                if nCoord not in visited:
                    # if node already exists in a path with
                    # less cost, skip to next iteration
                    if nCoord in costMap:
                        if costMap[nCoord] < total:
                            continue
                    # update costMap, path, and push to the queue
                    costMap[nCoord] = total
                    nextSquares = squares + [neighbor]
                    # don't know if will work
                    pq.update((nCoord, total, nextSquares, neighbor), total)
                    if neighbor.get_color() != RED:
                        rect = pg.draw.rect(screen, (180, 180, 255), \
                            [(MARGIN + SQ_WIDTH) * nCoord[1] + MARGIN, \
                                (MARGIN + SQ_WIDTH) * nCoord[0] + MARGIN, SQ_WIDTH, SQ_WIDTH])
                        pg.display.update(rect)
                    pg.time.delay(5)
    
    return []

def astar(square):
    start = square.get_pos()
    visited = []
    squares = []
    costMap = {}
    pq = util.PriorityQueue()
    # trivial solution check
    if square.get_color() == RED:
        return []
    # set initial conditions
    #visited.append(start)
    pq.push((start, 0, squares, square), 0)
    costMap[start] = 0
    while not pq.isEmpty():
        #if pq.qsize() > 50:
        #    break
        coord, cost, squares, sq = pq.pop()
        #visited.append(coord)
        # check if current position is goal
        if sq.get_color() == RED:
            return squares
        if coord not in visited:
            visited.append(coord)
            # loop through kids
            for neighbor, nDirec, nCost in sq.get_neighbors():
                nCoord = neighbor.get_pos()
                total = cost + nCost# + util.manhattan_dist(nCoord, main.end)
                total_heur = total + util.manhattan_dist(nCoord, main.end)
                if nCoord not in visited:
                    # if node already exists in a path with
                    # less cost, skip to next iteration
                    if nCoord in costMap:
                        if costMap[nCoord] < total_heur:
                            continue
                    # update costMap, path, and push to the queue
                    costMap[nCoord] = total
                    nextSquares = squares + [neighbor]
                    # don't know if will work
                    pq.update((nCoord, total, nextSquares, neighbor), total_heur)
                    if neighbor.get_color() != RED:
                        rect = pg.draw.rect(screen, (180, 180, 255), \
                            [(MARGIN + SQ_WIDTH) * nCoord[1] + MARGIN, \
                                (MARGIN + SQ_WIDTH) * nCoord[0] + MARGIN, SQ_WIDTH, SQ_WIDTH])
                        pg.display.update(rect)
                    pg.time.delay(5)
    
    return []
    """
    start = square.get_pos()                                      
    pq = util.PriorityQueue()
    visited = []
    squares = []
    # trivial solution che
    if square.get_color() == RED:
        return []
    # set initial conditions
    pq.push((start, squares, square), 0)

    while not pq.isEmpty():
        coord, squares, square = pq.pop()
        # check if current position is goal
        if square.get_color() == RED:
            return squares
        if coord not in visited:
            visited.append(coord)
            # loop through kids
            for neighbor, nDirec, nCost in square.get_neighbors():
                # update path, compute total, push to queue
                nCoord = neighbor.get_pos()
                newSquares = squares + [neighbor]
                print(len(newSquares))
                total = len(newSquares) + util.manhattan_dist(nCoord, main.end)
                pq.push((nCoord, newSquares, square), total)
                if neighbor.get_color() != RED:
                    rect = pg.draw.rect(screen, (180, 180, 255), \
                        [(MARGIN + SQ_WIDTH) * nCoord[1] + MARGIN, \
                            (MARGIN + SQ_WIDTH) * nCoord[0] + MARGIN, SQ_WIDTH, SQ_WIDTH])
                    pg.display.update(rect)
                pg.time.delay(5)
    
    return []
"""

