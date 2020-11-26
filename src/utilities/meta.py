import tcod

import copy


import entities.actors as actors

from engine import Engine
from map.world import GameWorld


MAP_WIDTH = 63
MAP_HEIGHT = 47


def new_game():
    player = copy.deepcopy(actors.player)
    engine = Engine(player)
    engine.game_world = GameWorld(
        engine = engine,
        map_width = MAP_WIDTH,
        map_height = MAP_HEIGHT,
    )
    player.place(20, 20, engine.game_world.curr_map)

    return engine
