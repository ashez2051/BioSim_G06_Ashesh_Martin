# -*- coding: utf-8 -*-

"""
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

# -*- coding: utf-8 -*-

from biosim.island import Island
from biosim.landscape import Water, Desert, Lowland, Highland
from biosim.fauna import Carnivore, Herbivore
from biosim.graphics import Graphics
from biosim.visualization1 import Plotting

import numpy as np
import time
import pandas as pd
import os
import subprocess
#import ffmpeg
from os import path


DEFAULT_GRAPHICS_DIR = os.path.join('results/')
DEFAULT_GRAPHICS_NAME = 'biosim'
DEFAULT_MOVIE_FORMAT = 'mp4'

FFMPEG_BINARY = 'ffmpeg'
CONVERT_BINARY = 'magick'


class BioSim:
    """Main BioSim class for running simulations"""

    def __init__(
            self,
            island_map=None,
            ini_pop=[],
            seed=123,
            ymax_animals=None,
            cmax_animals=None,
            hist_specs=None,
            img_base=None,
            img_fmt="png",
            plot_graph=False,
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
        {'Herbivore': 50, 'Carnivore': 20}
        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
        {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.
        If img_base is None, no figures are written to file.
        Filenames are formed as
        '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """

        self.landscapes = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}
        self.landscapes_with_parameters = [Highland, Lowland]

        self.animal_species = {'Carnivore': Carnivore, 'Herbivore': Herbivore}

        for char in island_map.replace('\n', ''):
            if char not in self.landscapes:
                raise ValueError('This given string contains unknown geographies')

        lengths = [len(line) for line in island_map.splitlines()]
        if len(set(lengths)) > 1:
            raise ValueError('This given string is not uniform')
        self.island_map = island_map
        self._map = Island(island_map)
        np.random.seed(seed)

        self._ymax = ymax_animals
        self._cmax = cmax_animals

        self._hist_specs = hist_specs

        self.add_population(ini_pop)  # Add initial population to Island instance

        self._year = 0  # Year counter
        self._year_target = 0  # Number of simulated years total
        self._plot_bool = plot_graph  # Visualization on/off
        self._plot = None  # Plot figure for simulation initialized
        self.img_base = img_base  # Str for naming saved figures
        self._img_fmt = img_fmt  # Format saved figures

        if self.img_base:  # Create images folder
            if not path.exists("images"):
                os.mkdir('images')

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species. \n

        :param species: String, name of animal species \n
        :param params: Dict with valid parameter specification for species \n
        """
        if species in self.animal_species:
            species_type = self.animal_species[species]
            animal = species_type()
            animal.set_parameters(params)
        else:
            raise TypeError(species + ' parameters cant be assigned,there is no such data type')

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type. \n
        :param landscape: String, code letter for landscape \n
        :param params: Dict with valid parameter specification for landscape \n
        """
        if landscape in self.landscapes:
            landscape_type = self.landscapes[landscape]
            if landscape_type in self.landscapes_with_parameters:
                landscape_type.set_parameters(params)
            else:
                raise ValueError(landscape + ' parameter is not valid')

        else:
            raise TypeError(landscape + ' parameters cannot be assigned, there is no such '
                                        'data type')

    def add_population(self, population):
        """
        Add a population to the island \n

        :param population: List of dictionaries specifying population \n
        """
        self._map.add_animals(population)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        start_time = time.time()
        self._year_target += num_years

        if self._plot_bool and self._plot is None:
            self._plot = Plotting(self._map, cmax=self._cmax, ymax=self._ymax,
                hist_specs=self._hist_specs)
            self._map.number_of_animals_per_species()
            self._plot.init_plot(num_years)
            self._plot.y_herb[self._year] = self._map.number_of_animals_per_species['Herbivores']
            self._plot.y_carn[self._year] = self._map.number_of_animals_per_species['Carnivores']

        elif self._plot_bool:
            self._plot.set_x_axis(self._year_target)
            self._plot.y_herb += [np.nan for _ in range(num_years)]
            self._plot.y_carn += [np.nan for _ in range(num_years)]

        for _ in range(num_years):
            self._map.life_cycle_in_rossumoya()
            print(f"Year: {self._year}")
            #print(f"Animals: {self._map.number_of_animals_per_species('Herbiv')}")
            #print(f"Herbivores: {self._map.number_of_animals_per_species['Herbivores']}")
            #print(f"Carnivore: {self._map.number_of_animals_per_species['Herbivores']}")
            if self._plot_bool:
                self._plot.y_herb[self._year] = self._map.number_of_animals_per_species['Herbivores']
                self._plot.y_carn[self._year] = self._map.number_of_animals_per_species['Herbivores']
                if self._year % vis_years == 0:
                    self._map.number_of_animals_per_species()
                    self._plot.update_plot()

            if self.img_base is not None:
                if img_years is None:
                    if self._year % vis_years == 0:
                        self._plot.save_graphics(self._img_base, self._img_fmt)

                else:
                    if self._year % img_years == 0:
                        self._plot.save_graphics(self._img_base, self._img_fmt)

        finish_time = time.time()

        print("Simulation complete.")
        print("Elapsed time: {:.6} seconds".format(finish_time - start_time))

    @property
    def year(self):
        """
        Last year simulated. \n
        """
        return self._year

    @property
    def num_animals(self):
        """
        Total number of animals on island. \n
        """
        animal_count = 0
        for species in self.animal_species:
            animal_count += self._map.number_of_animals_per_species(species)
            return animal_count

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary. \n
        """
        num_fauna_per_species = {}
        for species in self.animal_species:
            num_fauna_per_species[species] = self._map.number_of_animals_per_species(species)
        return num_fauna_per_species

    @property
    def animal_distribution(self):
        """
        Pandas DataFrame with animal count per species for each cell on the island. \n
        """
        animal_df = []
        rows, cols = self._map.map_dims
        for row in range(rows):
            for col in range(cols):
                cell = self._map.cells[row, col]
                animal_count = cell.cell_fauna_count
                animal_df.append({'Row': row, 'Col': col, 'Herbivore': animal_count['Herbivore'],
                                  'Carnivore': animal_count['Carnivore']})
        return pd.DataFrame(animal_df)

    # def make_movie(self, movie_fmt=DEFAULT_MOVIE_FORMAT):
    #     """
    #     Create MPEG4 movie from visualization images saved. \n
    #     """
    #     if self.img_base is None:
    #         raise RuntimeError('No filename defined')
    #
    #     if movie_fmt == 'mp4':
    #         try:
    #             subprocess.check_call(
    #                 [FFMPEG_BINARY, '-i', '{}_%05d.png'.format(self.img_base), '-y', '-profile:v',
    #                  'baseline', '-level', '3.0', '-pix_fmt', 'yuv420p',
    #                  '{}.{}'.format(self.img_base, movie_fmt)])
    #         except subprocess.CalledProcessError as err:
    #             raise RuntimeError('Error: ffmpeg failed with: {}'.format(err))
    #     elif movie_fmt == 'gif':
    #         try:
    #             subprocess.check_call(
    #                 [CONVERT_BINARY, '-delay', '1', '-loop', '0', '{}_*.png'.format(self.img_base),
    #                  '{}.{}'.format(self.img_base, movie_fmt)])
    #         except subprocess.CalledProcessError as err:
    #             raise RuntimeError('Error: convert failed with: {}'.format(err))
    #     else:
    #         raise ValueError('Unknown movie format')
    #
