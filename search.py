from main import Square
from queue import PriorityQueue, Queue
import main

RED = (255, 0, 0)

def dfs(square):
    start = square.get_pos()
    visited = []
    actions = []
    # trivial solution check
    if square.get_color() == RED:
        return []
    visited.append(start)
    # find solution recursively
    return dfs_recur(square, (start,'Undefined'), actions, visited)
    
def dfs_recur(square, node, actions, visited):
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
            path = dfs_recur(neighbor, (nCoord, nDirec), actions, visited)
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
    q.put((start, path))
    visited.append(start)

    while not q.empty():
        coord, actions = q.get()
        print(coord)
        # check is current position is goal
        sq = main.get_square_at(coord)
        if sq.get_color() == RED:
            return actions
        # loop through kids
        for neighbor, nDirec in sq.get_neighbors():
            nCoord = neighbor.get_pos()
            if nCoord not in visited:
                # update visited, path, and push to the queue
                visited.append(nCoord)
                nextPath = actions + [nDirec]
                q.put((nCoord, nextPath))

    return []

def ucs():
    return None

def astar():
    return None

