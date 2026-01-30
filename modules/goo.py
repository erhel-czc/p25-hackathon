# goo.py
import arcade
import math

k = 100
dt = 1/60
g = 9.81/20
mass = 0.4

# --- Fonctions de conversion ---
def convert_to_meters(value) -> float:
    return value / 1000

def convert_to_pixels(value) -> float:
    return int(value * 1000)


class Goo(arcade.SpriteCircle):
    goos: list["Goo"] = []
    # store rest lengths between pairs of goos: {(goo1, goo2): (l0x, l0y)}
    rest_lengths: dict[tuple["Goo", "Goo"], tuple[float, float]] = {}

    def __init__(self, init_x: int, init_y: int, size: int) -> None:
        super().__init__(size, arcade.color.ARMY_GREEN)
        self.center_x = init_x
        self.center_y = init_y

        self.initial_x = init_x
        self.initial_y = init_y
        self.v_x = 0
        self.v_y = 0

    def start(self) -> None:
        # Calculate and store rest lengths with all existing goos
        for other in Goo.goos:
            l0x = convert_to_meters(other.center_x - self.center_x)
            l0y = convert_to_meters(other.center_y - self.center_y)

            # Only create spring link if distance is less than 20 cm (0.2 m)
            distance = math.sqrt(l0x**2 + l0y**2)
            if distance < 0.2:
                Goo.rest_lengths[(self, other)] = (l0x, l0y)
                Goo.rest_lengths[(other, self)] = (-l0x, -l0y)

        Goo.goos.append(self)

    def distance_to(self, other: "Goo") -> tuple[float, float]:
        dx = other.center_x - self.center_x
        dy = other.center_y - self.center_y

        return dx, dy

    def force_from(self, other: "Goo") -> tuple[float, float]:
        """
        Compute the force from self to other.

        Returns
        -------
        Fx, Fy : tuple[float, float]
            The x and y components of the force from self to other.
        """

        # Get the stored rest length for this pair
        l0x, l0y = Goo.rest_lengths.get((self, other), (0, 0))

        if l0x == 0 and l0y == 0:
            return 0, 0

        else:
            dx, dy = self.distance_to(other)

            Fx = k*(dx - l0x)
            Fy = k*(dy - l0y)

            return Fx, Fy

    def global_force(self):
        """
        Compute the total force from all other goos.
        """

        Fx_total = 0
        Fy_total = 0

        other_goos = [goo for goo in Goo.goos if goo != self]

        for other in other_goos:
            Fx, Fy = self.force_from(other)
            Fx_total += Fx
            Fy_total += Fy

        return Fx_total, Fy_total

    def move(self) -> None:
        F = self.global_force()
        F = 0.0, 0.0

        self.v_x += dt*F[0]/mass
        self.v_y += dt*F[1]/mass - dt*g

        dx = convert_to_pixels(self.v_x*dt)
        dy = convert_to_pixels(self.v_y*dt)

        # --- Déplacement horizontal ---
        self.center_x += dx
        if solid_list:
            for solid in solid_list:
                if arcade.check_for_collision(self, solid):
                    self.center_x -= dx
                    self.v_x = 0
                    break

        # --- Déplacement vertical ---
        self.center_y += dy
        if solid_list:
            for solid in solid_list:
                if arcade.check_for_collision(self, solid):
                    self.center_y -= dy
                    self.v_y = 0
                    break
