__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import numpy as np
from biosim import Fauna #How do we import this?

class Landscape:
    """
    Parent class for various landscapes water, desert, highland and lowland
    """

    parameters ={}

    def __init__(self):
        self.sorted_animal_fitness_dict = {} #needed for when we introduce carnivores
        self.fauna_dict = {"Hebivore": []} # Add carnivore later
        self.updated_fauna_dict = {"Hebivore": []} # Add carnivore later
        self._remaining_food = {'Herbivore': 0, 'Carnivore': 0} #might need to have the same name as the method remaining_food


    def add_animal(self, animal):
        """
        Adds the animal object to the species list of cell
        :param animal: Input animal object, #Will specify what this actually is later
        """
        species = animal.__class__.__name__
        self.fauna_dict[species].append(animal)


    def remove_animal(self, animal):
        """
        Removes the animal object from the list of species of cell
        :param animal: Input animal object, #Will specify what this actually is later
        :return:
        """
        species = animal.__class__.__name__
        self.fauna_dict[species].remove(animal)

    def update_fitness(self, animal,species):
        """
        Updates the fitness of herbivores or carnivores
        :param animal: animal object
        :param species: an animal can be herbivore or a carnivore
        """
        animal_fitness ={}
        for animal_iter in animal[species]:
            animal_fitness[animal_iter] =animal.fitness
        self.sorted_animal_fitness_dict[species] = animal_fitness

    def animal_eats(self):
        """
        The animals in the cells feed, the herbivores feed on fodder and the carnivores
        on herbivores
        """
        self.update_fodder()
        self.herbivore_eats()
        #self.carnivore_eats()

    def available_food(self, animal):
        """
        Returns the remaining food value in a cell.
        This is different for the two species
        :param animal: animal object
        :return: the remaining amount of food
        """
        species = animal.__class__.__name__
        return self.remaining_food[species]

    def herbivore_eats(self):
        """
        Herbivores eat randomly, and if there is no fodder available in the cell, the animal
        doesn't eat.
        If the available fodder is greater than the food the animal requires, we calculate the food
        that remains.
        If the fodder available is less than the food required by the animal we update remaining
        fodder as 0.
        """
        np.random.shuffle(self.fauna_dict["Herbivore"])
        for herb in fauna_dict["Herbivore"]:
            herb_remaining_fodder = self.remaining_food['Herbivore']
            if herb_remaining_fodder == 0:
                break
            elif herb_remaining_fodder >= herb.parameters['F']:
                herb.animal_eats(herb.parameters['F'])
                self.remaining_food['Herbivore'] -= herb.parameters['F']
            else:
                self.remaining_food["Herbivore"] = 0

    @property
    def remaining_food(self):
        """
        Gives the remaining food in a cell
        :return: the remaining amount of food
        """
        if isinstance(self, Water):
            raise ValueError("There is no fodder available in the water")
        elif isinstance(self, Desert):
            self._remaining_food = {'Herbivore': 0}
        else:
            self._remaining_food = {"Herbivore": self._remaining_food["Herbivore"]}
        return self._remaining_food


    def update_animal_weight(self):
        """
        Each year the animals ages by 1 and loses weight by a factor of eta
        """
        for species in self.fauna_dict:
            for animal in self.fauna_dict[species]:
                animal.



    def animal_gives_birth(self):
        pass

    def add_children_to_adult_animals(self):
        pass

    def animal_dies(self):
        pass

    def grow_all_animals(self): #aging?
        pass

    def cell_fauna_count(self):
        pass

    def total_herbivore_weight(self): #not needed before we introduce carnivores
        pass



class Water(Landscape):
    def __init__(self):
        pass


class Desert(Landscape):
    def __init__(self):
        pass


class Highland(Landscape):
    def __init__(self):
        pass


class Lowland(Landscape):
    def __init__(self):
        pass

if __name__ == "__main__":
    print(np.random.shuffle(["a","b","c"]))
