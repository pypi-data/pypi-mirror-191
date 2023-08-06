#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused


class FusedTests(BaseFused):
    def __init__(self,
                 fusion_degree: float,
                 index: float,
                 core_position_scrambling: float = 0):

        super().__init__(index=index, core_position_scrambling=core_position_scrambling)

        # self.add_fiber_ring(
        #     number_of_fibers=6,
        #     fusion_degree=0.4,
        #     fiber_radius=62.5
        # )

        self.add_fiber_ring(
            number_of_fibers=3,
            fusion_degree=0.4,
            fiber_radius=62.5 / 2
        )

        self.compute_optimize_geometry()


if __name__ == '__main__':
    a = FusedTests(fusion_degree=0.7, index=1)

    a.plot(show_fibers=True, show_added=True, show_removed=True).show()
