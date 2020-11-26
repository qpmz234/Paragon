import tcod
import traceback
import numpy as np
import sys


import state.menu
import state.game

# import utilities.color
import utilities.exceptions as exceptions

WIDTH = 96
HEIGHT = 54

RESOLUTION = 16

def main() -> None:

    tileset = tcod.tileset.load_tilesheet(
        "resources/tileset_"+str(RESOLUTION)+"x"+str(RESOLUTION)+".png",
        16, 16, tcod.tileset.CHARMAP_CP437,
    )

    cState: state._base.State = state.menu.MainMenu()

    with tcod.context.new_terminal(
        WIDTH,
        HEIGHT,
        tileset=tileset,
        title="Paragon",
        vsync=True,
    ) as context:
        console = tcod.Console(WIDTH, HEIGHT, order="F")
        try:
            while True:
                console.clear()
                cState.on_render(console=console)
                context.present(console, keep_aspect=True, integer_scaling=True)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        cState = cState.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    # if isinstance(state, state._base.State):
                    #     state.engine.interface.message_log.add_message(
                    #         traceback.format_exc(), utilities.color.error
                    #    )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            # TODO: Save Game Code
            raise
        except BaseException:  # Save on any other unexpected exception.
            # TODO: Save Game Code
            raise

if __name__ == "__main__":
    main()
