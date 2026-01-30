# goo.py
import arcade
import math

k = 0.5  # constante ressort
dt = 0.1
g = 9.81/20
mass = 0.4

# --- Fonctions de conversion ---
def convert_to_meters(value) -> float:
    return value / 1000

def convert_to_pixels(value) -> float:
    return int(value * 1000)


class Goo(arcade.SpriteCircle):
    goos: list["Goo"] = []

    def __init__(self, init_x: int, init_y: int, size: int, mass: int) -> None:
        super().__init__(size, arcade.color.ARMY_GREEN)
        self.center_x = init_x
        self.center_y = init_y
        self.mass = mass

        self.initial_x = init_x
        self.initial_y = init_y
        self.v_x = 0
        self.v_y = 0

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

    def move(self, solid_list=None) -> None:
        # Pour l'instant, on ignore les forces
        F = 0.0, 0.0
        self.v_x += dt*F[0]/mass
        self.v_y += dt*(-mass*g + F[1])/mass

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
