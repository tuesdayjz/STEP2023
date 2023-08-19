import sys
import math

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
    cities_num = len(cities)
    junction_set = {i for i in range(1, cities_num)}
    dist_table = create_distance_table(cities)
    memo = {}
    min_distance = dp(0, junction_set, 0, dist_table, memo)
    # print("score: " + str(min_distance))
    return tuple(get_route(memo, dist_table))

# memo is a dict, whose key is (start, junction_set, goal)
# e.g. memo[(0, (1, 2, 3), 0)] = 100
#
def dp(start, junction_set, goal, dist_table, memo):
    # base case
    if len(junction_set) == 0:
        memo[(start, tuple(junction_set - {start}),
                goal)] = dist_table[start][goal]
        return dist_table[start][goal]

    # recursive case
    min_distance = float("inf")
    # try all possible cities that could be the next city
    for city in junction_set - {start}:
        # prev could be a key of memo
        prev = (city, tuple(junction_set - {start, city}), goal)
        if prev not in memo:
            # if prev is not in memo, calculate it recursively
            memo[prev] = dp(
                city, junction_set -
                {start, city}, goal, dist_table, memo
            )
        # distance is, start~city + city~goal
        distance = dist_table[start][city] + memo[prev]
        if distance < min_distance:
            min_distance = distance
    # pick the minimum distance
    return min_distance

# get route from memo and put it in a dict,
# whose key is length of junction_set.
def get_route(memo, dist_table):
    memo_dict_in_length = {}
    route = [0]
    for start, junction_set, goal in memo:
        if len(junction_set) not in memo_dict_in_length:
            memo_dict_in_length[len(junction_set)] = [(start, junction_set, goal)]
        else:
            memo_dict_in_length[len(junction_set)].append((start, junction_set, goal))
    start = 0
    cost = 0
    # get route using memo
    # start from the longest junction_set
    for junction_length in reversed(range(len(dist_table) - 1)):
        min_distance = float("inf")
        min_city = -1
        for memo_start, junction_set, memo_goal in memo_dict_in_length[junction_length]:
            # distance is, start~cmemo_start + memo_start~goal
            distance = dist_table[start][memo_start] + memo[(memo_start, junction_set, memo_goal)] + cost
            if distance < min_distance and memo_start not in route:
                ok = True
                for city in junction_set:
                    # if city is already in route, then this route is not valid
                    if city in route:
                        ok = False
                        break
                if ok:
                    min_distance = distance
                    min_city = memo_start
        route.append(min_city)
        cost += dist_table[start][min_city]
        start = min_city
    return route


if __name__ == "__main__":
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
