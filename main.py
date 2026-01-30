import arcade
from modules.goo import Goo
from random import randint

class Window(arcade.Window):
    def __init__(self, width: int = 800, height: int = 600, title: str = "Simulation"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.setup()

    def setup(self):
        self.sprites = arcade.SpriteList()

        self.goos = [Goo(randint(0, self.width), randint(0, self.height), 10, 25) for _ in range(50)]

        for goo in self.goos:
            self.sprites.append(goo)

    def on_draw(self):
        self.clear()
        self.sprites.draw()
        pass

    def on_update(self, delta_time):
        for goo in self.goos:
            goo.move()
        self.sprites.update()

def main():
    pass

if __name__ == "__main__":
    window = Window()
    arcade.run()
