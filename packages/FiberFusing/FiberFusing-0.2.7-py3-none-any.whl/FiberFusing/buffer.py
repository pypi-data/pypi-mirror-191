#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import numpy
import copy
from collections.abc import Iterable
from dataclasses import dataclass


# matplotlib imports
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection
from matplotlib.path import Path


# shapely imports
from shapely.ops import split
import shapely.geometry as geo
from shapely import affinity

# other imports
from FiberFusing import utils
from MPSPlots.Render2D import Scene2D, Axis


class Alteration():
    has_z = False

    def in_place_copy(function, *args, **kwargs):
        def wrapper(self, *args, in_place=False, **kwargs):
            if in_place:
                output = self
            else:
                output = self.copy()
                for attr in self.inherit_attr:
                    setattr(output, attr, getattr(self, attr))
            return function(self, output, *args, **kwargs)

        return wrapper

    def copy(self):
        return copy.deepcopy(self)

    def __repr__(self):
        return self._shapely_object.__repr__()

    @property
    def is_empty(self):
        return self._shapely_object.is_empty

    @in_place_copy
    def union(self, output, *others):
        others = tuple(o._shapely_object for o in others)
        output._shapely_object = self._shapely_object.union(*others)
        return output

    @in_place_copy
    def intersection(self, output, *others):
        others = tuple(o._shapely_object for o in others)
        output._shapely_object = self._shapely_object.intersection(*others)
        return output

    @in_place_copy
    def scale(self, output, factor: float, origin: tuple = (0, 0)) -> None:
        origin = utils.interpret_to_point(origin)
        output._shapely_object = affinity.scale(self._shapely_object, xfact=factor, yfact=factor, origin=origin._shapely_object)
        return output

    @in_place_copy
    def translate(self, output, shift: tuple) -> None:
        shift = utils.interpret_to_point(shift)
        output._shapely_object = affinity.translate(self._shapely_object, shift.x, shift.y)
        return output

    @in_place_copy
    def rotate(self, output, angle, origin: tuple = (0, 0)) -> None:
        origin = utils.interpret_to_point(origin)
        output._shapely_object = affinity.rotate(self._shapely_object, angle=angle, origin=origin._shapely_object)
        return output


class BaseArea(Alteration):
    @property
    def exterior(self):
        return self._shapely_object.exterior

    def get_rasterized_mesh(self, coordinate: numpy.ndarray, n_x: int, n_y: int) -> numpy.ndarray:
        return self.__raster__(coordinate).reshape([n_y, n_x])

    @property
    def is_empty(self):
        return self._shapely_object.is_empty

    @property
    def convex_hull(self):
        return Polygon(instance=self._shapely_object.convex_hull)

    @property
    def area(self):
        return self._shapely_object.area

    @property
    def bounds(self):
        return self._shapely_object.bounds

    @property
    def center(self):
        return Point(position=(self._shapely_object.centroid.x, self._shapely_object.centroid.y), name='center')

    def __add__(self, other):
        output = self.copy()
        output._shapely_object = self._shapely_object.__add__(other._shapely_object)
        return output

    def __sub__(self, other):
        output = self.copy()
        output._shapely_object = self._shapely_object.__sub__(other._shapely_object)
        return output

    def __and__(self, other):
        output = self.copy()
        output._shapely_object = self._shapely_object.__and__(other._shapely_object)
        return output

    def split_with_line(self, line, return_type: str = 'largest') -> 'Polygon':
        self.remove_insignificant_section()

        assert self.is_pure_polygon, f"Error: non-pure polygone is catch before spliting: {self._shapely_object.__class__}."

        split_geometry = split(self._shapely_object, line.copy().extend(factor=100)._shapely_object).geoms

        areas = [poly.area for poly in split_geometry]

        sorted_area = numpy.argsort(areas)

        match return_type:
            case 'largest':
                idx = sorted_area[-1]
                return Polygon(instance=split_geometry[idx])
            case 'smallest':
                idx = sorted_area[0]
                return Polygon(instance=split_geometry[idx])


@dataclass
class Circle(BaseArea):
    position: list
    radius: float
    name: str = ''
    index: float = 1.0
    facecolor: str = 'lightblue'
    edgecolor: str = 'black'
    alpha: float = 0.4
    resolution: int = 128 * 2

    inherit_attr: list = ('name', 'facecolor', 'alpha', 'edgecolor', 'index')

    def __post_init__(self) -> None:
        self.position = utils.interpret_to_point(self.position)
        self._shapely_object = self.position._shapely_object.buffer(self.radius, resolution=self.resolution)
        self.position = None
        self.core = None

    def _render_(self, ax: Axis) -> None:
        path = Path.make_compound_path(
            Path(numpy.asarray(self.exterior.coords)[:, :2]),
            *[Path(numpy.asarray(ring.coords)[:, :2]) for ring in self._shapely_object.interiors])

        patch = PathPatch(path)
        collection = PatchCollection([patch], alpha=self.alpha, facecolor=self.facecolor, edgecolor=self.edgecolor)

        ax._ax.add_collection(collection, autolim=True)
        ax._ax.autoscale_view()
        if self.name:
            ax._ax.scatter(self.center.x, self.center.y, color='k', zorder=10)
            ax._ax.text(self.center.x, self.center.y, self.name)

    def plot(self) -> Scene2D:
        figure = Scene2D(unit_size=(6, 6))
        ax = Axis(row=0, col=0, x_label='x', y_label='y', colorbar=False, equal=True)
        figure.add_axes(ax)
        figure._generate_axis_()
        self._render_(ax)

        if self.core is not None:
            self.core._render_(ax)

        return figure

    def __raster__(self, coordinate: numpy.ndarray) -> numpy.ndarray:
        Exterior = Path(self.exterior.coords)

        Exterior = Exterior.contains_points(coordinate)

        return Exterior.astype(int)

    def contains_points(self, coordinate: numpy.ndarray) -> numpy.ndarray:
        exterior = Path(self.exterior.coords)
        return exterior.contains_points(coordinate).astype(bool)

    def scale_position(self, factor: float):
        new_position = affinity.scale(
            self.center._shapely_object, 
            xfact=factor, 
            yfact=factor, 
            origin=(0, 0)
        )

        shift = (new_position.x - self.center.x, new_position.y - self.center.y)

        return self.translate(shift=shift, in_place=True)


@dataclass
class Point(Alteration):
    position: list = (0, 0)
    name: str = 'Point'
    index: float = 1.0
    color: str = 'black'
    alpha: float = 1.0
    marker: str = "o"
    markersize: int = 60

    inherit_attr: list = ('name', 'color', 'marker', 'alpha', 'markersize', 'index')

    object_description = 'Point'

    def __post_init__(self) -> None:
        if isinstance(self.position, Point):
            self._shapely_object = self.position._shapely_object
        elif isinstance(self.position, geo.Point):
            self._shapely_object = self.position
        else:
            self._shapely_object = geo.Point(self.position)

    @property
    def x(self) -> float:
        return self._shapely_object.x

    @property
    def y(self) -> float:
        return self._shapely_object.y

    def __add__(self, other) -> 'Point':
        other = utils.interpret_to_point(other)

        return Point(position=(self.x + other.x, self.y + other.y))

    def __sub__(self, other) -> 'Point':
        other = utils.interpret_to_point(other)
        return Point(position=(self.x - other.x, self.y - other.y))

    def __neg__(self) -> 'Point':
        return Point(position=[-self.x, -self.y])

    def __mul__(self, factor: float) -> 'Point':
        return Point(position=[self.x * factor, self.y * factor])

    def distance(self, other):
        return numpy.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def _render_(self, ax: Axis) -> None:
        ax._ax.scatter(self.x, self.y, s=self.markersize, marker=self.marker, color=self.color, alpha=self.alpha)
        ax._ax.text(self.x * 1.01, self.y * 1.01, self.name)

    def plot(self) -> Scene2D:
        figure = Scene2D(unit_size=(6, 6))
        ax = Axis(row=0, col=0, x_label='x', y_label='y', colorbar=False, equal=True)
        figure.add_axes(ax)
        figure._generate_axis_()

        self._render_(ax)

        return figure


@dataclass
class LineString(Alteration):
    coordinates: list = ()
    name: str = ''
    index: float = 1.0
    color: str = 'black'
    alpha: float = 1.0
    marker: str = "o"
    markersize: int = 60

    inherit_attr: list = ('name', 'color', 'marker', 'alpha', 'markersize', 'index')

    object_description = 'LineString'

    def __post_init__(self) -> None:
        assert len(self.coordinates) == 2, 'LineString class is only intended for two coordinates.'
        self.coordinates = utils.interpret_to_point(*self.coordinates)

        shapely_coordinate = [c._shapely_object for c in self.coordinates]

        self._shapely_object = geo.LineString(shapely_coordinate)

        self.coordinates = None

    @property
    def boundary(self):
        return [Point(p) for p in self._shapely_object.boundary.geoms]

    @property
    def center(self):
        return self._shapely_object.centroid

    def intersect(self, other):
        self._shapely_object = self._shapely_object.intersection(other._shapely_object)

    @property
    def mid_point(self):
        P0, P1 = self.boundary
        return Point(position=[(P0.x + P1.x) / 2, (P0.y + P1.y) / 2])

    @property
    def length(self):
        P0, P1 = self.boundary
        return numpy.sqrt((P0.x - P1.x)**2 + (P0.y - P1.y)**2)

    def get_perpendicular(self):
        perpendicular = self.copy()
        perpendicular.rotate(angle=90, origin=perpendicular.mid_point, in_place=True)
        return perpendicular

    def get_position_parametrisation(self, x: float):
        P0, P1 = self.boundary
        return P0 - (P0 - P1) * x

    def _render_(self, ax: Axis) -> None:
        ax._ax.plot(*self._shapely_object.xy, color=self.color, alpha=self.alpha)

    def make_length(self, length: float):
        return self.extend(factor=length / self.length)

    def centering(self, center: Point):
        P0, P1 = self.boundary

        shift = (center.x - self.mid_point.x, center.y - self.mid_point.y)
        P2 = P0.translate(shift=shift)
        P3 = P1.translate(shift=shift)

        output = LineString(coordinates=[P2._shapely_object, P3._shapely_object])

        self._shapely_object = output._shapely_object

        return self

    def get_vector(self):
        P0, P1 = self.boundary

        dy = P0.y - P1.y
        dx = P0.x - P1.x
        if dx == 0:
            return numpy.asarray([0, 1])
        else:
            norm = numpy.sqrt(1 + (dy / dx)**2)
            return numpy.array([1, dy / dx]) / norm

    def extend(self, factor: float = 1):
        self._shapely_object = affinity.scale(self._shapely_object, xfact=factor, yfact=factor, origin=self.mid_point._shapely_object)
        return self

    def plot(self) -> Scene2D:
        figure = Scene2D(unit_size=(6, 6))
        ax = Axis(row=0, col=0, x_label='x', y_label='y', colorbar=False, equal=True)
        figure.add_axes(ax)
        figure._generate_axis_()

        self._render_(ax)

        return figure


class BackGround(Circle):
    def __init__(self, index, radius: float = 1000):
        self.position = (0, 0)
        self.radius = 1000
        self.index = index
        super().__post_init__()


@dataclass
class Polygon(BaseArea):
    coordinates: list = None
    instance: geo.Polygon = None
    name: str = ''
    index: float = 1.0
    facecolor: str = 'lightblue'
    edgecolor: str = 'black'
    alpha: float = 0.4

    inherit_attr: list = ('name', 'facecolor', 'alpha', 'edgecolor', 'index')

    def __post_init__(self) -> None:
        if self.instance is not None:
            self._shapely_object = self.instance
        else:
            self.coordinates = utils.interpret_to_point(*self.coordinates)
            self._shapely_object = geo.Polygon((c.x, c.y) for c in self.coordinates)

    @property
    def hole(self):
        assert self.is_pure_polygon, "Cannot compute hole for non-pure polygone"
        output = self.copy()
        if isinstance(output.interiors, Iterable):
            polygon = [geo.Polygon(c) for c in output.interiors]
            output = utils.Union(*polygon)
            output.remove_insignificant_section()
        else:
            output._shapely_object = geo.Polygon(*output.interiors)

        return output

    @property
    def interiors(self):
        return self._shapely_object.interiors

    def remove_non_polygon(self):
        if isinstance(self._shapely_object, geo.GeometryCollection):
            new_polygon_set = [p for p in self._shapely_object.geoms if isinstance(p, (geo.Polygon, geo.MultiPolygon))]
            self._shapely_object = geo.MultiPolygon(new_polygon_set)

        return self

    def remove_insignificant_section(self, ratio: float = 0.1, min_area: float = 1) -> None:
        if isinstance(self._shapely_object, geo.Polygon) and self._shapely_object.area == 0:
            self._shapely_object = geo.Polygon()

        if isinstance(self._shapely_object, geo.MultiPolygon):
            polygones = [p for p in self._shapely_object.geoms if p.area > min_area]
            if len(polygones) == 0:
                self._shapely_object = geo.Polygon()
            elif len(polygones) == 1:
                self._shapely_object = geo.Polygon(polygones[0])
            else:
                self._shapely_object = geo.MultiPolygon(polygones)

    def _render_(self, ax: Axis) -> None:
        if isinstance(self._shapely_object, geo.MultiPolygon):
            for polygon in self._shapely_object.geoms:
                self._render_polygon_on_ax_(ax=ax, polygon=polygon)

        else:
            self._render_polygon_on_ax_(ax=ax, polygon=self._shapely_object)

        if self.name:
            ax._ax.scatter(*self.center)
            ax._ax.text(*self.center, self.name)

    def _render_polygon_on_ax_(self, polygon, ax):
        path = Path.make_compound_path(
            Path(numpy.asarray(polygon.exterior.coords)[:, :]),
            *[Path(numpy.asarray(ring.coords)[:, :]) for ring in polygon.interiors])

        patch = PathPatch(path)
        collection = PatchCollection([patch], alpha=self.alpha, facecolor=self.facecolor, edgecolor=self.edgecolor)

        ax._ax.add_collection(collection, autolim=True)
        ax._ax.autoscale_view()

    def plot(self) -> Scene2D:
        figure = Scene2D(unit_size=(6, 6))
        ax = Axis(row=0, col=0, x_label='x', y_label='y', colorbar=False, equal=True)
        figure.add_axes(ax)
        figure._generate_axis_()

        if isinstance(self._shapely_object, geo.MultiPolygon):
            for poly in self._shapely_object.geoms:
                self._render_(instance=poly, ax=ax)

        else:
            self._render_(instance=self._shapely_object, ax=ax)

        return figure

    def __raster__(self, coordinate: numpy.ndarray) -> numpy.ndarray:
        Exterior = Path(self.exterior.coords)

        Exterior = Exterior.contains_points(coordinate)

        hole = self.hole.contains_points(coordinate)

        return Exterior.astype(int) - hole.astype(int)

    def contains_points(self, coordinate) -> numpy.ndarray:
        Exterior = Path(self.exterior.coords)
        return Exterior.contains_points(coordinate).astype(bool)

    @property
    def is_pure_polygon(self) -> bool:
        if isinstance(self._shapely_object, geo.Polygon):
            return True
        else:
            return False


# -
