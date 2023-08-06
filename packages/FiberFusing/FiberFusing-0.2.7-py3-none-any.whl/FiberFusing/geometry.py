# Third-party imports
import numpy
from dataclasses import dataclass
from scipy.ndimage import gaussian_filter

# MPSPlots imports
import MPSPlots.CMAP
from MPSPlots.Render2D import Scene2D, ColorBar, Axis, Mesh, Polygon

# FiberFusing imports
from FiberFusing import utils
from FiberFusing.axes import Axes
from FiberFusing.buffer import BackGround


@dataclass
class Geometry(object):
    """
    Class represent the refractive index (RI) geometrique profile which
    can be used to retrieve the supermodes.
    """
    background: object
    """ Geometrique object representing the background (usually air). """
    structures: list
    """ List of geometrique object representing the fiber structure. """
    x_bounds: list = 'auto-centering'
    """ X boundary to render the structure, argument can be either list or a string from ['auto', 'left', 'right', 'centering']. """
    y_bounds: list = 'auto-centering'
    """ Y boundary to render the structure, argument can be either list or a string from ['auto', 'top', 'bottom', 'centering']. """
    n: int = 100
    """ Number of point (x and y-direction) to evaluate the rendering """
    index_scrambling: float = 0
    """ Index scrambling for degeneracy lifting """
    gaussian_filter: int = None
    """ Standard deviation of the gaussian blurring for the mesh and gradient """
    boundary_pad_factor: int = 1.3
    """ The factor that multiply the boundary value in order to keep padding between mesh and boundary """

    def __post_init__(self):
        self.object_list = [self.background, *self.structures]
        self._mesh = None
        self._gradient = None

        min_x, min_y, max_x, max_y = self.get_boundaries()

        self.axes = Axes(
            x_bounds=(min_x, max_x),
            y_bounds=(min_y, max_y),
            nx=self.n,
            ny=self.n
        )
        self.axes.centering(factor=self.boundary_pad_factor)

        self.interpret_boundaries()

        self.index_list = self.get_index_range()

    def interpret_boundaries(self):
        self.interpret_y_boundary()

        self.interpret_x_boundary()

    def interpret_y_boundary(self) -> None:
        """
        Interpret the y_bound parameter.
        If the parameter is in ["top", "bottom", "centering"], it returns
        an auto-evaluated boundary

        :param      y_bound:  The y boundary to be interpreted
        :type       y_bound:  list

        :returns:   The interpreted y boundary
        :rtype:     list
        """
        if isinstance(self.y_bounds, (list, tuple)):
            self.axes.y_bounds = self.y_bounds

        elif isinstance(self.y_bounds, str):
            arguments = self.y_bounds.split('-')
            if 'centering' in arguments:
                self.axes.y_centering()
            if 'top' in arguments:
                self.axes.set_top()
            if 'bottom' in arguments:
                self.axes.set_bottom()

    def get_boundaries(self):
        min_x, min_y, max_x, max_y = [], [], [], []
        for obj in self.structures:
            bounds = obj.bounds
            min_x.append(bounds[0])
            min_y.append(bounds[1])
            max_x.append(bounds[2])
            max_y.append(bounds[3])

        return (numpy.min(min_x),
                numpy.min(min_y),
                numpy.max(max_x),
                numpy.max(max_y))

    def interpret_x_boundary(self) -> None:
        """
        Interpret the x_bound parameter.
        If the parameter is in ["left", "right", "centering"], it returns
        an auto-evaluated boundary

        :param      x_bound:  The y boundary to be interpreted
        :type       x_bound:  list

        :returns:   The interpreted y boundary
        :rtype:     list
        """
        if isinstance(self.x_bounds, (list, tuple)):
            self.axes.x_bounds = self.x_bounds

        elif isinstance(self.x_bounds, str):
            arguments = self.x_bounds.split('-')

            if 'centering' in arguments:
                self.axes.x_centering()
            if 'right' in arguments:
                self.axes.set_right()
            if 'left' in arguments:
                self.axes.set_left()

    def get_gradient_mesh(self, mesh: numpy.ndarray, Axes: Axes) -> numpy.ndarray:
        """
        Returns the gradient to the 4th degree of the provided mesh.

        :param      mesh:  The mesh to which compute the gradient
        :type       mesh:  numpy.ndarray
        :param      Axes:  The axis associated to the mesh.
        :type       Axes:  Axes

        :returns:   The gradient of the mesh.
        :rtype:     numpy.ndarray
        """
        Ygrad, Xgrad = utils.gradientO4(mesh, Axes.dx, Axes.dy)

        gradient = (Xgrad * Axes.x_mesh + Ygrad * Axes.y_mesh)

        return gradient

    @property
    def mesh(self) -> numpy.ndarray:
        if self._mesh is None:
            self._mesh, self._gradient = self.generate_mesh()
        return self._mesh

    @property
    def gradient(self) -> numpy.ndarray:
        if self._gradient is None:
            self._mesh, self._gradient = self.generate_mesh()
        return self._gradient

    @property
    def max_index(self) -> float:
        return max([obj.index for obj in self.object_list])[0]

    @property
    def min_index(self) -> float:
        return min([obj.index for obj in self.object_list])[0]

    def get_index_range(self) -> list:
        """
        Returns the list of all index associated to the element of the geometry.
        """
        return [float(obj.index) for obj in self.object_list]

    def rotate(self, angle: float) -> None:
        """
        Rotate the full geometry

        :param      angle:  Angle to rotate the geometry, in degrees.
        :type       angle:  float
        """
        for obj in self.structures:
            obj = obj.rotate(angle=angle)

    def rasterize_polygons(self, coordinates: numpy.ndarray, n_x: int, n_y: int) -> numpy.ndarray:
        """
        Returns the rasterize mesh of the object.

        :param      coordinates:  The coordinates to which evaluate the mesh.
        :type       coordinates:  { type_description }
        :param      n_x:          The number of point in the x direction
        :type       n_x:          int
        :param      n_y:          The number of point in the y direction
        :type       n_y:          int

        :returns:   The rasterized mesh
        :rtype:     numpy.ndarray
        """
        mesh = numpy.zeros([n_y, n_x])

        for polygone in self.object_list:
            raster = polygone.get_rasterized_mesh(coordinate=coordinates, n_x=n_x, n_y=n_y).astype(numpy.float64)

            rand = (numpy.random.rand(1) - 0.5) * self.index_scrambling

            raster *= polygone.index + rand

            mesh[numpy.where(raster != 0)] = 0

            mesh += raster

        return mesh

    def generate_mesh(self) -> numpy.ndarray:
        self.coords = numpy.vstack((self.axes.x_mesh.flatten(), self.axes.y_mesh.flatten())).T

        mesh = self.rasterize_polygons(
            coordinates=self.coords,
            n_x=self.axes.nx,
            n_y=self.axes.ny
        )

        if self.gaussian_filter is not None:
            mesh = gaussian_filter(input=mesh, sigma=self.gaussian_filter)

        gradient = self.get_gradient_mesh(mesh=mesh**2, Axes=self.axes)

        return mesh, gradient

    def _render_patch_on_ax_(self, ax: Axis) -> None:
        """
        Add the patch representation of the geometry into the give ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        colorbar = ColorBar(log_norm=True,
                            position='right',
                            numeric_format='%.1e',
                            symmetric=True)

        for polygon in self.object_list:
            if isinstance(polygon, BackGround):
                continue

            artist = Polygon(x=self.axes.x_vector,
                             y=self.axes.y_vector,
                             instance=polygon._shapely_object)

            ax.add_artist(artist)

        ax.colorbar = colorbar
        ax.x_label = r'x-distance'
        ax.y_label = r'y-distance'
        ax.title = 'Coupler index structure'

    def _render_gradient_on_ax_(self, ax: Axis) -> None:
        """
        Add the rasterized representation of the gradient of the geometrys into the give ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        colorbar = ColorBar(log_norm=True,
                            position='right',
                            numeric_format='%.1e',
                            symmetric=True)

        artist = Mesh(x=self.axes.x_vector,
                      y=self.axes.y_vector,
                      scalar=self.gradient,
                      colormap=MPSPlots.CMAP.BWR)

        ax.colorbar = colorbar
        ax.x_label = r'x-distance'
        ax.y_label = r'y-distance'
        ax.title = 'Refractive index gradient'
        ax.add_artist(artist)

    def _render_mesh_on_ax_(self, ax: Axis) -> None:
        """
        Add the rasterized representation of the geometry into the give ax.

        :param      ax:   The ax to which append the representation.
        :type       ax:   Axis
        """
        colorbar = ColorBar(discreet=False,
                            position='right',
                            numeric_format='%.4f')

        artist = Mesh(x=self.axes.x_vector,
                      y=self.axes.y_vector,
                      scalar=self.mesh,
                      colormap='Blues')

        ax.colorbar = colorbar
        ax.x_label = r'x-distance'
        ax.y_label = r'y-distance'
        ax.title = 'Rasterized mesh'
        ax.add_artist(artist)

    def plot(self) -> None:
        """
        Plot the different representations [patch, raster-mesh, raster-gradient]
        of the geometry.
        """
        figure = Scene2D(unit_size=(4, 4), tight_layout=True)

        ax0 = Axis(row=0, col=0, equal_limits=True)

        ax1 = Axis(row=0, col=1, equal_limits=True)

        ax2 = Axis(row=0, col=2, equal_limits=True)

        self._render_patch_on_ax_(ax0)
        self._render_mesh_on_ax_(ax1)
        self._render_gradient_on_ax_(ax2)

        figure.add_axes(ax0, ax1, ax2)

        return figure

# -
