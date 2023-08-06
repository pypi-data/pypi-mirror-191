#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused


class Fused4(BaseFused):
    def __init__(self,
                 fiber_radius: float,
                 fusion_degree: float,
                 index: float,
                 core_position_scrambling: float = 0):

        super().__init__(index=index, core_position_scrambling=core_position_scrambling)

        FusionRange = [0, 1]
        assert FusionRange[0] <= fusion_degree <= FusionRange[1], f"Fusion degree has to be in the range {FusionRange}"

        self.add_fiber_ring(
            number_of_fibers=4,
            fusion_degree=fusion_degree,
            fiber_radius=fiber_radius
        )

        self.compute_optimize_geometry()


if __name__ == '__main__':
    a = Fused4(fiber_radius=62.5, fusion_degree=0.6, index=1)
    a.plot(show_fibers=True, show_added=True, show_removed=True).show()
