import sys
import math
import random
import tqdm

from common import print_tour, read_input


def calculate_distance(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# create a table which holds distances of all pairs of cities
def create_distance_table(cities):
    cities_num = len(cities)
    table = [[0 for i in range(cities_num)] for j in range(cities_num)]
    for p1 in range(cities_num):
        for p2 in range(cities_num):
            table[p1][p2] = calculate_distance(cities[p1], cities[p2])
    return table


def solve(cities):
    cities_list = list(range(len(cities)))
    best_tour = tuple(cities_list)
    best_distance = float("inf")
    # generate greedy tours and apply 2-opt to each of them
    # select the best tour of all
    dist_table = create_distance_table(cities)
    for i in tqdm.tqdm(range(20)):
        greedy_tour = greedy_solve(cities, dist_table)
        while True:
            delta = 0
            for (a, b) in all_segments(len(cities)):
                delta += reverse_subtour_2opt(greedy_tour, a, b, dist_table)
            if delta >= 0:
                break
        total_distance = calculate_total_distance(greedy_tour, dist_table)
        if total_distance < best_distance:
            best_tour = tuple(greedy_tour)
            best_distance = total_distance
    return best_tour, best_distance

# from solver_greedy.py
def greedy_solve(cities, dist_table):
    N = len(cities)

    current_city = random.randrange(0, N)
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist_table[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

# calculate total distance of a tour
def calculate_total_distance(tour, dist_table):
    total_distance = 0
    for i in range(len(tour)):
        if i == len(tour) - 1:
            total_distance += dist_table[tour[i]][tour[0]]
        else:
            total_distance += dist_table[tour[i]][tour[i + 1]]
    return total_distance

# calculate all segments of a tour
def all_segments(n):
    return ((i, j)
            for i in range(n)
            for j in range(i + 2, n + (i > 0)))

# reverse subtour of a tour
# if the reversed subtour is better than the original one,
# return the difference of distances
def reverse_subtour_2opt(tour, i, j, dist_table):
    A, B, C, D = tour[i - 1], tour[i], tour[(j - 1) % len(tour)], tour[j % len(tour)]
    d0 = dist_table[A][B] + dist_table[C][D]
    d1 = dist_table[A][C] + dist_table[B][D]
    if d0 > d1:
        tour[i:j] = reversed(tour[i:j])
        return -d0 + d1
    return 0

if __name__ == "__main__":
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour[0])
    # print("score: " + str(tour[1]))
