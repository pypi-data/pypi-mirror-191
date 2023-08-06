#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused


class Fused19(BaseFused):
    def __init__(self,
                 fiber_radius: float,
                 fusion_degree: float,
                 index: float,
                 core_position_scrambling: float = 0):

        super().__init__(
            fiber_radius=fiber_radius,
            fusion_degree=fusion_degree,
            index=index,
            core_position_scrambling=core_position_scrambling
        )

        self.add_fiber_ring(
            number_of_fibers=6,
            fusion_degree=self.fusion_degree,
            fiber_radius=self.fiber_radius
        )

        self.add_fiber_ring(
            number_of_fibers=12,
            fusion_degree=self.fusion_degree,
            fiber_radius=self.fiber_radius
        )

        self.Object = self.compute_optimize_geometry()


if __name__ == '__main__':
    a = Fused19(fiber_radius=62.5, fusion_degree=0.6, index=1)
    a.plot(show_fibers=True, show_added=True, show_removed=True).show()
