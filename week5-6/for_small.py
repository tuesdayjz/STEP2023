#!/usr/bin/env python3

import sys
import itertools
import math

from common import print_tour, read_input


def calculate_distance(point1, point2):
    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def generate_all_paths(cities):
    # start is 0
    cities_list = list(range(1, len(cities)))
    all_paths = list(itertools.permutations(cities_list))
    reduced_paths = all_paths
    # remove reversed path
    for path in all_paths:
        if tuple(reversed(path)) in reduced_paths:
            reduced_paths.remove(tuple(reversed(path)))
    return reduced_paths


def solve(cities):
    all_paths = generate_all_paths(cities)
    path_len_dict = {}
    # record {path: length} in dict
    for path in all_paths:
        prev = 0
        distance = 0
        for i in range(len(path)):
            now = path[i]
            distance += calculate_distance(cities[prev], cities[now])
            prev = path[i]
        distance += calculate_distance(cities[now], cities[0])
        path_len_dict[path] = distance
    path_len_dict = sorted(
        path_len_dict.items(), key=lambda path_len_dict: path_len_dict[1]
    )
    min_path = path_len_dict[0]
    return min_path


if __name__ == "__main__":
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    route = tuple([0]) + tour[0]
    print_tour(route)
    # print("score: " + str(tour[1]))
