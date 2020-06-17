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
    # import time
    # start_time = time.time()

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

    ini_herbs = [{'loc': (5, 5),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 200} for _ in range(200)]}]
    ini_carns = [{'loc': (5, 5),
                  'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 200} for _ in range(200)]}]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=1,
                 # hist_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                 #               'age': {'max': 60.0, 'delta': 2},
                 #               'weight': {'max': 60, 'delta': 2}},
                 )
    sim.set_animal_parameters("Herbivore",
                              {"zeta": 3.2, "xi": 1., "F": 0, "omega":0, "gamma":0, "a_half":1000,
                               "mu":1})
    sim.set_animal_parameters("Carnivore", {
                                            "phi_age": 0.5,
                                            "DeltaPhiMax": 9, "F": 0, "omega":0, "gamma":0, "a_half":1000,
    "mu":1})

    sim.set_landscape_parameters('L', {'f_max': 700})

    #sim.simulate(num_years=100, vis_years=1, img_years=2000)

    sim.add_population(population=ini_carns)
    sim.simulate(num_years=20, vis_years=1, img_years=2000)

    # I think the img_years is how often we save to file

    # print("--- %s seconds ---" % (time.time() - start_time))
    plt.savefig('check_sim.pdf')
    # sim.make_movie()

    input('Press ENTER')
