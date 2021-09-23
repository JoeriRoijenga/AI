import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')


def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)


def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = all_tours(cities)
    return min(tours, key=tour_length)


def all_tours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities))
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]


def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))


def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(n) # the current system time is used as a seed
                  # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))


def nearest_neighbour(cities, current_city=None, visited=[]):
    if len(visited) == len(cities):
        return visited

    nn = None

    if current_city is None:
        current_city = next(iter(cities))

    # Look for the current city its nearest neighbour
    for city in cities:
        if city not in visited:
            if nn is None:
                nn = city

            if distance(current_city, city) < distance(current_city, nn):
                nn = city

    visited.append(nn)

    return nearest_neighbour(cities, nn, visited)


def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()


def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    print(tour)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)


# give a demo with 10 cities using brute force
plot_tsp(try_all_tours, make_cities(10))
plot_tsp(nearest_neighbour, make_cities(10))     # 100 - (2521.9 / 3230.6 * 100) = 21.9% difference
# plot_tsp(nearest_neighbour, make_cities(500))  # Time: 1.922 seconds, length: 20457

