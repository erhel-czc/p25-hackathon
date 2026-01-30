import arcade
from modules.goo import Goo
from random import randint
from modules.solid import Solid


class Window(arcade.Window):
    def __init__(self, width: int = 800, height: int = 600, title: str = "Goo Simulation"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.setup()

    def setup(self):
        self.sprites = arcade.SpriteList()
        self.goos = []

        for goo in self.goos:
            self.sprites.append(goo)

        self.start = Solid(randint(50, self.width - 50),
                           randint(50, self.height - 50))

        while True:
            self.end = Solid(randint(50, self.width - 50),
                             randint(50, self.height - 50))

            if not self.end.collides_with(self.start):
                break

        self.sprites.append(self.start)
        self.sprites.append(self.end)

    def on_draw(self):
        self.clear()
        self.sprites.draw()
        pass

    def on_update(self, delta_time):
        for goo in self.goos:
            goo.move()
            
        self.sprites.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            g = Goo(x, y, 10)
            self.goos.append(g)
            self.sprites.append(g)


if __name__ == "__main__":
    window = Window()
    arcade.run()
