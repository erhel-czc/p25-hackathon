import numpy as np
import arcade
from random import randint, choice


class Solid(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.width = randint(100, 200)
        self.height = randint(50, 100)


        self.center_x = x
        self.center_y = y
        
        # Choix aléatoire de la forme
        shape = choice(["ellipse", "rectangle"])

        if shape == "ellipse":
            diameter = min(self.width, self.height)
            self.texture = arcade.make_circle_texture(
                diameter,
                arcade.color.DARK_GREEN
            )


        elif shape == "rectangle":
            self.texture = arcade.make_soft_square_texture(
                max(self.width, self.height),
                arcade.color.DARK_BLUE,
                outer_alpha=255
            )

    #pour que le départ et l'arrivée ne se superposent pas 
    def collides_with(self, other):
        dx = self.center_x - other.center_x
        dy = self.center_y - other.center_y
        distance = (dx**2 + dy**2) ** 0.5

        min_distance = (self.width + other.width) / 2
        return distance < min_distance
