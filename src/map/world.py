import map.procgen as procgen


class GameWorld:
    """
    Holds global settings, handles GameMap generation, and contains the atlas.
    """

    def __init__(
        self,
        *,
        engine,
        map_width: int,
        map_height: int,
        map_index: int = 0
    ):
        self.engine = engine
        self.map_width = map_width
        self.map_height = map_height
        self.map_index = map_index

        self.atlas = []

        self.atlas.append(self.generate_map())

    @property
    def curr_map(self):
        return self.atlas[self.map_index]

    def ascend(self):
        if self.map_index > 0:
            self.map_index -= 1
        else:
            pass

    def descend(self):
        self.map_index += 1

        while (len(self.atlas) - 1) < self.map_index:
            self.atlas.append(self.generate_map())

    def generate_map(self):
        tilemap, points, edges, lock = procgen.generate_caves(
            parent=self,
            map_width=self.map_width,
            map_height=self.map_height,
        )

        return tilemap
