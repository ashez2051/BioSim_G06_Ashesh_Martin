# -*- coding: utf-8 -*-

"""
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import textwrap
import subprocess
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from .island import Island
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

from biosim.island import Island
from biosim.landscape import Water, Desert, Lowland, Highland
from biosim.fauna import Carnivore, Herbivore

#matplotlib.use('macosx')

FFMPEG_BINARY = 'ffmpeg'
DEFAULT_MOVIE_FORMAT = 'mp4'


class BioSim:
    """Responsible to provide to the user an interface for simulation as
    well as visualization."""

    map_colors = {
        "W": mcolors.to_rgba("navy"),
        "L": mcolors.to_rgba("forestgreen"),
        "H": mcolors.to_rgba("#e1ab62"),
        "D": mcolors.to_rgba("salmon"),
    }
    map_labels = {
        "W": "Water",
        "L": "Lowland",
        "H": "Highland",
        "D": "Desert",

    }

    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_fmt='png'):
        """
        BioSims package constructor.
        Parameters
        ----------
        island_map:
            Multi-line string specifying island geography.
        ini_pop:
            List of dictionaries specifying initial population.
        seed:
            Integer used as random number seed.
        ymax_animals:
            Number specifying y-axis limit for graph showing animal
            numbers.
        cmax_animals:
            Dict specifying color-code limits for animal densities.
        img_base:
            String with beginning of file name for figures, including
            path.
        img_fmt:
            String with file type for figures, e.g. ’png’.
        Notes
        ----------
            -> If ymax_animals is None, the y-axis limit should be
               adjusted automatically.
            -> If cmax_animals is None, sensible, fixed default values
               should be used. cmax_animals is a dict mapping species
               names to numbers, e.g., {’Herbivore’: 50, ’Carnivore’:
               20}.
            -> If img_base is None, no figures are written to file.
               Filenames are formed as ’{}_{:05d}.{}’.format(img_base,
               img_no, img_fmt) where img_no are consecutive image
               numbers starting from 0.
            -> img_base should contain a path and beginning of a file
               name.
        """
        self.animal_species = None
        self._map = island_map
        self.island = Island(self._map)
        self.island.add_animals(ini_pop)
        np.random.seed(seed)
        self.last_year = 0
        self.year_num = 0
        self.img_no = 0
        self.final_year = None
        self.img_fmt = img_fmt
        self.fig = None
        self._island_map = None
        self._img_axis = None
        self._mean_ax = None
        self._herbivore_line = None
        self._carnivore_line = None
        self.herb_pop = None
        self.carn_pop = None
        self._herb_img_axis = None
        self._carn_img_axis = None

        self.animal_species = {'Carnivore': Carnivore, 'Herbivore': Herbivore}
        self.landscapes = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}
        self.landscapes_with_parameters = [Highland, Lowland]

        if img_base is None:
            self.img_base = None
        else:
            self.img_base = img_base

        self.ymax_animals = None if ymax_animals is None \
            else ymax_animals

        self.cmax_animals = None if ymax_animals is None \
            else cmax_animals

    @property
    def generate_map_array(self):
        """This method generates the colored island map array.
        Returns
        ----------
            Array with the map colors.
        """
        lines = textwrap.dedent(self._map).splitlines()
        if len(lines[-1]) == 0:
            lines = lines[:-1]

        num_cells = len(lines[0])
        map_array = []
        for line in lines:
            map_array.append([])
            if num_cells is not len(line):
                raise ValueError('All lines in the map must have the '
                                 'same number of cells.')
            for letter in line:
                if letter not in self.map_colors:
                    raise ValueError(
                        f"'{letter}' is not a valid landscape type. "
                        f"Must be one of {set(self.map_colors.keys())}")
                map_array[-1].append(self.map_colors[letter])
        return map_array

    @property
    def num_animals(self):
        """Total number of animals on island."""
        animal_count = 0
        for species in self.animal_species:
            animal_count += self._map.number_of_animals_per_species(species)
            return animal_count

    @property
    def year(self):
        """Last year simulated.
        Returns
        ----------
            int
        """
        return self.last_year

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_fauna_per_species = {}
        for species in self.animal_species:
            num_fauna_per_species[species] = self.island.number_of_animals_per_species(species)
        return num_fauna_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell
        on island."""
        animal_df = []
        rows, cols = self.island.map_dims
        for row in range(rows):
            for col in range(cols):
                cell = self.island.cells[row, col]
                animal_count = cell.cell_fauna_count
                animal_df.append({'Row': row, 'Col': col, 'Herbivore': animal_count['Herbivore'],
                                  'Carnivore': animal_count['Carnivore']})
        return pd.DataFrame(animal_df)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species in self.animal_species:
            species_type = self.animal_species[species]
            animal = species_type()
            animal.set_parameters(params)
        else:
            raise TypeError(species + ' parameters cant be assigned,there is no such data type')

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
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
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.add_animals(population)


    def simulate(self, num_years, vis_years=1, img_years=None):
        """This method is the simulation procedures.
        Parameters
        ----------
        num_years: int
        vis_years: int
        img_years: int
        """
        if img_years is None:
            img_years = vis_years

        self.last_year += num_years
        self.final_year = self.year_num + num_years
        self.setup_graphics(), self.update_graphics()

        while self.year_num < self.final_year:
            self.island.life_cycle_in_rossumoya()

            if self.year_num % vis_years == 0:
                self.update_graphics()

            if self.year_num % img_years == 0:
                self.save_figures()

            self.year_num += 1

    def save_figures(self):
        """This method saves the simulated graphic figures on a
        given image base."""
        if self.img_base is None:
            pass
        else:
            plt.savefig('{}_{:05d}.{}'.format(self.img_base,
                                              self.img_no,
                                              self.img_fmt))
            self.img_no += 1

    def create_mp4(self, mov_fmt=DEFAULT_MOVIE_FORMAT):
        """
                This method creates a movie from the images obtained
                from the visualization plots.
                Parameters
                ----------
                mov_fmt: 'mp4'
                    DEFAULT_MOVIE_FORMAT = 'mp4'
        """
        if self.img_base is None:
            raise RuntimeError("No Image base defined.")

        if mov_fmt == 'mp4':
            try:
                subprocess.check_call([FFMPEG_BINARY,
                                       '-i',
                                       '{}_%05d.png'.format(
                                           self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base,
                                                      mov_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ffmpeg failed: {}'.format(err))

    def setup_graphics(self):
        """This method setups the graphics of the visualization."""
        if self.fig is None:
            self.fig = plt.figure(figsize=[12, 7])
            self.fig.canvas.set_window_title('BioSim Window')

        if self._island_map is None:
            self.static_map()

        if self._mean_ax is None:
            self._mean_ax = self.fig.add_subplot(2, 2, 2)
            self._mean_ax.set_ylim(0, 30000)

        self._mean_ax.set_xlim(0, self.final_year)
        self.herbivore_line()
        self.carnivore_line()

        if self.herb_pop is None:
            self.herb_pop = self.fig.add_subplot(2, 2, 3)
            self._herb_img_axis = None

        if self.carn_pop is None:
            self.carn_pop = self.fig.add_subplot(2, 2, 4)
            self._carn_img_axis = None

        self.fig.tight_layout()

    def herbivore_line(self):
        """This method creates the herbivore line on the graphic."""
        if self._herbivore_line is None:
            plot = self._mean_ax.plot(
                np.arange(0, self.final_year),
                np.nan * np.ones(self.final_year))
            self._herbivore_line = plot[0]
        else:
            xdata, ydata = self._herbivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self.final_year)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self._herbivore_line.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

    def carnivore_line(self):
        """This method creates the carnivore line on the graphic."""
        if self._carnivore_line is None:
            carnivore_plot = self._mean_ax.plot(
                np.arange(0, self.final_year),
                np.nan * np.ones(self.final_year))
            self._carnivore_line = carnivore_plot[0]
        else:
            xdata, ydata = self._carnivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self.final_year)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self._carnivore_line.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

    def static_map(self):
        """This method creates the static map on the visualization."""
        self._island_map = self.fig.add_subplot(2, 2, 1)
        self._island_map.imshow(self.generate_map_array)
        patches = []
        for i, (landscape, l_color) in enumerate(
                self.map_colors.items()):
            patch = mpatches.Patch(color=l_color,
                                   label=self.map_labels[landscape])
            patches.append(patch)
        self._island_map.legend(handles=patches)

    def update_counter_graph(self, pop_count):
        """This method updates the population counter for herbivore
        and carnivore."""
        herb_count, carn_count = list(pop_count.values())

        herb = self._herbivore_line.get_ydata()
        herb[self.year_num] = herb_count
        self._herbivore_line.set_ydata(herb)

        carn = self._carnivore_line.get_ydata()
        carn[self.year_num] = carn_count
        self._carnivore_line.set_ydata(carn)

    def update_herb(self, pop):
        """This method updates the herbivore population on the
        graphic."""
        if self._herb_img_axis is not None:
            self._herb_img_axis.set_data(pop)
        else:
            self._herb_img_axis = self.herb_pop.imshow(
                pop, vmin=0,
                vmax=200,
                interpolation='nearest',
                aspect='auto',
                cmap="Spectral")
            plt.colorbar(self._herb_img_axis, ax=self.herb_pop)
            self.herb_pop.set_xticks(
                range(0, len(self.generate_map_array[0]), 5))
            self.herb_pop.set_xticklabels(range(1, 1 + len(
                self.generate_map_array[0]), 5))

            self.herb_pop.set_yticks(
                range(0, len(self.generate_map_array), 5))
            self.herb_pop.set_yticklabels(range(1, 1 + len(
                self.generate_map_array), 5))
            self.herb_pop.set_title('Herbivore distribution')

    def update_carn(self, distribution):
        """This method updates the Carnivore population on the
        graphic."""
        if self._carn_img_axis is not None:
            self._carn_img_axis.set_data(distribution)

        else:
            self._carn_img_axis = self.carn_pop.imshow(
                distribution, vmin=0, vmax=200, interpolation='nearest',
                aspect='auto', cmap="Spectral")

            plt.colorbar(self._carn_img_axis, ax=self.carn_pop)
            self.carn_pop.set_xticks(range(0,
                                           len(self.generate_map_array[
                                                   0]), 5))
            self.carn_pop.set_xticklabels(range(1, 1 + len(
                self.generate_map_array[0]), 5))

            self.carn_pop.set_yticks(
                range(0, len(self.generate_map_array), 5))

            self.carn_pop.set_yticklabels(range(1, 1 + len(
                self.generate_map_array), 5))

            self.carn_pop.set_title('Carnivore distribution')

    def setup_graphics(self):
        """This method setups the graphics of the visualization."""
        if self.fig is None:
            self.fig = plt.figure(figsize=[12, 7])
            self.fig.canvas.set_window_title('BioSim Window')

        if self._island_map is None:
            self.static_map()

        if self._mean_ax is None:
            self._mean_ax = self.fig.add_subplot(2, 2, 2)
            self._mean_ax.set_ylim(0, 20000)

        self._mean_ax.set_xlim(0, self.final_year)
        self.herbivore_line()
        self.carnivore_line()

        if self.herb_pop is None:
            self.herb_pop = self.fig.add_subplot(2, 2, 3)
            self._herb_img_axis = None

        if self.carn_pop is None:
            self.carn_pop = self.fig.add_subplot(2, 2, 4)
            self._carn_img_axis = None

        self.fig.tight_layout()

    def herbivore_line(self):
        """This method creates the herbivore line on the graphic."""
        if self._herbivore_line is None:
            plot = self._mean_ax.plot(np.arange(0, self.final_year),
                np.nan * np.ones(self.final_year))
            self._herbivore_line = plot[0]
        else:
            xdata, ydata = self._herbivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self.final_year)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self._herbivore_line.set_data(np.hstack((xdata, xnew)), np.hstack((ydata, ynew)))

    def carnivore_line(self):
        """This method creates the carnivore line on the graphic."""
        if self._carnivore_line is None:
            carnivore_plot = self._mean_ax.plot(np.arange(0, self.final_year),
                np.nan * np.ones(self.final_year))
            self._carnivore_line = carnivore_plot[0]
        else:
            xdata, ydata = self._carnivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self.final_year)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self._carnivore_line.set_data(np.hstack((xdata, xnew)), np.hstack((ydata, ynew)))

    def static_map(self):
        """This method creates the static map on the visualization."""
        self._island_map = self.fig.add_subplot(2, 2, 1)
        self._island_map.imshow(self.generate_map_array)
        patches = []
        for i, (landscape, l_color) in enumerate(self.map_colors.items()):
            patch = mpatches.Patch(color=l_color, label=self.map_labels[landscape])
            patches.append(patch)
        self._island_map.legend(handles=patches)

    def update_counter_graph(self, pop_count):
        """This method updates the population counter for herbivore
        and carnivore."""
        herb_count, carn_count = list(pop_count.values())

        herb = self._herbivore_line.get_ydata()
        herb[self.year_num] = herb_count
        self._herbivore_line.set_ydata(herb)

        carn = self._carnivore_line.get_ydata()
        carn[self.year_num] = carn_count
        self._carnivore_line.set_ydata(carn)

    def update_herb(self, pop):
        """This method updates the herbivore population on the
        graphic."""
        if self._herb_img_axis is not None:
            self._herb_img_axis.set_data(pop)
        else:
            self._herb_img_axis = self.herb_pop.imshow(pop, vmin=0, vmax=200,
                interpolation='nearest', aspect='auto', cmap="Spectral")
            plt.colorbar(self._herb_img_axis, ax=self.herb_pop)
            self.herb_pop.set_xticks(range(0, len(self.generate_map_array[0]), 5))
            self.herb_pop.set_xticklabels(range(1, 1 + len(self.generate_map_array[0]), 5))

            self.herb_pop.set_yticks(range(0, len(self.generate_map_array), 5))
            self.herb_pop.set_yticklabels(range(1, 1 + len(self.generate_map_array), 5))
            self.herb_pop.set_title('Herbivore distribution')

    def update_carn(self, distribution):
        """This method updates the Carnivore population on the
        graphic."""
        if self._carn_img_axis is not None:
            self._carn_img_axis.set_data(distribution)

        else:
            self._carn_img_axis = self.carn_pop.imshow(distribution, vmin=0, vmax=200,
                interpolation='nearest', aspect='auto', cmap="Spectral")

            plt.colorbar(self._carn_img_axis, ax=self.carn_pop)
            self.carn_pop.set_xticks(range(0, len(self.generate_map_array[0]), 5))
            self.carn_pop.set_xticklabels(range(1, 1 + len(self.generate_map_array[0]), 5))

            self.carn_pop.set_yticks(range(0, len(self.generate_map_array), 5))

            self.carn_pop.set_yticklabels(range(1, 1 + len(self.generate_map_array), 5))

            self.carn_pop.set_title('Carnivore distribution')

    def update_graphics(self):
        """This method updates the graphics with the simulated data
        provided by the Pandas DataFrame."""
        counter = self.animal_distribution
        row = len(self.generate_map_array)
        col = len(self.generate_map_array[0])

        self.update_counter_graph(self.num_animals_per_species)
        self.update_herb(np.array(counter.Herbivore).reshape(row, col))
        self.update_carn(np.array(counter.Carnivore).reshape(row, col))
        plt.pause(1e-6)
        self.fig.suptitle('Year: {}'.format(self.year_num), x=0.025, fontsize=10)


