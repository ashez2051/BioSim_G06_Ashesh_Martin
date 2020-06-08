import pytest

from biosim.landscape import Landscape, Lowland
from biosim.fauna import Herbivore


class TestLandscape:

    @pytest.fixture
    def animal_objects(self):
        herb1 = Herbivore()
        herb2 = Herbivore()
        print(herb1.weight, herb2.weight)
        return herb1, herb2

    @pytest.fixture
    def landscape_data(self, animal_objects):
        herb1, herb2 = animal_objects
        animals = {'Herbivore': [herb1, herb2]}
        landscapes_dict = {'W': Water(), 'H': Highland(), 'L': Lowland(), 'D': Desert()}
        for species, animals in animals.items():
            for animal in animals:
                landscapes_dict['L'].add_animal(animal)
                landscapes_dict['D'].add_animal(animal)
                landscapes_dict['H'].add_animal(animal)
        return landscapes_dict

    def test_add_animals(self, landscape_data):
        lowland = landscape_data["L"]
        assert len(lowland.fauna_dict['Herbivore']) == 2
        herb3 = Herbivore()
        lowland.add_animal(herb3)
        assert len(lowland.fauna_dict['Herbivore']) == 3

    def test_remove_animals(self, landscape_data):
        lowland = landscape_data["L"]
        assert len(lowland.fauna_dict['Herbivore']) == 2
        lowland.remove_animal(herb1)
        assert len(lowland.fauna_dict['Herbivore']) == 1

    def test_herbivore_eats_in_lowland(self, landscape_data):
        lowland = landscape_data['L']
        herb1 = lowland.fauna_dict['Herbivore']
        herb1_weight_before_eat = herb1.weight
        lowland.animal_eats()
        herb1_weight_after_eat = herb1.weight
        assert herb1_weight_after_eat >= herb1_weight_before_eat






