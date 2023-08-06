import numpy
import matplotlib.pyplot as plt


class Axes(object):
    def __init__(self, nx: int, ny: int, x_bounds: list, y_bounds: list):
        self._nx = nx
        self._ny = ny

        self._x_bounds = x_bounds
        self._y_bounds = y_bounds

        self.compute_mesh()

    def centering(self, factor: float = 1.2, zero_included=True):
        min_bound = min(self.x_bounds[0], self.y_bounds[0]) * factor
        max_bound = min(self.x_bounds[1], self.y_bounds[1]) * factor

        self._x_bounds = self._y_bounds = (min_bound, max_bound)

        if zero_included:
            self.make_nx_odd()
            self.make_ny_odd()

        self.compute_mesh()

    def x_centering(self, zero_included=True):
        abs_boundary = abs(self.x_bounds[0]), abs(self.x_bounds[1])
        abs_boundary = max(abs_boundary)

        self._x_bounds = (-abs_boundary, +abs_boundary)

        if zero_included:
            self.make_nx_odd()

        self.compute_mesh()

    def y_centering(self, zero_included=True):
        abs_boundary = abs(self.y_bounds[0]), abs(self.y_bounds[1])
        abs_boundary = max(abs_boundary)

        self._y_bounds = (-abs_boundary, +abs_boundary)

        if zero_included:
            self.make_ny_odd()

        self.compute_mesh()

    def compute_mesh(self):
        self.x_mesh, self.y_mesh = numpy.meshgrid(self.x_vector, self.y_vector)

    def make_nx_odd(self):
        self.nx = self.to_odd(self.nx)

    def make_ny_odd(self):
        self.ny = self.to_odd(self.ny)

    def make_nx_even(self):
        self.nx = self.to_even(self.nx)

    def make_ny_even(self):
        self.ny = self.to_even(self.ny)

    @property
    def shape(self):
        return numpy.array([self.nx, self.ny])

    @property
    def dA(self):
        return self.dx * self.dy

    @property
    def rho_mesh(self):
        return numpy.sqrt(self.x.mesh**2 + self.y.mesh**2)

    def set_left(self):
        self._nx = self._nx // 2 + 1
        self.x_bounds = (self.x_bounds[0], 0)

    def set_right(self):
        self._nx = self._nx // 2 + 1
        self.x_bounds = (0, self.x_bounds[1])

    def set_top(self):
        self._ny = self._ny // 2 + 1
        self.y_bounds = (0, self.x_bounds[1])

    def set_bottom(self):
        self._ny = self._ny // 2 + 1
        self.y_bounds = (self.x_bounds[0], 0)

    # nx property------------
    @property
    def nx(self):
        return self._nx

    @nx.setter
    def nx(self, value):
        self._nx = value
        self.compute_mesh()

    # ny property------------
    @property
    def ny(self):
        return self._ny

    @ny.setter
    def ny(self, value):
        self._ny = value
        self.compute_mesh()

    # dx property------------
    @property
    def dx(self):
        return numpy.abs(self.x_bounds[0] - self.x_bounds[1]) / (self.nx - 1)

    # dy property------------
    @property
    def dy(self):
        return numpy.abs(self.y_bounds[0] - self.y_bounds[1]) / (self.ny - 1)

    @property
    def x_vector(self):
        return numpy.linspace(*self.x_bounds, self.nx, endpoint=True)

    @property
    def y_vector(self):
        return numpy.linspace(*self.y_bounds, self.ny, endpoint=True)

    # x_bound property------------
    @property
    def x_bounds(self):
        return self._x_bounds

    @x_bounds.setter
    def x_bounds(self, value):
        self._x_bounds = value

        self.compute_mesh()

    # y_bound property------------
    @property
    def y_bounds(self):
        return self._y_bounds

    @y_bounds.setter
    def y_bounds(self, value):
        self._y_bounds = value

        self.compute_mesh()

    def to_odd(self, value: int):
        return (value // 2) * 2 + 1

    def to_even(self, value: int):
        return (value // 2) * 2

    def plot(self):
        figure, ax = plt.subplots(1, 1)
        ax.grid('on')
        ax.set_xticks(self.x_vector)
        ax.set_yticks(self.y_vector)
        ax.set_xlim(self.x_bounds)
        ax.set_ylim(self.y_bounds)
        ax.set_title('Mesh grid')
        ax.set_xlabel('x-direction')
        ax.set_ylabel('y-direction')
        ax.set_aspect('equal')
        plt.show()

# -
