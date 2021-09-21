import random
import heapq
import math
import config as cf
from time import sleep

# global var
grid = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]


class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get()) / 10 else 0


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value


def heuristic(start, goal):
    # https://stackoverflow.com/questions/46974075/a-star-algorithm-distance-heuristics
    D = 1
    D2 = math.sqrt(2)

    dx = abs(goal[0] - start[0])
    dy = abs(goal[1] - start[1])

    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)

def get_cost(node):
    cost = get_grid_value(node)
    if cost == 'b' or cost == -1:
        return 0
    else:
        return cost


def get_neighbours(node):
    output = []

    if node[0] + 1 > 0:
        try:
            if get_grid_value((node[0] + 1, node[1])) != 'b':
                output.append((node[0] + 1, node[1]))
        except IndexError:
            pass

    if node[0] - 1 > 0:
        try:
            if get_grid_value((node[0] - 1, node[1])) != 'b':
                output.append((node[0] - 1, node[1]))
        except IndexError:
            pass

    if node[1] + 1 > 0:
        try:
            if get_grid_value((node[0], node[1] + 1)) != 'b':
                output.append((node[0], node[1] + 1))
        except IndexError:
            pass

    if node[1] - 1 > 0:
        try:
            if get_grid_value((node[0], node[1] - 1)) != 'b':
                output.append((node[0], node[1] - 1))
        except IndexError:
            pass

    return output


def search(app, start, goal):
    print(heuristic((0, 0), (3, 3)))
    # plot a sample path for demonstration

    priority_queue = PriorityQueue()

    final_path = {}

    visited = []

    priority_queue.put(start, 0)

    while not priority_queue.empty():
        current_node = priority_queue.get()

        # Get the neighbours of the current node
        neighbours = get_neighbours(current_node)

        # If the goal is reached
        if current_node == goal:
            print(final_path)
            app.draw_path(final_path)
            break

        visited.append(current_node)

        for neighbour in neighbours:

            new_cost = get_cost(current_node) + get_cost(neighbour)
            print(neighbour, new_cost)

            if neighbour not in visited or new_cost < get_cost(neighbour):

                priority = new_cost + heuristic(neighbour, goal)
                priority_queue.put(neighbour, priority)

                visited.append(neighbour)
                final_path[neighbour] = current_node