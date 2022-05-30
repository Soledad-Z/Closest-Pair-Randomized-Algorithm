import math
import random
import pandas as pd
from typing import List, Tuple, Dict


class Point:
    def __init__(self, name: str, x: float, y: float):
        self.id = name
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.id} {self.x} {self.y}'


class Grid:
    def __init__(self, pos: Point, d: float):
        self.pos = pos  # Coordinates of the lower left corner of the grid
        self.d = d  # Side length of the grid

    def isInGrid(self, point: Point):
        """
        check if the point in this grid
        :param point: the point to be checked
        :return: Ture if in the grid
        """

        if (self.pos.x <= point.x <= (self.pos.x + self.d)) and (self.pos.y <= point.y <= (self.pos.y + self.d)):
            return True

        return False


def distance(p1: Point, p2: Point):
    """
    calculate the distance of tow points
    :param p1: point
    :param p2: point
    :return: distance
    """

    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def make_grids(points: List[Point], theta) -> Tuple[Dict[int, List[Point]], Tuple]:
    """
    Divide the range of all points into uniform grids
    :param points: the list of all points
    :param theta: the side length of every grid
    :return: A dictionary(hash map) that stores the corresponding points of each grid, the shape of grids(num_x, num_y)
    """

    max_x, max_y = max(points, key=lambda p: p.x), max(points, key=lambda p: p.y)
    min_x, min_y = min(points, key=lambda p: p.x), min(points, key=lambda p: p.y)

    e = 1e-5  # a tiny offset

    width = max_x.x - min_x.x + e
    height = max_y.y - min_y.y + e

    num_x = math.ceil(width / theta)
    num_y = math.ceil(height / theta)

    grid_list = []  # the list to store grids
    left_down = (min_x.x-e, min_y.y-e)
    # Generate each grid
    for i in range(num_x):
        for j in range(num_y):
            tempX, tempY = left_down[0] + i * theta, left_down[1] + j * theta
            grid_list.append(Grid(Point('', tempX, tempY), theta))

    # Store the points belonging to the grid into the corresponding hash table
    hash_map = {i: [] for i in range(len(grid_list))}

    for p in points:
        for idx, s in enumerate(grid_list):
            if s.isInGrid(p):
                hash_map[idx].append(p)

    return hash_map, (num_x, num_y)


def search_neighbor_grids(grids_list: Dict[int, List[Point]], shape: Tuple):
    """
    search in the neighbor 8 grids to find the min_distance of points, make the algorithmic complexity is O(n)
    :param grids_list: A dictionary(hash map) that stores the corresponding points of each grid
    :param shape: the shape of grids
    :return: the minimum distance of all point pairs
    """

    numX, numY = shape[0], shape[1]

    min_distance = float('Inf')
    # Search for the nearest point pairs in the 8 nearby grids
    for i in range(numX):
        for j in range(numY):
            temp = []
            if 0 <= i+1 < numX:
                temp += grids_list[(i + 1) * numY + j]
            elif 0 <= j+1 < numY:
                temp += grids_list[i * numY + (j + 1)]
            elif 0 <= i-1 < numX:
                temp += grids_list[(i - 1) * numY + j]
            elif 0 <= j-1 < numY:
                temp += grids_list[i * numY + (j - 1)]
            elif 0 <= i+1 < numX and 0 <= j+1 < numY:
                temp += grids_list[(i + 1) * numY + (j + 1)]
            elif 0 <= i-1 < numX and 0 <= j+1 < numY:
                temp += grids_list[(i - 1) * numY + (j + 1)]
            elif 0 <= i-1 < numX and 0 <= j-1 < numY:
                temp += grids_list[(i - 1) * numY + (j - 1)]
            elif 0 <= i+1 < numX and 0 <= j-1 < numY:
                temp += grids_list[(i + 1) * numY + (j - 1)]

            temp += grids_list[i * numY + j]

            for q in grids_list[i * numY + j]:
                for k in temp:
                    if q.id != k.id:
                        min_distance = min(min_distance, distance(q, k))

    return min_distance


def closest_pair_randomized_algorithms(point_list: List[Point]):
    """
    A randomized algorithm to find the minimum distance of all point pairs, which complexity is O(n).
    :param point_list: the list of points
    :return: the minimum distance of all point pairs
    """

    n = len(point_list)

    # Randomly select floor(sqrt(n)) points as random_points
    random_idx = random.sample(range(n), k=math.floor(math.sqrt(n)))
    random_points = []

    for i in random_idx:
        random_points.append(point_list[i])

    # Calculate the distance of point pairs in random_points, and get the distance of the nearest point pair
    minDis = float('Inf')
    for i in range(len(random_points)):
        for j in range(i+1, len(random_points)):
            minDis = min(minDis, distance(random_points[i], random_points[j]))

    del random_idx, random_points

    hash_map, _ = make_grids(point_list, minDis)

    # Find the index of the grid with the highest number of points
    max_point_square_idx = max(hash_map, key=lambda i: len(hash_map[i]))

    # Make sure the number of points in the grid with the highest number of points less than sqrt(n)
    # The number of points in the grid with the highest number of points exceeds sqrt(n)
    if len(hash_map[max_point_square_idx]) > math.floor(math.sqrt(n)):
        # Divide the grid into four equal parts
        while len(hash_map[max_point_square_idx]) > math.floor(math.sqrt(n)):
            minDis /= 2
            hash_map, _ = make_grids(point_list, minDis)

            max_point_square_idx = max(hash_map, key=lambda i: len(hash_map[i]))

    # The number of points in the grid with the highest number of points less than sqrt(n)
    p_list = hash_map[max_point_square_idx]
    for i in range(len(p_list)):
        for j in range(i + 1, len(p_list)):
            minDis = min(minDis, distance(p_list[i], p_list[j]))

    # Make sure minDis greater than the actual minimum distance
    minDis += 1e-5

    # Construct a grid with the new minDis as the edge length
    hash_map, shape = make_grids(point_list, minDis)

    # Find the smallest distance in 8 nearby grids
    result = search_neighbor_grids(hash_map, shape)

    return result


if __name__ == '__main__':
    data = pd.read_csv('data.csv')
    pointList = []
    for idx, x, y in zip(data['ID'], data['lat'], data['lon']):
        pointList.append(Point(idx, x, y))

    min_dis = closest_pair_randomized_algorithms(pointList)
    print(min_dis)
