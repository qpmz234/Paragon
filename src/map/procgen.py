import tcod
import copy
import numpy as np
from numpy.random import default_rng

from map.map import GameMap
import tileset.generic
from utilities.misc import Sync
import utilities.graph

rng = default_rng()

def neighborsM(tile_index):
    x, y = tile_index
    return [(x1, y1) for x1 in range(x-1, x+2)
                    for y1 in range(y-1, y+2)
                    if (x1, y1) != (x, y)]

def CA_smooth(tile_mi, map):
    neighbors = neighborsM(tile_mi)
    count = 0
    for i in neighbors:
        if map[i]:
            count +=1

    if count > 4:
        return 1
    elif count < 4:
        return 0
    else:
        return None

def generate_layout(
    parent,
    max_rooms,
    room_min_size,
    room_max_size,
    map_width,
    map_height,

):

    NUM_POINTS = 10

    points = np.vstack((np.random.randint(1, map_width, NUM_POINTS), np.random.randint(1, map_height, NUM_POINTS))).transpose()

    edges = utilities.graph.rel_neighborhood(points)

    tilegen = np.pad(np.ones((map_width, map_height), dtype=np.int32), (1,1), mode='constant', constant_values=1)
    cost = copy.deepcopy(tilegen)

    for edge in edges:
        (start, end) = edge
        line_points = tcod.los.bresenham(start, end)
        for line_point in line_points:
            tilegen[tuple(line_point)] = 0

    SCALE = 8

    dist = np.select([tilegen == 0], [-SCALE])
    tcod.path.dijkstra2d(dist, cost, 1, 1)
    dist = dist.astype(float) / -SCALE

    with np.nditer(tilegen[1:, 1:], flags=["multi_index"], op_flags=["readwrite"], order="F") as it:
        for tile in it:
            sample = rng.random()
            if sample < dist[it.multi_index]:
                tilegen[it.multi_index] = 0

    PASSES = 5

    for _ in range(PASSES):
        with Sync(tilegen) as sync:
            with np.nditer(tilegen[1:, 1:], flags=["multi_index"], op_flags=["readwrite"], order="F") as it:
                for tile in it:
                    count = CA_smooth(it.multi_index, sync)
                    if type(count) == int:
                        tilegen[it.multi_index] = count

    tiles = np.where(tilegen[1:-1, 1:-1], tileset.generic.wall, tileset.generic.floor)
    # tiles = np.where(tilegen[1:-1, 1:-1], tileset.generic.wall, tileset.generic.floor)
    curr_map = GameMap(parent, map_width, map_height, tiles=tiles)

    return curr_map
