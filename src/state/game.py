import tcod


import state

from utilities.debug import MAPGEN


class MainGame(state._base.State):
    def __init__(self, engine):
        self.engine = engine

    def on_render(self, console: tcod.console.Console):
        self.engine.render(console)

    def ev_keydown(self, event: tcod.event.KeyDown):
        if event.sym == tcod.event.K_m and MAPGEN == True:
            self.engine.game_world.atlas[self.engine.game_world.map_index] = self.engine.game_world.generate_map()
