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
    # generate greedy tours and apply 4-opt to each of them
    # select the best tour of all
    for i in tqdm.tqdm(range(10)):
        dist_table = create_distance_table(cities)
        greedy_tour = greedy_solve(cities, dist_table)
        while True:
            delta = 0
            for (a, b, c, d) in all_segments(len(cities)):
                delta += reverse_subtour_4opt(greedy_tour, a, b, c, d,dist_table)
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

# return all possible segments of a tour
def all_segments(n):
    return ((i, j, k, l)
            for i in range(n)
            for j in range(i + 2, n)
            for k in range(j + 2, n + (i > 0))
            for l in range(k + 2, n + (i > 0) + (j > 0)))

# reverse a subtour if it improves the total distance
# return the difference of total distance before and after the reverse
def reverse_subtour_4opt(tour, i, j, k, l, dist_table):
    A, B, C, D, E, F, G, H = tour[(i - 1)], tour[i], tour[(j - 1)], tour[j], tour[(k - 1)], tour[k], tour[(l - 1) % len(tour)], tour[l % len(tour)]
    d0 = dist_table[A][B] + dist_table[C][D] + dist_table[E][F] + dist_table[G][H]
    d1 = dist_table[A][C] + dist_table[B][D] + dist_table[E][F] + dist_table[G][H]
    d2 = dist_table[A][B] + dist_table[C][E] + dist_table[D][F] + dist_table[G][H]
    d3 = dist_table[A][D] + dist_table[E][B] + dist_table[C][F] + dist_table[G][H]
    d4 = dist_table[H][B] + dist_table[C][D] + dist_table[E][F] + dist_table[G][A]
    d5 = dist_table[A][H] + dist_table[C][D] + dist_table[E][F] + dist_table[G][B]
    d6 = dist_table[A][B] + dist_table[H][D] + dist_table[E][F] + dist_table[G][C]
    d7 = dist_table[A][B] + dist_table[C][H] + dist_table[E][F] + dist_table[G][D]
    d8 = dist_table[A][B] + dist_table[C][D] + dist_table[H][F] + dist_table[G][E]

    if d0 > d1:
        tour[i:j] = reversed(tour[i:j])
        return -d0 + d1
    if d0 > d2:
        tour[j:k] = reversed(tour[j:k])
        return -d0 + d2
    if d0 > d4:
        tour[i:k] = reversed(tour[i:k])
        return -d0 + d4
    if d0 > d3:
        tour[i:k] = reversed(tour[i:k])
        tour[j:k] = reversed(tour[j:k])
        return -d0 + d3
    if d0 > d5:
        tour[i:j] = reversed(tour[i:j])
        tour[j:k] = reversed(tour[j:k])
        return -d0 + d5
    if d0 > d6:
        tour[k:l] = reversed(tour[k:l])
        return -d0 + d6
    if d0 > d7:
        tour[i:l] = reversed(tour[i:l])
        return -d0 + d7
    if d0 > d8:
        tour[i:j] = reversed(tour[i:j])
        tour[k:l] = reversed(tour[k:l])
        return -d0 + d8
    return 0


if __name__ == "__main__":
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour[0])
    # print("score: " + str(tour[1]))
