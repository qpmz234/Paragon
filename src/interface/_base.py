import tcod


class Interface:
    def __init__(self, engine = None):
        if engine:
            self.engine = engine

    def render(self):
        raise NotImplementedError
