# -*- coding: utf-8 -*-

"""
"""
__author__ = "Ashesh Raj Gnawali, Martin Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import numpy as np
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches


class Graphics:
    """
    Source: Yngve Mardal Moe, Biosim material january 2020
    The graphics class contains everything that is needed to plot graphs from Rossumøya
    :param map_layout: Multiline string of the island map
    :param figure: Creates a blank canvas to add subplots to
    :param map_dims: Dimensions of the map, number of rows and columns
    """
    map_colors = {"W": mcolors.to_rgba("navy"), "L": mcolors.to_rgba("forestgreen"),
                  "H": mcolors.to_rgba("springgreen"), "D": mcolors.to_rgba("navajowhite")}

    map_labels = {"W": "Water", "L": "Lowland", "H": "Highland", "D": "Desert"}

    def __init__(self, map_layout, figure, map_dims):
        self.map_layout = map_layout
        self.fig = figure
        self.map_dims = map_dims
        self.map_colors = Graphics.map_colors
        self.map_graph = None
        self.herbivore_curve = None
        self.carnivore_curve = None
        self.herbivore_dist = None
        self.carnivore_dist = None
        self.mean_ax = None
        self.fit_ax = None
        self.fit_axis = None
        self.wt_ax = None
        self.age_ax = None
        self.herbivore_image_axis = None
        self.carnivore_image_axis = None

    def create_map(self):
        """
        Convert the string to image array, raises value error if the rows does not have the
        same amount of columns or if it has an invalid landscape type
        """
        lines = self.map_layout.splitlines()
        if len(lines[-1]) == 0:
            lines = lines[:-1]

        num_cells = len(lines[0])
        map_array = []
        for line in lines:
            map_array.append([])
            if num_cells != len(line):
                raise ValueError("All lines in the map must have the same number of cells.")
            for letter in line:
                if letter not in self.map_colors:
                    raise ValueError('Not a valid landscape type')
                map_array[-1].append(self.map_colors[letter])

        return map_array

    def create_histograms_setup(self):

        self.fit_ax = self.fig.add_subplot(6, 3, 16)
        self.fit_ax.title.set_text('Fitness Histogram')
        self.age_ax = self.fig.add_subplot(6, 3, 17)
        self.age_ax.title.set_text('Age Histogram')
        self.wt_ax = self.fig.add_subplot(6, 3, 18)
        self.wt_ax.title.set_text('Weight Histogram')

    def create_island_graph(self):
        """
        Creates a map for the island in subplot (3, 3, 1)
        """
        if self.map_graph is None:
            self.map_graph = self.fig.add_subplot(3, 3, 1)
            self.map_graph.imshow(self.create_map())
            self.map_graph.set_title('Island')
            self.map_graph.set_yticklabels([])
            self.map_graph.set_xticklabels([])
        patches = []
        for i, (landscape, l_color) in enumerate(self.map_colors.items()):
            patch = mpatches.Patch(color=l_color, label=self.map_labels[landscape])
            patches.append(patch)
        self.map_graph.legend(handles=patches)

    def create_herbivore_graph(self, final_year, recreate=False):
        """
        Creates a line plot for herbivores by themselves
        """
        if (self.herbivore_curve is None) or recreate:
            plot = self.mean_ax.plot(np.arange(0, final_year), np.full(final_year, np.nan), "r")
            self.herbivore_curve = plot[0]

        else:
            x_data, y_data = self.herbivore_curve.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.herbivore_curve.set_data(np.hstack((x_data, x_new)),
                                              np.hstack((y_data, y_new)))

    def create_carnivore_graph(self, final_year, recreate=False):
        """
        Creates a line plot for carnivores by themselves
        """
        if (self.carnivore_curve is None) or recreate:
            plot = self.mean_ax.plot(np.arange(0, final_year), np.full(final_year, np.nan), "g")
            self.carnivore_curve = plot[0]
        else:
            x_data, y_data = self.carnivore_curve.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.carnivore_curve.set_data(np.hstack((x_data, x_new)),
                                              np.hstack((y_data, y_new)))

    def update_graphs(self, year, herb_count, carn_count):
        """
        Updates graphs according to number of years and animals count
        in subplot(3, 3, 2)
        """
        herb_ydata = self.herbivore_curve.get_ydata()
        herb_ydata[year] = herb_count
        self.herbivore_curve.set_ydata(herb_ydata)

        carn_ydata = self.carnivore_curve.get_ydata()
        carn_ydata[year] = carn_count
        self.carnivore_curve.set_ydata(carn_ydata)
        self.fig.suptitle('Graphics for Year: ' + str(year), x=0.5)

    def create_animal_graphs(self, final_year, y_lim, recreate=False):
        """
        Creates separate line graphs for Herbivores and Carnivores
        """
        if self.mean_ax is None:
            self.mean_ax = self.fig.add_subplot(3, 3, 3)
            self.mean_ax.set_ylim(0, y_lim)

        self.mean_ax.set_xlim(0, final_year + 1)
        self.create_herbivore_graph(final_year, recreate=recreate)
        self.create_carnivore_graph(final_year, recreate=recreate)
        self.mean_ax.set_title('Animal Graphs')

    def animal_distribution_graphs(self):
        """
        Creates the distribution graphs for herbivore and
        carnivore distribution
        """
        if self.herbivore_dist is None:
            self.herbivore_dist = self.fig.add_subplot(3, 3, 4)
            self.herbivore_dist.set_yticklabels([])
            self.herbivore_dist.set_xticklabels([])
            self.herbivore_image_axis = None

        if self.carnivore_dist is None:
            self.carnivore_dist = self.fig.add_subplot(3, 3, 6)
            self.carnivore_dist.set_yticklabels([])
            self.carnivore_dist.set_xticklabels([])
            self.carnivore_image_axis = None

    def update_herbivore_distribution(self, distribution):
        """
        Updates herbivore distribution in subplot (3, 3, 4)
        """
        if self.herbivore_image_axis is not None:
            self.herbivore_image_axis.set_data(distribution)
        else:
            self.herbivore_image_axis = self.herbivore_dist.imshow(distribution,
                                                                   interpolation='nearest', vmin=0,
                                                                   vmax=100)

            self.herbivore_image_axis.figure.colorbar(self.herbivore_image_axis,
                                                      ax=self.herbivore_dist,
                                                      orientation='vertical', fraction=0.07,
                                                      pad=0.04)

            self.herbivore_dist.set_title('Herbivore Distribution')

    def update_carnivore_distribution(self, distribution):
        """
        updates Carnivore distribution subplot (3, 3, 6)
        """
        if self.carnivore_image_axis is not None:
            self.carnivore_image_axis.set_data(distribution)
        else:
            self.carnivore_image_axis = self.carnivore_dist.imshow(distribution,
                                                                   interpolation='nearest', vmin=0,
                                                                   vmax=100)
            self.carnivore_image_axis.figure.colorbar(self.carnivore_image_axis,
                                                      ax=self.carnivore_dist,
                                                      orientation='vertical', fraction=0.07,
                                                      pad=0.04)

            self.carnivore_dist.set_title('Carnivore Distribution')

    def update_histogram(self, fit_list=None, age_list=None, wt_list=None):
        """
        Updates the histograms in the main plot. Colors are set to green for herbivores \n
        and red for carnivores.
        """
        self.fit_ax.clear()
        self.fit_ax.title.set_text('Fitness Histogram')
        self.fit_ax.hist(fit_list['Herbivore'], bins=20, histtype='step', color="g")
        self.fit_ax.hist(fit_list['Carnivore'], bins=20, histtype='step', color="r")
        self.age_ax.clear()
        self.age_ax.title.set_text('Age Histogram')
        self.age_ax.hist(age_list['Herbivore'], bins=20, histtype='step', color="g")
        self.age_ax.hist(age_list['Carnivore'], bins=20, histtype='step', color="r")
        self.wt_ax.clear()
        self.wt_ax.title.set_text('Weight Histogram')
        self.wt_ax.hist(wt_list['Herbivore'], bins=20, histtype='bar', color="g")
        self.wt_ax.hist(wt_list['Carnivore'], bins=100, histtype='bar', color="r")

    def set_year(self, year):
        """
        Set the year on the Figure
        """
        self.fig.suptitle('Graphics for Year: ' + str(year), x=0.5)
