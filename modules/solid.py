import arcade
from random import randint, choice
import math


class Solid(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.width = randint(120, 200)
        self.height = randint(100, 150)

        self.center_x = x
        self.center_y = y

        # Choix aléatoire de la forme
        self.shape = choice(["ellipse", "rectangle"])

        if self.shape == "ellipse":
            diameter = min(self.width, self.height)
            self.texture = arcade.make_circle_texture(diameter, arcade.color.DARK_GREEN)

        elif self.shape == "rectangle":
            size = max(self.width, self.height)
            self.texture = arcade.make_soft_square_texture(size, arcade.color.DARK_BLUE, outer_alpha=255)
           
    def _ellipse_hitbox(self, a, b, n_points=12):
        """Crée une hitbox approximative pour une ellipse"""
        points = []
        for i in range(n_points):
            angle = 2 * math.pi * i / n_points
            x = a * math.cos(angle)
            y = b * math.sin(angle)
            points.append((x, y))
        return points

    # Pour que le départ et l'arrivée ne se superposent pas
    def collides_with(self, other):
        dx = self.center_x - other.center_x
        dy = self.center_y - other.center_y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        min_distance = (self.width + other.width) / 2
        return distance < min_distance
