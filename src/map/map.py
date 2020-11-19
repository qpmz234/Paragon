import numpy as np  # type: ignore

from entities._base import Actor, Item
import tileset.generic

from utilities.debug import FULLBRIGHT


class GameMap:


    def __init__(
        self, parent, width, height, entities = (), tiles = None
    ):

        self.parent = parent
        self.width, self.height = width, height
        self.entities = set(entities)
        if type(tiles) is None:
            tiles = np.full((width, height), fill_value=tileset.generic.wall, order="F")
        self.tiles = tiles

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before

    @property
    def engine(self):
        return self.parent.engine

    @property
    def actors(self):
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self):
        """Iterate over this maps ground items."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Item)
        )

    def get_impassable_entity_at_location(
        self, location_x: int, location_y: int,
    ):
        """If an impassable entity is present at (x,y), return that entity"""
        for entity in self.entities:
            if (
                entity.impassable
                and entity.x == location_x
                and entity.y == location_y
            ):
                return entity

        return None

    def get_actor_at_location(self, x: int, y: int):
        """If an actor is present at (x,y), return that actor"""
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor

        return None

    def in_bounds(self, x: int, y: int):
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console):
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """

        if not FULLBRIGHT:
            console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
                condlist=[self.visible, self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=tiles.generic.SHROUD,
            )
        else:
            console.tiles_rgb[0 : self.width, 0 : self.height] = self.tiles["light"]

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color,
                )
