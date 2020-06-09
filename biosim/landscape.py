__author__ = "Ashesh Raj Gnawali, Maritn Bø"
__email__ = "asgn@nmbu.no & mabo@nmbu.no"

import numpy as np
import math
from .fauna import Fauna, Herbivore


class Landscape:
    """
    Parent class for various landscapes water, desert, highland and lowland
    """

    parameters = {}

    def __init__(self):
        self.sorted_animal_fitness_dict = {}  # needed for when we introduce carnivores
        self.fauna_dict = {"Herbivore": []}  # Add carnivore later
        self.updated_fauna_dict = {"Herbivore": []}  # Add carnivore later
        self.food_left = {'Herbivore': 0,
                          'Carnivore': 0}  # might need to have the same name as the method remaining_food

    def add_animal(self, animal):
        """
        Adds the animal object to the species list of cell(?)
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

    def update_fitness(self, animal, species):
        """
        Updates the fitness of herbivores or carnivores
        :param animal: animal object
        :param species: an animal can be herbivore or a carnivore
        """
        animal_fitness = {}
        for animal_iter in animal[species]:
            animal_fitness[animal_iter] = animal.fitness
        self.sorted_animal_fitness_dict[species] = animal_fitness

    def animal_eats(self):
        """
        The animals in the cells feed, the herbivores feed on fodder and the carnivores
        on herbivores
        """
        self.update_fodder()
        self.herbivore_eats()  # self.carnivore_eats()

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
        for herb in self.fauna_dict["Herbivore"]:
            herb_remaining_fodder = self.remaining_food['Herbivore']
            if herb_remaining_fodder == 0:
                break
            elif herb_remaining_fodder >= herb.parameters['F']:
                herb.animal_weight_with_food(herb.parameters['F'])
                self.remaining_food['Herbivore'] -= herb.parameters['F']
            elif 0 < herb_remaining_fodder < herb.parameters["F"]:
                herb.animal_weight_with_food(herb_remaining_fodder)
                self.remaining_food['Herbivore'] = 0

    @property
    def remaining_food(self):
        """
        Gives the remaining food in a cell
        :return: the remaining amount of food
        """
        if isinstance(self, Water):
            raise ValueError("There is no fodder available in the water")
        elif isinstance(self, Desert):
            self.food_left = {'Herbivore': 0}
        else:
            self.food_left = {"Herbivore": self.food_left["Herbivore"]}
        return self.food_left

    def update_animal_weight_and_age(self):
        """
        Each year the animals ages by 1 and loses weight by a factor of eta
        """
        for species in self.fauna_dict:
            for animal in self.fauna_dict[species]:
                animal.animal_weight_with_age()

    def animal_gives_birth(self):
        """
        Compares the birth_probability of an animal with the randomly generated value between
        0 and 1 and if it's greater it, the animal gives birth. Creates the child of the same
        species and decreases the weight of an animal
        """
        for species, animals in self.updated_fauna_dict.items():
            for i in range(math.floor(len(self.updated_fauna_dict[species]) / 2)):
                animal = animals[i]
                # print(len(animals))

                if animal.proba_animal_birth(len(animals)):
                    child_species = animal.__class__
                    child = child_species()
                    animal.weight_update_after_birth(child)

                    if animal.gives_birth:
                        self.updated_fauna_dict[species].append(child)
                        animal.gives_birth = True

    def new_animal_gives_birth(self):
        length = len(self.fauna_dict["Herbivore"])
        newborn_list = []
        if length >=2:
            for anim in self.fauna_dict["Herbivore"]:
                if anim.proba_animal_birth():
                    newherb = Herbivore()
                    if self.params['xi'] * newherb.weight <= self.weight:
                        self.weight -= self._params['xi'] * new_animal.weight

                    newborn_list.append(newherb)

    def add_children_to_adult_animals(self):
        """
        After the breeding season, new babies are added to cell animals dictionary and remove it
        from the baby fauna dictionary.
        """
        self.updated_fauna_dict = self.fauna_dict

    def animal_dies(self):
        """"
        If the generated random number is greater than the probability of death, we remove
        the animal from the dictionary
        """
        for species, animals in self.fauna_dict.items():
            for animal in animals:
                if animal.death_probability:
                    self.remove_animal(animal)


    @property
    def cell_fauna_count(self):
        """ Returns the number of fauna type as a dictionary"""
        herb_count = len(self.fauna_dict['Herbivore'])
        # carn_count = len(self.fauna_dict['Carnivore'])
        return {"Herbivore": herb_count}

    def total_herbivore_weight(self):  # not needed before we introduce carnivores
        pass

    @classmethod
    def set_parameters(cls, given_params):
        for param in given_params:
            if param in cls.parameters:
                cls.parameters[param] = given_params[param]
            else:
                raise ValueError('Parameter not set in list' + str(param))


class Water(Landscape):
    # is_migratable = False

    def __init__(self):
        super().__init__()


class Desert(Landscape):
    # is_migratable = True
    parameters = {'f_max': 0}

    def __init__(self, given_params=None):
        super().__init__()
        if given_params is not None:
            self.set_parameters(given_params)
        self.parameters = Highland.parameters
        self.remaining_food['Herbivore'] = self.parameters[
            'f_max']  # self.remaining_food['Carnivore'] = sum(herb.weight for herb in  # self.fauna_list['Herbivore'])

    def update_fodder(self):
        """
        Updates the annual fodder value back to f_max annually
        """  # self.remaining_food["Carnivore"]=


class Highland(Landscape):
    """
    Represents the highland covered by highland cells. Every year the available fodder
    is set to the maximum
    """
    # is_migratable = True
    parameters = {'f_max': 300}

    def __init__(self, given_params=None):
        super().__init__()
        if given_params is not None:
            self.set_parameters(given_params)
        self.parameters = Highland.parameters
        self.remaining_food['Herbivore'] = self.parameters[
            'f_max']  # self.remaining_food['Carnivore']=

    def update_fodder(self):
        """
        Updates the annual fodder value back to f_max annually
        """
        self.remaining_food["Herbivore"] = self.parameters["f_max"]


class Lowland(Landscape):
    """ Represents the landscape covered by lowland cells.  Every year the available fodder
    is set to maximum"""
    # is_migratable = True
    parameters = {'f_max': 800}

    def __init__(self, given_params=None):
        super().__init__()
        if given_params is not None:
            self.set_parameters(given_params)
        self.parameters = Lowland.parameters
        self.remaining_food['Herbivore'] = self.parameters[
            'f_max']  # self.remaining_food['Carnivore']=

    def update_fodder(self):
        """
        Updates the annual fodder value back to f_max annually
        """
        self.remaining_food["Herbivore"] = self.parameters["f_max"]


if __name__ == "__main__":
    print(np.random.shuffle(["a", "b", "c"]))
