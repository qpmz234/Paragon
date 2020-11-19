import tcod

class State(tcod.event.EventDispatch):
    def handle_events(self, event: tcod.event.Event):
        state = self.dispatch(event)
        if isinstance(state, State):
            return state
        else:
            return self

    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()

    def on_render(self, console: tcod.Console):
        raise NotImplementedError()
