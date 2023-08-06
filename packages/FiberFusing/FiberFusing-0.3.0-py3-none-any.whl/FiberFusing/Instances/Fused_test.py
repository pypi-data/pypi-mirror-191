#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused


class FusedTests(BaseFused):
    def __init__(self,
                 fusion_degree: float,
                 index: float,
                 core_position_scrambling: float = 0):

        super().__init__(index=index)

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

        self.init_connected_fibers()

        self.compute_optimal_structure()

        self.compute_core_position()

        self.randomize_core_position(randomize_position=core_position_scrambling)


if __name__ == '__main__':
    instance = FusedTests(
        fusion_degree=0.6, 
        index=1
    )

    figure = instance.plot(
        show_structure=True, 
        show_fibers=True, 
        show_cores=False,
        show_added=False
    )

    figure.show()

# -
