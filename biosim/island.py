# -*- coding: utf-8 -*-

"""
Island class which gives a geographical structure of the multiline string provided.
Returns a numpy array with cell information equal to the number of characters in given string
"""
__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

from biosim.landscape import Lowland
#from .fauna import Herbivore
#from .fauna import Fauna
import numpy as np



class Island:
    """
    This class represents the given map string as an array of objects
    """

    def __init__(self, map):
        self.map = map
        self.island_map = self.convert_string_to_array()
        self.check_edge_cells_is_water(self.map)

        self.landscape_dict = {'W': Water, 'D': Desert, 'L': Lowland, 'H': Highland}
        self.fauna_dict = {'Herbivore': Herbivore,  'Carnivore': Carnivore
                           }

        self._cells = self.array_with_landscape_objects()

        rows = self._cells.shape[0]
        cols = self._cells.shape[1]
        self.map_dims = rows, cols

    @property
    def cells(self):
        """
         :return: landscape objects
        """
        return self._cells

    def convert_string_to_array(self):
        """
        Gets numpy array from multidimensional string
        """
        map_str_clean = self.map.replace(' ', '')  ## necessary?
        char_map = np.array([[col for col in row] for row in map_str_clean.splitlines()])
        return char_map

    @staticmethod  # Why is it static?
    def edges(island_array):
        """
        Finds the edges of the map for later use
        :param island_array: Array of the island
        :return: the map edges
        """
        rows, cols = island_array.shape[0], island_array.shape[1]
        island_edges = island_array[0, :cols], island_array[rows - 1, :cols], island_array[
                                                                              :rows - 1,
                                                                              0], island_array[
                                                                                  :rows - 1,
                                                                                  cols - 1]
        return island_edges

    def check_edge_cells_is_water(self, island_array):
        """
        Checks if the edge cells is water. Raises ValueError if the edges contain something
        else than water
        :param island_array:
        """
        edges = self.edges(island_array)
        for edge in edges:
            if np.all(edge != "W"):
                raise ValueError("The edges of the island map should only contain water cells")

    def array_with_landscape_objects(self):
        """
        Creates an array similar to the map with the same dimensions, but with the landscape
        objects corresponding to the landscape letter instead of a string
        :return: an array with the landscape objects
        """
        landscape_cell_object = np.empty(self.map.shape, dtype=object)
        for row in np.arange(self.map.shape[0]):
            for col in np.arange(self.map.shape[1]):
                landscape_type = self.map[row][col]
                landscape_cell_object[row][col] = self.landscape_dict[landscape_type]()
        return landscape_cell_object

    def adjacent_cells(self, n_rows, n_cols):
        """
        Finds the immediate adjacent cells
        :param n_rows: The number of rows
        :param n_cols: The number of columns
        :return: A list for adjacent cells
        """
        rows, cols = self.map_dims
        adjacent_cell_list = []
        if n_rows > 0:
            adjacent_cell_list.append(self._cells[n_rows-1,n_cols])
        if n_rows + 1 > n_rows:
            adjacent_cell_list.append(self._cells[n_rows+1, n_cols])
        if n_cols > 0:
            adjacent_cell_list.append(self._cells[n_rows, n_cols -1])
        if n_cols +1 < n_cols:
            adjacent_cell_list.append(self._cells[n_rows, n_cols +1])
        return adjacent_cell_list

    def life_cycle(self):
        """
        Iterates through all the cells and performs life cycle events. This should be called
        every year
        """
        print("New year")
        self.restart_migration() #write this function in landscape
        rows, cols = self.map_dims


    def add_animals(self, population):
        """
        Adds animals to the cells in the map
        #### Change docstring
        """
        for animal_group in population:
            loc = animal_group["loc"]
            animals = animal_group["pop"]
            for animal in animals:
                species = animal["species"]
                age = animal["age"]
                weight = animal["weight"]
                species_class = self.fauna_dict[species]
                animal_object = species_class(age=age, weight=weight)
                cell = self._cells[loc]
                print(animal_object)
                cell.add_animal(animal_object)

    def number_of_animals_per_species(self, species):
        """
        Calculates the total amount of animals per species on the island
        :param species: dictionary of
        :return: The total number of animals on the island
        """
        num_animals = 0
        rows, cols = self.map_dims
        for row in range(rows):
            for col in range(cols):
                cell = self._cells[row, col]
                num_animals += len(cell.fauna_dict[species])
        return num_animals



## SIMULATION FOR HERBIVORES AND CARNIVORES

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from biosim.fauna import Herbivore, Carnivore

    dict_animals = [{"species": "Herbivore", "age": 5, "weight": 25} for _ in range(50)]
    l = Lowland()
    for anim in dict_animals:
        if anim['species'] == "Herbivore":
            animal_object = Herbivore(age=anim['age'], weight=anim['weight'])


            l.add_animal(animal_object)



    # print(l.fauna_dict['Herbivore'])

    fig = plt.figure(figsize=(8, 6.4))
    plt.plot(0,len( l.fauna_dict['Herbivore']), '*-', color='b', lw=0.5)
    plt.draw()
    plt.pause(0.001)
    plt.show()


    # count list
    count_herb = [len(l.fauna_dict)]
    for i in range(200):
        l.animal_eats() # This updates the fodder as well
        l.animal_gives_birth()
        l.add_children_to_adult_animals()
        l.update_animal_weight_and_age()
        l.animal_dies()
        print("In year: {0} the number of animals is {1}".format(i + 1,
                                                                 len(l.fauna_dict["Herbivore"])))