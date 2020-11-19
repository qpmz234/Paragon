import tcod


import interface.mainmenu

import state._base

import utilities.meta as meta


class MainMenu(state._base.State):
    def __init__(self):
        super().__init__()
        self.interface = interface.mainmenu.UI_MainMenu()

    def on_render(self, console: tcod.Console):
        self.interface.render(console)

    def ev_keydown(self, event: tcod.event.KeyDown):
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        # elif event.sym == tcod.event.K_c:
        #     try:
        #         return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
        #     except FileNotFoundError:
        #         return input_handlers.PopupMessage(self, "No saved game to load.")
        #     except Exception as exc:
        #         traceback.print_exc()  # Print to stderr.
        #         return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return state.game.MainGame(meta.new_game())

        return None
