import heapq
import math

class PriorityQueue:

    # initialize a priority queue
    def  __init__(self):
        self.heap = []
        self.count = 0


    # push onto the queue
    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1


    # pop off of the queue
    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item


    # empty queue check
    def isEmpty(self):
        return len(self.heap) == 0


    # If item already in priority queue with higher priority, update its priority and rebuild the heap.
    # If item already in priority queue with equal or lower priority, do nothing.
    # If item not in priority queue, do the same thing as self.push.
    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


# calculates manhattan distance between two points
def manhattan_dist(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


# calculates euclidean distance between two points
def euclid_dist(start, end):
    return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)