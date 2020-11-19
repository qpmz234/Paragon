import tcod

import copy


import entities.actors as actors

from engine import Engine
from map.world import GameWorld


MAP_WIDTH = 63
MAP_HEIGHT = 47
MAX_ROOMS = 30
ROOM_MIN_SIZE = 6
ROOM_MAX_SIZE =10


def new_game():
    player = copy.deepcopy(actors.player)
    engine = Engine(player)
    engine.game_world = GameWorld(
        engine = engine,
        map_width = MAP_WIDTH,
        map_height = MAP_HEIGHT,
        max_rooms = MAX_ROOMS,
        room_min_size = ROOM_MIN_SIZE,
        room_max_size = ROOM_MAX_SIZE,
    )
    player.place(20, 20, engine.game_world.curr_map)

    return engine
