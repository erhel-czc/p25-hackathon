import arcade
from modules.goo import Goo
from random import randint
from modules.solid import Solid


class Window(arcade.Window):
    def __init__(self, width: int = 800, height: int = 600,
                 title: str = "Goo Simulation"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.setup()

    def setup(self):
        self.sprites = arcade.SpriteList()
        self.goos = []

        self.solids = []

        self.start = Solid(randint(50, self.width - 50),
                           randint(50, self.height - 50))
        self.solids.append(self.start)

        while True:
            self.end = Solid(randint(50, self.width - 50),
                             randint(50, self.height - 50))

            if not self.end.collides_with(self.start):
                break
        self.solids.append(self.end)

        # Add obstacles to the SpriteList
        for solid in self.solids:
            self.sprites.append(solid)

    def on_draw(self):
        self.clear()
        self.sprites.draw()

    def on_update(self, delta_time):
        # Move the goos while considering collisions
        for goo in self.goos:
            goo.move(self.solids)
        self.sprites.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            g = Goo(x, y, 10)
            if not (arcade.check_for_collision(g, self.start)
                    or arcade.check_for_collision(g, self.end)):
                g.start()
                self.goos.append(g)
                self.sprites.append(g)


if __name__ == "__main__":
    window = Window()
    arcade.run()
