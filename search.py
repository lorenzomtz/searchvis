from main import RED, GREY
from queue import Queue
import util


# depth-first search
def dfs(square):
    # set initial parameters
    start = square.get_pos()
    visited = []
    path = []
    
    # trivial solution check
    if square.get_color() == RED:
        return []

    # mark as visited and find solution recursively 
    visited.append(start)
    return dfs_recur(square, start, path, visited), visited
    

# recursive helper method for dfs
def dfs_recur(square, coord, path, visited):
    # mark as visited
    visited.append(coord)
    
    # check if current position is goal
    if square.get_color() == RED:
        return path
    
    # loop through neighbors
    for neighbor, nCost in square.get_neighbors():
        nCoord = neighbor.get_pos()

        # only expand unvisited path
        if nCoord not in visited:
            # mark as visited, ignore if wall
            visited.append(nCoord)
            if neighbor.get_color() == GREY:
                continue

            # update path list
            path.append(neighbor)
            
            # recursive call to find path
            next_path = dfs_recur(neighbor, (nCoord), path, visited)
            
            # if path with goal found, return it
            if len(next_path) > 0:
                return next_path
            
            # if not found, delete this choice from path
            del path[len(path)-1]

    # no path found
    return ''


# breadth-first search
def bfs(square):
    # set initial parameters
    start = square.get_pos()
    visited = []
    path = []
    q = Queue(maxsize = 1000)

    # trivial solution check
    if square.get_color() == RED:
        return [], []

    # update queue and mark as visited
    q.put((square, start, path))
    visited.append(start)

    # loop until queue is empty
    while not q.empty():
        sq, coord, path = q.get()
        
        # check is current position is goal,
        # ignore if wall
        if sq.get_color() == RED:
            return path, visited
        if sq.get_color() == GREY:
            continue
        
        # loop through kids
        for neighbor, nCost in sq.get_neighbors():
            nCoord = neighbor.get_pos()

            # only expand unvisited path
            if nCoord not in visited:
                # mark as visited, and ignore if wall
                visited.append(nCoord)
                if neighbor.get_color() == GREY:
                    continue
                
                # update path, and push to the queue
                next_path = path + [neighbor]
                q.put((neighbor, nCoord, next_path))

    # no path found
    return [], []


# uniform-cost search
def ucs(square):
    # set initial parameters
    start = square.get_pos()
    visited = []
    path = []
    costMap = {}
    pq = util.PriorityQueue()

    # trivial solution check
    if square.get_color() == RED:
        return [], []

    # update queue and cost map
    pq.push((start, 0, path, square), 0)
    costMap[start] = 0
    
    # loop until queue is empty
    while not pq.isEmpty():
        coord, cost, path, sq = pq.pop()
        
        # check if current position is goal
        if sq.get_color() == RED:
            return path, visited
        
        # only expand unvisited squares
        if coord not in visited:
            # mark as visited, ignore if wall 
            visited.append(coord)
            if sq.get_color() == GREY:
                continue
            
            # loop through kids
            for neighbor, nCost in sq.get_neighbors():
                # ignore if wall
                if neighbor.get_color() == GREY:
                    continue
            
                nCoord = neighbor.get_pos()
                # only expand unvisited squares
                if nCoord not in visited:
                    # if node already exists in a path with
                    # less cost, skip to next iteration
                    total = cost + nCost
                    if nCoord in costMap:
                        if costMap[nCoord] < total:
                            continue
                    
                    # update costMap, path, and push to the queue
                    costMap[nCoord] = total
                    next_path = path + [neighbor]
                    pq.update((nCoord, total, next_path, neighbor), total)
    
    # no path found
    return [], []


# A* search
def astar(square, end):
    # set initial parameters
    start = square.get_pos()
    visited = []
    path = []
    costMap = {}
    pq = util.PriorityQueue()

    # trivial solution check
    if square.get_color() == RED:
        return [], []
    
    # update queue and cost map
    pq.push((start, 0, path, square), 0)
    costMap[start] = 0

    # loop until queue is empty
    while not pq.isEmpty():
        coord, cost, path, sq = pq.pop()
        
        # check if current position is goal
        if sq.get_color() == RED:
            return path, visited
        
        # only expand unvisited squares
        if coord not in visited:
            # mark as visited, ignore if wall 
            visited.append(coord)
            if sq.get_color() == GREY:
                continue

            # loop through kids
            for neighbor, nCost in sq.get_neighbors():
                # ignore if wall
                if neighbor.get_color() == GREY:
                    continue
                nCoord = neighbor.get_pos()
                
                # only expand unvisited squares
                if nCoord not in visited:
                    # total path cost with and without heuristic
                    total = cost + nCost
                    total_heur = total + util.manhattan_dist(nCoord, end)
                    
                    # if node already exists in a path with
                    # less cost, skip to next iteration
                    if nCoord in costMap:
                        if costMap[nCoord] < total:
                            continue
                    
                    # update costMap, path, and push to the queue
                    costMap[nCoord] = total
                    next_path = path + [neighbor]
                    pq.update((nCoord, total, next_path, neighbor), total_heur)
    
    # no path found
    return [], []
