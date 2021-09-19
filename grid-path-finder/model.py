import random
import heapq
import math
import config as cf

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
    return abs(goal[0] - start[0]) + abs(goal[1] - start[1])


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
    # plot a sample path for demonstration
    print(get_neighbours((0, 0)))
    print(heuristic(start, goal))

    priority_queue = PriorityQueue()

    final_path = {}

    visited = []
    closed = []
    new_cost = 0

    priority_queue.put(start, 0)

    while not priority_queue.empty():
        current_node = priority_queue.get()

        # Get the neighbours of the current node
        neighbours = get_neighbours(current_node)

        # If the goal is reached
        if current_node == goal:
            print("Found")
            draw_line(app, final_path)

        visited.append(current_node)

        for neighbour in neighbours:
            new_cost = get_cost(current_node) + heuristic(current_node, goal)
            print(current_node, neighbour, heuristic(neighbour, goal))
            if neighbour not in visited or new_cost < get_cost(neighbour) + heuristic(neighbour, goal):
                print("Found new path")
                priority = new_cost + heuristic(neighbour, goal)
                priority_queue.put(neighbour, priority)

                visited.append(neighbour)
                final_path[current_node] = neighbour


def draw_line(app, path):
    for first_node, second_node in path.items():
        app.plot_line_segment(first_node[0], first_node[1], second_node[0], second_node[1], color=cf.FINAL_C)
        app.pause()
