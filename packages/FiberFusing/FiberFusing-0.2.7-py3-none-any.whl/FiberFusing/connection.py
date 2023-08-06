#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import numpy
import logging
from scipy.optimize import minimize_scalar
from itertools import combinations

# Local imports
from FiberFusing.buffer import Circle, Point, Polygon, LineString
from FiberFusing import utils
from MPSPlots.Render2D import Scene2D, Axis


class ConnectionOptimization():
    def iterate_over_connected_fibers(self) -> tuple:
        """
        Just like the name implies, generator that iterate 
        over all the connected fibers.
        
        :returns:   pair of two connected fibers
        :rtype:     tuple
        """
        for fiber0, fiber1 in combinations(self.fiber_list, 2):
            if fiber0.intersection(fiber1).is_empty:
                continue
            else:
                yield fiber0, fiber1

    def shift_connections(self, virtual_shift: float) -> None:
        """
        Set the virtual shift of the virtual circles for each of the 
        connections.
        
        :param      virtual_shift:  The shift of virtual circles
        :type       virtual_shift:  float
        """
        self.virtual_shift = virtual_shift

        for connection in self.connected_fibers:
            connection.shift = virtual_shift
            connection.topology = self.topology

        self._initialize_()

    def compute_added_section(self) -> None:
        added_section = []
        for n, connection in enumerate(self.connected_fibers):
            Newadded_section = connection.added_section

            added_section.append(Newadded_section)

        self._added_section = utils.Union(*added_section) - utils.Union(*self.fiber_list)
        self._added_section.remove_non_polygon()
        self._added_section.Area = self._added_section.area
        total_added_area = self._added_section.area

        return total_added_area

    def compute_removed_section(self) -> None:
        removed_section = []
        for connection in self.connected_fibers:
            removed_section.append(connection.removed_section)

        self._removed_section = utils.Union(*removed_section)
        self._removed_section = self._removed_section
        self._removed_section.facecolor = 'red'
        total_removed_area = len(self.fiber_list) * self.fiber_list[0].area - utils.Union(*self.fiber_list).area
        return total_removed_area

    def initialize_connections_cores(self) -> None:
        """
        Setup the core position for each connections.
        Initial values of the core is the center.
        """
        for connection in self.connected_fibers:
            connection[0].core = connection[0].center
            connection[1].core = connection[1].center

    def initialize_connections(self) -> None:
        """
        Generate the connections (every pair of connnected fibers).
        """
        self.connected_fibers = []

        for fibers in self.iterate_over_connected_fibers():
            connection = Connection(*fibers)
            self.connected_fibers.append(connection)

        self.initialize_connections_cores()

    def get_cost_value(self, virtual_shift: float) -> float:
        """
        Gets the cost value which is the difference between removed section
        and added section for a given virtual circle shift.
        
        :param      virtual_shift:  The shift of the virtual circles
        :type       virtual_shift:  float
        
        :returns:   The cost value.
        :rtype:     float
        """
        
        self.shift_connections(virtual_shift=virtual_shift)

        added_section = self.compute_added_section()
        removed_section = self.compute_removed_section()

        cost = abs(added_section - removed_section)

        logging.debug(f' Fusing optimization: {virtual_shift = :.2e} \t -> \t{added_section = :.2e} \t -> {removed_section = :.2e} \t -> {cost = :.2e}')

        return cost

    def optimize_virtual_shift(self, bounds: tuple) -> float:
        """
        Compute the optimized geometry such that mass is conserved. 
        Does not compute the core movment.
        
        :param      bounds:  The virtual shift boundaries
        :type       bounds:  tuple
        
        :returns:   The optimal virtual shift.
        :rtype:     float
        """
        self.initialize_connections()

        core_distance = self.connected_fibers[0].distance_between_cores
        bounds = (0, core_distance * 1e3) if bounds is None else bounds

        res = minimize_scalar(
            self.get_cost_value, 
            bounds=bounds, 
            method='bounded', 
            options={'xatol': core_distance * self.tolerance_factor}
        )

        return res.x

    def compute_optimize_geometry(self, bounds: tuple = None) -> "buffer.Polygon":
        """
        Compute the optimized geometry such that mass is conserved and return the optimal geometry. 
        Does not compute the core movment.
        
        :param      bounds:  The virtual shift boundaries
        :type       bounds:  tuple
        
        :returns:   The optimize geometry.
        :rtype:     buffer.Polygon
        """

        optimal_virtual_shift = self.optimize_virtual_shift(bounds=bounds)

        optimal_geometry = self.get_shifted_geometry(virtual_shift=optimal_virtual_shift)

        self.clad_structure = optimal_geometry


class Connection():
    def __init__(self, fiber0, fiber1, topology: str = None, shift: float = None):
        self._topology = topology
        self.fiber_list = [fiber0, fiber1]
        self._shift = shift
        self._center_line = None
        self._extended_center_line = None
        self._initialize_()

    def _initialize_(self):
        self._virtual_circles = None
        self._added_section = None
        self._removed = None
        self._mask = None

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, value):
        self._shift = value
        self._initialize_()

    @property
    def topology(self):
        return self._topology

    @topology.setter
    def topology(self, Value):
        self._topology = Value

    def __getitem__(self, idx):
        return self.fiber_list[idx]

    def __setitem__(self, idx, Item):
        self.fiber_list[idx] = Item

    @property
    def virtual_circles(self,):
        if self._virtual_circles is None:
            self.compute_virtual_circles()
        return self._virtual_circles

    @property
    def distance_between_cores(self):
        return self[0].center.distance(self[1].center)

    @property
    def mask(self,):
        if self._mask is None:
            self.compute_mask()
        return self._mask

    @property
    def added_section(self):
        if self._added_section is None:
            self.compute_added_section()
        return self._added_section

    @property
    def removed_section(self):
        if self._removed is None:
            self.compute_removed_section()
        return self._removed

    @property
    def limit_added_area(self):
        return self[0].union(self[1]).convex_hull - self[0] - self[1]

    def compute_removed_section(self) -> None:
        self._removed = utils.Intersection(*self)
        self._removed.Area = self[1].area + self[0].area - utils.Union(*self).area

    def compute_topology(self) -> None:
        if self.removed_section.Area > self.limit_added_area.area:
            self._topology = 'convex'  
        else: 
            self._topology = 'concave'

    def get_conscripted_circles(self, type='exterior') -> Circle:
        """
        Return the connection two circonscript circles, which can be either of type exterior
        or interior.
        
        :param      type:  The type of circonscript circle to compute
        :type       type:  str
        
        :returns:   The conscripted circles.
        :rtype:     Circle
        """
        perpendicular_vector = self.extended_center_line.copy().get_perpendicular().get_vector()

        point = self.center_line.mid_point.translate(perpendicular_vector * self._shift)

        if type.lower() in ['exterior', 'concave']:
            radius = numpy.sqrt(self._shift**2 + (self.center_line.length / 2)**2) - self[0].radius

        if type.lower() in ['interior', 'convex']:
            radius = numpy.sqrt(self._shift**2 + (self.center_line.length / 2)**2) + self[0].radius

        return Circle(position=point, radius=radius, alpha=0.3, facecolor='black', name='virtual')

    def compute_virtual_circles(self) -> None:
        Circonscript0 = self.get_conscripted_circles(type=self.topology)

        Circonscript1 = Circonscript0.rotate(angle=180, origin=self.center_line.mid_point, in_place=False)

        self._virtual_circles = Circonscript0, Circonscript1

    def get_connected_point(self) -> list:
        """
        Return list of contact point from the connected fibers and
        virtual circles.
        """
        P0 = utils.NearestPoints(self.virtual_circles[0], self[0])
        P1 = utils.NearestPoints(self.virtual_circles[1], self[0])
        P2 = utils.NearestPoints(self.virtual_circles[0], self[1])
        P3 = utils.NearestPoints(self.virtual_circles[1], self[1])

        return [Point(position=(p.x, p.y)) for p in [P0, P1, P2, P3]]

    def compute_mask(self) -> None:
        """
        Compute the mask that is connecting the center to the contact point
        with the virtual circles.
        """
        P0, P1, P2, P3 = self.get_connected_point()

        if self.topology.lower() == 'concave':

            mask = Polygon(coordinates=[P0._shapely_object, P1._shapely_object, P3._shapely_object, P2._shapely_object])

            self._mask = (mask - self.virtual_circles[0] - self.virtual_circles[1])

        elif self.topology.lower() == 'convex':
            mid_point = LineString(coordinates=[self[0].center, self[1].center]).mid_point

            mask0 = Polygon(coordinates=[mid_point._shapely_object, P0._shapely_object, P2._shapely_object])
            mask0.scale(factor=1000, origin=mid_point._shapely_object, in_place=True)

            mask1 = Polygon(coordinates=[mid_point._shapely_object, P1._shapely_object, P3._shapely_object])
            mask1.scale(factor=1000, origin=mid_point._shapely_object, in_place=True)

            self._mask = (utils.Union(mask0, mask1) & utils.Union(*self.virtual_circles))

    def compute_added_section(self) -> None:
        if self.topology == 'convex':
            interesction = self.virtual_circles[0].intersection(self.virtual_circles[1], in_place=False)
            self._added_section = (self.mask - self[0] - self[1]) & interesction

        elif self.topology == 'concave':
            union = self.virtual_circles[0].union(self.virtual_circles[1], in_place=False)
            self._added_section = self.mask - self[0] - self[1] - union

        self._added_section.Area = self._added_section.area

    def _render_(self,
                 ax,
                 show_fiber: bool = True,
                 show_mask: bool = False,
                 show_virtual: bool = False,
                 show_added: bool = False,
                 show_removed: bool = False) -> None:

        if show_fiber:
            for fiber in self:
                fiber._render_(ax)

        if show_mask:
            self.mask._render_(ax)

        if show_virtual:
            self.virtual_circles[0]._render_(ax)
            self.virtual_circles[1]._render_(ax)

        if show_added:
            self.added_section._render_(ax)

        if show_removed:
            self.removed_section._render_(ax)

    @property
    def center_line(self) -> LineString:
        if self._center_line is None:
            self.compute_center_line()
        return self._center_line

    def compute_center_line(self) -> None:
        self._center_line = LineString(coordinates=[self[0].center, self[1].center])

    @property
    def extended_center_line(self) -> LineString:
        if self._extended_center_line is None:
            self.compute_extended_center_line()
        return self._extended_center_line

    def compute_extended_center_line(self) -> None:
        line = self.center_line.copy()

        line.make_length(line.length + self[0].radius + self[1].radius)

        self._extended_center_line = line

    @property
    def total_area(self) -> Polygon:
        output = utils.Union(*self, self.added_section)
        output.remove_non_polygon()

        return output

    def split_geometry(self, geometry, position) -> Polygon:
        """
        Split the connection at a certain position x which is the parametrised
        point covering the full connection.
        
        :param      geometry:  The geometry
        :type       geometry:  Polygon
        :param      position:  The parametrized position
        :type       position:  float
        
        :returns:   The splitted geometry
        :rtype:     Polygon
        """
        line = self.extended_center_line.copy()

        line.centering(center=position).rotate(
            angle=90, 
            in_place=True, 
            origin=line.mid_point
        )

        line.extend(factor=2)

        external_part = utils.Union(geometry).remove_non_polygon()

        return external_part.split_with_line(line=line, return_type='largest')

    def compute_area_mismatch_cost(self, x: float = 0.5) -> float:
        position0 = self.extended_center_line.get_position_parametrisation(1 - x)
        position1 = self.extended_center_line.get_position_parametrisation(x)
        
        large_section = self.split_geometry(
            geometry=self.total_area, 
            position=position0
        )

        small_area = abs(large_section.area - self.total_area.area)

        Cost = abs(small_area - self[0].area / 2.)

        position0.name = 'position0'
        position1.name = 'position1'
        position0.color = 'b'
        position1.color = 'b'
        center0 = self[0].center
        center0.name = 'center0'
        center1 = self[1].center
        center1.name = 'center1'

        self.core_shift = (position0 - self[0].center), (position1 - self[1].center)
        self.core_shift[0].name = 'shift0'
        self.core_shift[1].name = 'shift1'

        logging.debug(f'Core positioning optimization: {x = :+.2f} \t -> \t{Cost = :<10.2f} -> \t\t{self.core_shift = }')

        return Cost

    def optimize_core_position(self) -> None:
        minimize_scalar(
            self.compute_area_mismatch_cost,
            bounds=(0.50001, 0.99),
            method='bounded',
            options={'xatol': 1e-10}
            # options={'xatol': self.center_line.length / 1e4}
        )

        self[0].core = self[0].core + self.core_shift[0]

        self[1].core = self[1].core + self.core_shift[1]

    def plot(self) -> Scene2D:
        figure = Scene2D(unit_size=(6, 6))

        ax = Axis(row=0,
                  col=0,
                  x_label=r'x distance',
                  y_label=r'y distance',
                  legend=False,
                  show_grid=True,
                  equal=True,)

        figure.add_axes(ax)
        figure._generate_axis_()

        self[0]._render_(ax)
        self[1]._render_(ax)

        self.added_section._render_(ax)

        return figure


# -
