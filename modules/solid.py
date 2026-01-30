import numpy as np
import arcade
from random import randint, choice
from PIL import Image, ImageDraw


class Solid(arcade.Sprite):
    def __init__(self, x, y, solid_size=40):
        super().__init__()

        self.center_x = x
        self.center_y = y
        self.solid_size = solid_size

        # Choix aléatoire de la forme
        shape = choice(["circle", "rectangle"])

        if shape == "circle":
            self.texture = arcade.make_circle_texture(
                solid_size,
                arcade.color.DARK_GREEN
            )

        elif shape == "rectangle":
            self.texture = arcade.make_soft_square_texture(
                solid_size,
                arcade.color.DARK_BLUE,
                outer_alpha=255
            )