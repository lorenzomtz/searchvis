from main import Square
from queue import PriorityQueue, Queue
import main
import pygame as pg
import util
from colour import Color

green = Color("green")
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
screen = main.screen
clock = main.clock
MARGIN = main.MARGIN
SQ_WIDTH = main.SQ_WIDTH


# depth-first search
def dfs(square):
    start = square.get_pos()
    visited = []
    squares = []
    # trivial solution check
    if square.get_color() == RED:
        return []
    visited.append(start)
    # find solution recursively
    return dfs_recur(square, (start,'Undefined'), squares, visited, 255), []
    

# recursive helper method for dfs
def dfs_recur(square, node, squares, visited, b):
    coord, direc = node
    visited.append(coord)
    # check if current position is goal
    if square.get_color() == RED:
        return squares
    # loop through neighbors
    for neighbor, nCost in square.get_neighbors():
        nCoord = neighbor.get_pos()
        if nCoord not in visited:
            # update action and visited list
            visited.append(nCoord)
            # ignore if wall
            if neighbor.get_color() == GREY:
                continue
            squares.append(neighbor)
            # mark as visited on screen
            path = dfs_recur(neighbor, (nCoord), squares, visited, b)
            # if path with goal found, return it
            if len(path) > 0:
                return path
            # if not found, delete this choice from path
            del squares[len(squares)-1]

    # no goal found
    return ''


# breadth-first search
def bfs(square):
    start = square.get_pos()
    visited = []
    squares = []
    q = Queue(maxsize = 1000)
    # trivial solution check
    if square.get_color() == RED:
        return [], []
    # set initial conditions
    q.put((square, start, squares))
    visited.append(start)

    while not q.empty():
        sq, coord, squares = q.get()
        # check is current position is goal
        if sq.get_color() == RED:
            return squares, visited
        # ignore if wall
        if sq.get_color() == GREY:
            continue
        # loop through kids
        for neighbor, nCost in sq.get_neighbors():
            nCoord = neighbor.get_pos()
            if nCoord not in visited:
                # update visited, path, and push to the queue
                visited.append(nCoord)
                # ignore if wall
                if neighbor.get_color() == GREY:
                    continue
                nextSquares = squares + [neighbor]
                q.put((neighbor, nCoord, nextSquares))

    return [], []


# uniform-cost search
def ucs(square):
    start = square.get_pos()
    visited = []
    squares = []
    costMap = {}
    pq = util.PriorityQueue()
    # trivial solution check
    if square.get_color() == RED:
        return [], []
    # set initial conditions
    pq.push((start, 0, squares, square), 0)
    costMap[start] = 0
    while not pq.isEmpty():
        coord, cost, squares, sq = pq.pop()
        # check if current position is goal
        if sq.get_color() == RED:
            return squares, visited
        if coord not in visited:
            visited.append(coord)
            # ignore if wall
            if sq.get_color() == GREY:
                continue
            # loop through kids
            for neighbor, nCost in sq.get_neighbors():
                # ignore if wall
                if neighbor.get_color() == GREY:
                    continue
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
                    pq.update((nCoord, total, nextSquares, neighbor), total)
    
    return [], []


# A* search
def astar(square, end):
    start = square.get_pos()
    visited = []
    squares = []
    costMap = {}
    pq = util.PriorityQueue()
    # trivial solution check
    if square.get_color() == RED:
        return [], []
    # set initial conditions
    pq.push((start, 0, squares, square), 0)
    costMap[start] = 0
    while not pq.isEmpty():
        coord, cost, squares, sq = pq.pop()
        # check if current position is goal
        if sq.get_color() == RED:
            return squares, visited
        if coord not in visited:
            visited.append(coord)
            # ignore if wall
            if sq.get_color() == GREY:
                continue
            # loop through kids
            for neighbor, nCost in sq.get_neighbors():
                # ignore if wall
                if neighbor.get_color() == GREY:
                    continue
                nCoord = neighbor.get_pos()
                # total path cost
                total = cost + nCost
                # total path cost including heuristic
                total_heur = total + util.manhattan_dist(nCoord, end)
                if nCoord not in visited:
                    # if node already exists in a path with
                    # less cost, skip to next iteration
                    if nCoord in costMap:
                        if costMap[nCoord] < total:
                            continue
                    # update costMap, path, and push to the queue
                    costMap[nCoord] = total
                    nextSquares = squares + [neighbor]
                    pq.update((nCoord, total, nextSquares, neighbor), total_heur)
    
    return [],[]
