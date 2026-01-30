import arcade
import math

k = 100


class Goo(arcade.SpriteCircle):
    # store all goos created in a list called goos
    goos: list["Goo"] = []

    def __init__(self, init_x: int, init_y: int, size: int, mass: int) -> None:
        super().__init__(size, arcade.color.ARMY_GREEN)
        self.center_x = init_x
        self.center_y = init_y
        self.mass = mass

        self.initial_x = init_x
        self.initial_y = init_y

        Goo.goos.append(self)

    def distance_to(self, other: "Goo") -> tuple[float, float]:
        dx = other.center_x - self.center_x
        dy = other.center_y - self.center_y

        return dx, dy

    def force_from(self, other: "Goo") -> tuple[float, float]:
        """
        Compute the force from self to other.

        Parameters
        ----------
        other : Goo
            The other goo from which the force is computed.

        Returns
        -------
        Fx, Fy : tuple[float, float]
            The x and y components of the force from self to other.
        """

        l0 = math.sqrt((self.initial_x - other.initial_x)**2 +
                       (self.initial_y - other.initial_y)**2)

        dx, dy = self.distance_to(other)
        Fx = -k*(dx - l0)
        Fy = -k*(dy - l0)

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
        pass
