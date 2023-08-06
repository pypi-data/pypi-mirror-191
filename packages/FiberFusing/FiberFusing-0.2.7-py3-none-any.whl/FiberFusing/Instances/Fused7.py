#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused


class Fused7(BaseFused):
    def __init__(self,
                 fiber_radius: float,
                 fusion_degree: float,
                 index: float,
                 core_position_scrambling: float = 0):

        super().__init__(index=index, core_position_scrambling=core_position_scrambling)

        assert 0.25 <= fusion_degree <= 0.65, "Fusion degree has to be in the range [0.25, 0.65]"

        self.add_fiber_ring(
            number_of_fibers=6,
            fusion_degree=fusion_degree,
            fiber_radius=fiber_radius
        )

        self.add_center_fiber(fiber_radius=fiber_radius)

        self.compute_optimize_geometry()


if __name__ == '__main__':
    a = Fused7(fiber_radius=62.5, fusion_degree=0.3, index=1)
    a.plot(show_fibers=True, show_added=True, show_removed=True).show()
