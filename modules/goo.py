import arcade

dt=0.1
g = 0.5
mass=0.4
class Goo(arcade.SpriteCircle):
    # store all goos created in a list called goos 
    goos: list["Goo"] = []

    def __init__(self, init_x: int, init_y: int, size: int, mass: int) -> None:
        super().__init__(size, arcade.color.BLUE)
        self.center_x = init_x
        self.center_y = init_y
        self.mass = mass
        self.v_x = 0
        self.v_y = 0

        Goo.goos.append(self)

    def move(self) -> None:
        F = self.F()  
        self.equa_diff(F)

    def compute_deltas(self):
        other_goos = [goo for goo in Goo.goos if goo != self]

        pass

    def F(self):
        pass

    def equa_diff(self,F):
        self.v_x += dt*F[0]/mass
        self.v_y += dt*(-mass*g + F[1])/mass
        self.center_x += self.v_x*dt
        self.center_y += self.v_y*dt 
        pass
