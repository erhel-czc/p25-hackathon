import arcade

class Link:
    def __init__(self, goo_a, goo_b):
        self.goo_a = goo_a
        self.goo_b = goo_b

    def draw(self):
        arcade.draw_line(
            self.goo_a.center_x,
            self.goo_a.center_y,
            self.goo_b.center_x,
            self.goo_b.center_y,
            arcade.color.BLACK,
            2
        )
