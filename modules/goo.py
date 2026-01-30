# goo.py
import arcade
import math

k = 100
dt = 1/60
g = 9.81/20
mass = 0.4
damping = 0.98
max_velocity = 5.0


def convert_to_meters(value) -> float:
    return value / 1000


def convert_to_pixels(value) -> float:
    return int(value * 1000)


class Goo(arcade.SpriteCircle):
    goos: list["Goo"] = []
    # store rest lengths between pairs of goos: {(goo1, goo2): (l0x, l0y)}
    rest_lengths: dict[tuple["Goo", "Goo"], tuple[float, float]] = {}

    def __init__(self, init_x: int, init_y: int, size: int) -> None:
        super().__init__(size, arcade.color.WILD_STRAWBERRY)
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

            dx_m = convert_to_meters(dx)
            dy_m = convert_to_meters(dy)

            d = math.sqrt(dx_m**2 + dy_m**2)

            l0 = math.sqrt(l0x**2 + l0y**2)

            if d < 1e-3:
                return 0, 0

            delta = d - l0

            F = k*delta

            Fx = F*(dx_m / d)
            Fy = F*(dy_m / d)

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

    def move(self, solid_list: list | None = None) -> None:
        F = self.global_force()

        self.v_x += dt*F[0]/mass
        self.v_y += dt*F[1]/mass - dt*g

        # add a damping factor to simulate energy loss
        # to avoid perpetual motion (found on the internet)
        self.v_x *= damping
        self.v_y *= damping

        # Limiter les vitesses pour éviter la divergence
        speed = math.sqrt(self.v_x**2 + self.v_y**2)
        if speed > max_velocity:
            self.v_x = (self.v_x / speed) * max_velocity
            self.v_y = (self.v_y / speed) * max_velocity

        dx = convert_to_pixels(self.v_x*dt)
        dy = convert_to_pixels(self.v_y*dt)

        self.center_y += dy
        self.center_x += dx

        if solid_list:
            for solid in solid_list:
                if arcade.check_for_collision(self, solid):
                    self.center_x -= dx
                    self.center_y -= dy
                    self.v_x = 0
                    self.v_y = 0
                    break


def draw_links():
    """Dessiner tous les liens (ressorts) entre les goos connectés."""
    drawn_pairs = set()

    for (goo1, goo2), _ in Goo.rest_lengths.items():
        # create a unique key for the pair to avoid drawing twice
        pair_key = tuple(sorted([id(goo1), id(goo2)]))

        if pair_key not in drawn_pairs:
            drawn_pairs.add(pair_key)
            arcade.draw_line(goo1.center_x, goo1.center_y,
                             goo2.center_x, goo2.center_y,
                             arcade.color.DARK_GREEN, 2)
