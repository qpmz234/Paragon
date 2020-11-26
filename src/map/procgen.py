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

def CA_smooth(tile_mi, map, hi, lo):
    neighbors = neighborsM(tile_mi)
    count = 0
    for i in neighbors:
        if map[i]:
            count +=1

    if count > hi:
        return 1
    elif count < lo:
        return 0
    else:
        return None


def generate_caves(
    parent,
    map_width,
    map_height,

):

    # TODO: pass as variables

    NUM_POINTS = 10
    SCALE = 5
    DIST_WIDTH = 2

    # Init map array and create copy for cost matrix

    tilegen = np.pad(np.ones((map_width, map_height), dtype=np.int32), (1,1), mode='constant', constant_values=1)
    cost = copy.deepcopy(tilegen)

    # Generate points and compute edges

    points = np.vstack((np.random.randint(1, map_width, NUM_POINTS), np.random.randint(1, map_height, NUM_POINTS))).transpose()
    edges = utilities.graph.rel_neighborhood(points)

    # Weight edges and apply to dist matrix

    for edge in edges:
        (start, end) = edge
        line_points = tcod.los.bresenham(start, end)
        rand_width = -rng.poisson(SCALE)
        for line_point in line_points:
            tilegen[tuple(line_point)] = max(min(rand_width, -(SCALE-DIST_WIDTH)), -(SCALE+DIST_WIDTH))

    # Compute carving probabilities using Dijkstra map

    dist = np.select([tilegen < 0], [tilegen])
    tcod.path.dijkstra2d(dist, cost, 1, 1)
    dist = dist.astype(float) / -(SCALE-DIST_WIDTH)

    # Force edges to be open, and retain a copy to lock smoothing routine

    tilegen = np.select([tilegen < 0], [0], default=1)
    lock = copy.deepcopy(tilegen)

    # Perform probabilistic carving around edges

    with np.nditer(tilegen[1:, 1:], flags=["multi_index"], op_flags=["readwrite"], order="F") as it:
        for tile in it:
            sample = rng.random()
            if sample < dist[it.multi_index]:
                tilegen[it.multi_index] = 0

    # Perform smoothing, with edges locked

    PASSES = 5

    for _ in range(PASSES):
        with Sync(tilegen) as sync:
            with np.nditer(tilegen[1:, 1:], flags=["multi_index"], op_flags=["readwrite"], order="F") as it:
                for tile in it:
                    if lock[it.multi_index]:
                        count = CA_smooth(it.multi_index, sync, 4, 4)
                        if type(count) == int:
                            tilegen[it.multi_index] = count

    # Final, biased, smoothing to expand narrow tunnels

    with Sync(tilegen) as sync:
        with np.nditer(tilegen[1:, 1:], flags=["multi_index"], op_flags=["readwrite"], order="F") as it:
            for tile in it:
                if lock[it.multi_index]:
                    count = CA_smooth(it.multi_index, sync, 6, 7)
                    if type(count) == int:
                        tilegen[it.multi_index] = count

    # Convert binary array to map data

    tiles = np.where(tilegen[1:-1, 1:-1], tileset.generic.wall, tileset.generic.floor)
    # tiles = np.where(tilegen[1:-1, 1:-1], tileset.generic.wall, tileset.generic.floor)
    curr_map = GameMap(parent, map_width, map_height, tiles=tiles)

    return curr_map, points, edges, lock
