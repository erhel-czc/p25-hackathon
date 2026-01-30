import arcade

class Goo(arcade.SpriteCircle):
    # store all goos created in a list called goos 
    goos: list["Goo"] = []

    def __init__(self, init_x: int, init_y: int, size: int, mass: int) -> None:
        super().__init__(size, arcade.color.BLUE)
        self.center_x = init_x
        self.center_y = init_y
        self.mass = mass

        Goo.goos.append(self)

    def move(self) -> None:
        pass

    def compute_deltas(self):
        other_goos = [goo for goo in Goo.goos if goo != self]

        pass