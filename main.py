import arcade
from modules.goo import Goo, draw_links
from random import randint
from modules.solid import Solid


class Window(arcade.Window):
    def __init__(self, width: int = 800, height: int = 600,
                 title: str = "Goo Simulation"):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLEU_DE_FRANCE)
        self.setup()

    def setup(self):
        self.sprites = arcade.SpriteList()
        self.goos = []
        self.won = False
        self.win_timer = 0.0  # Compteur pour la condition de victoire
        self.win_duration = 3.0  # Durée requise en secondes

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
        draw_links()
        self.sprites.draw()

        if self.won:
            arcade.draw_text("Gagné !", self.width // 2, self.height // 2,
                             arcade.color.BLACK, 60, anchor_x="center", bold=True)
        pass

    def is_goo_near_platform(self, goo, platform):
        """Check if a goo is near a platform (with some margin)"""
        contact_margin = 50

        dx = goo.center_x - platform.center_x
        dy = goo.center_y - platform.center_y

        if platform.shape == "ellipse":
            # For an ellipse, use the ellipse equation
            a = platform.width / 2 + contact_margin
            b = platform.height / 2 + contact_margin
            return (dx/a)**2 + (dy/b)**2 < 1

        else:  # rectangle
            # For a rectangle, check if within the bounding box
            half_width = platform.width / 2 + contact_margin
            half_height = platform.height / 2 + contact_margin
            return abs(dx) < half_width and abs(dy) < half_height

    def check_win_condition(self):
        """Check if any goo has reached the end platform"""
        if self.won or not self.goos:
            return False

        # Find goos touching the start platform
        start_goos = []
        for goo in self.goos:
            if self.is_goo_near_platform(goo, self.start):
                start_goos.append(goo)

        if not start_goos:
            return False

        visited = set()
        queue = start_goos.copy()

        for goo in queue:
            visited.add(goo)

        while queue:
            current_goo = queue.pop(0)

            # Check if the goo touches the end platform
            if self.is_goo_near_platform(current_goo, self.end):
                return True

            # add connected goos to the queue
            for other_goo in self.goos:
                if other_goo not in visited:
                    # check if there is a spring connection
                    if (current_goo, other_goo) in Goo.rest_lengths:
                        visited.add(other_goo)
                        queue.append(other_goo)

        return False

    def on_update(self, delta_time):
        # Move the goos while considering collisions
        for goo in self.goos:
            goo.move(self.solids)
        self.sprites.update()

        if not self.won:
            # Check if any goo has reached the end platform
            if self.check_win_condition():
                self.win_timer += delta_time
                if self.win_timer >= self.win_duration:
                    self.won = True
            else:
                self.win_timer = 0.0

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
