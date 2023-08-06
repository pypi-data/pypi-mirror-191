#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import logging
from dataclasses import dataclass

# Third-party imports
import numpy

# Local imports
from MPSPlots.Render2D import Scene2D, Axis
from FiberFusing import utils
from FiberFusing.connection import ConnectionOptimization
from FiberFusing import buffer
from FiberFusing.buffer import Circle
from FiberFusing.rings import FiberRing

logging.basicConfig(level=logging.INFO)


@dataclass
class BaseFused(ConnectionOptimization):
    index: float
    """ Refractive index of the cladding structure. """
    tolerance_factor: float = 1e-2
    """ Tolerance on the optimization problem which aim to minimize the difference between added and removed area of the heuristic algorithm. """
    core_position_scrambling: float = 0
    """ Not implemented yet. """

    def __post_init__(self):
        self._initialize_()
        self._fiber_list = None
        self.core_list = []

    def _initialize_(self):
        self._fiber_rings = []
        self.custom_fiber = []
        self._hole = None
        self._topology = None
        self._added_section = None
        self._removed_section = None
        self._fiber_centers = None
        self._core_shift = None

    @property
    def _shapely_object(self):
        return self.clad_structure

    @property
    def bounds(self):
        return self.clad_structure.bounds

    @property
    def fiber(self) -> list:
        return self.fiber_list

    @property
    def added_section(self) -> buffer.Polygon:
        if self._added_section is None:
            self.compute_added_section()
        return self._added_section

    @property
    def removed_section(self) -> buffer.Polygon:
        if self._removed_section is None:
            self.compute_removed_section()
        return self._removed_section

    @property
    def topology(self) -> str:
        if self._topology is None:
            self.compute_topology()
        return self._topology

    def compute_topology(self) -> None:
        Limit = []
        for connection in self.connected_fibers:
            Limit.append(connection.limit_added_area)

        OverallLimit = utils.Union(*Limit) - utils.Union(*self.fiber_list)
        self.compute_removed_section()

        total_removed_area = self.compute_removed_section()
        self._topology = 'convex' if total_removed_area > OverallLimit.area else 'concave'

    def get_max_distance(self) -> float:
        return numpy.max([f.get_max_distance() for f in self.fiber_list])

    @property
    def fiber_list(self) -> list:
        if self._fiber_list is None:
            self.compute_fiber_list()
        return self._fiber_list

    def add_fiber_ring(self, number_of_fibers: int, fusion_degree: float, fiber_radius: float) -> None:
        ring = FiberRing(
            number_of_fibers=number_of_fibers,
            fiber_radius=fiber_radius
        )

        ring.set_fusion_degree(fusion_degree=fusion_degree)

        self._fiber_rings.append(ring)

    def add_center_fiber(self, fiber_radius: float):
        fiber = Circle(
            radius=fiber_radius, 
            position=(0, 0), 
            name=f' Fiber {0}'
        )

        self.custom_fiber.append(fiber)

    def add_custom_fiber(self, *fibers) -> None:
        for fiber in fibers:
            self.custom_fiber.append(fiber)

    def compute_core_position(self) -> None:
        """
        Optimize one round for the core positions of each connections.
        """
        for connection in self.connected_fibers:
            connection.optimize_core_position()

    def compute_fiber_list(self) -> None:
        """
        Generate the fiber list.
        """
        self._fiber_list = []

        for Ring in self._fiber_rings:
            for fiber in Ring.fiber_list:
                self._fiber_list.append(fiber)

        for fiber in self.custom_fiber:
            self._fiber_list.append(fiber)

        for n, fiber in enumerate(self._fiber_list):
            fiber.name = f' fiber {n}'

    def get_shifted_geometry(self, virtual_shift: float) -> buffer.Polygon:
        """
        Returns the clad geometry for a certain shift value.

        :param      virtual_shift:  The shift value
        :type       virtual_shift:  { type_description }

        :returns:   The optimized geometry.
        :rtype:     { return_type_description }
        """
        opt_geometry = utils.Union(*self.fiber_list, self.added_section)

        self.compute_core_position()
        self.randomize_core_position()

        return opt_geometry

    def randomize_core_position(self) -> None:
        """
        Shuffle the position of the fiber cores.
        It can be used to add realism to the fusion process.
        """
        if self.core_position_scrambling != 0:
            for fiber in self._fiber_list:
                random_xy = numpy.random.rand(2) * self.core_position_scrambling
                fiber.core.translate(random_xy, in_place=True)

    def get_rasterized_mesh(self, coordinate: numpy.ndarray, n_x: int, n_y: int) -> numpy.ndarray:
        Exterior = self.clad_structure.__raster__(coordinate).reshape([n_y, n_x])

        self.Raster = Exterior

        return self.Raster

    def rotate(self, *args, **kwargs):
        """
        Rotates the full structure, including the fiber cores.
        """
        for fiber in self.fiber_list:
            fiber.rotate(*args, **kwargs, in_place=True)
            fiber.core.rotate(*args, **kwargs, in_place=True)
            
        self.clad_structure = self.clad_structure.rotate(*args, **kwargs)

    def scale_down_position(self, factor: float):
        """
        Scale down the distance between each cores.
        
        :param      factor:  The scaling factor
        :type       factor:  float
        """
        for fiber in self.fiber_list:
            fiber.scale_position(factor=factor)

    def plot(self,
             show_fibers: bool = True,
             show_added: bool = False,
             show_removed: bool = False) -> Scene2D:

        figure = Scene2D(unit_size=(6, 6))

        ax = Axis(
            row=0,
            col=0,
            x_label=r'x',
            y_label=r'y',
            show_grid=True,
            equal_limits=True,
            equal=True
        )

        figure.add_axes(ax)._generate_axis_()

        self.clad_structure._render_(ax)

        for fiber in self.fiber_list:
            fiber._render_(ax)

        return figure


#  -
