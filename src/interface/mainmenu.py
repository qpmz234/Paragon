import tcod
from interface._base import Interface


import utilities.color as color


class UI_MainMenu(Interface):
    def __init__(self):
        super().__init__()
        self.BG = tcod.image.load("resources/menu.png")[:, :, :3]

    def render(self, console: tcod.console.Console):
        console.draw_semigraphics(self.BG, 0, 0)

        console.print(
            console.width // 2,
            console.height - 2,
            "(C) 2020 NINEFOURFIVE Games",
            fg=color.copyright,
            alignment=tcod.CENTER,
        )
        for i, text in enumerate(
            ["[N]ew Game", "[C]ontinue", "[O]ptions ", "[Q]uit    "]
        ):
            console.print(
                console.width // 2,
                console.height // 2 + 10 + i,
                text,
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )
