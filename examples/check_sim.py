# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

"""
Compatibility check for BioSim simulations.

This script shall function with biosim packages written for
the INF200 project June 2020.
"""

__author__ = "Hans Ekkehard Plesser, NMBU"
__email__ = "hans.ekkehard.plesser@nmbu.no"

if __name__ == '__main__':
    plt.ion()

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr2 = """\
            WWWWWWWWW
            WDDDDDDDW
            WDDDDDDDW
            WDDDDDDDW
            WDDDDDDDW
            WDDDDDDDW
            WDDDDDDDW
            WDDDDDDDW
            WWWWWWWWW"""
    geogr = textwrap.dedent(geogr2)

    ini_herbs = [{'loc': (4, 4),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 50} for _ in range(1000)]}]
    ini_carns = [{'loc': (4, 4),
                  'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 50} for _ in range(1000)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456,
                 # hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                 #               'age': {'max': 60.0, 'delta': 2},
                 #               'weight': {'max': 60, 'delta': 2}},
                 )

    sim.set_animal_parameters("Herbivore",{'mu': 1, 'omega': 0, 'gamma': 0,
                                 'a_half': 1000})

    sim.set_animal_parameters('Carnivore',{'mu': 1, 'omega': 0, 'gamma': 0,
                                 'F': 0, 'a_half': 1000})

    sim.set_landscape_parameters('L', {'f_max': 700})

    sim.add_population(population=ini_carns)

    sim.simulate(num_years=100, vis_years=1, img_years=2000
                 )
    #I think the img_years is how often we save to file or something

    #sim.simulate(num_years=150, vis_years=1, img_years=2000
                 #)
    plt.savefig('check_sim_checkerboard.pdf')

    input('Press ENTER')

