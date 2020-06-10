import pytest

from biosim.landscape import Landscape, Lowland, Water, Highland, Desert
from biosim.fauna import Herbivore


class TestLandscape:

    @pytest.fixture(autouse = True)
    def animal_objects(self):
        self.herb1 = Herbivore()
        self.herb2 = Herbivore()
        print(self.herb1.weight, self.herb2.weight)
        return self.herb1, self.herb2

    @pytest.fixture
    def landscape_data(self, animal_objects):
        self.herb1, self.herb2 = animal_objects
        animals = {'Herbivore': [self.herb1, self.herb2]}
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
        lowland.remove_animal(self.herb1)
        assert len(lowland.fauna_dict['Herbivore']) == 1

    def test_herbivore_eats_in_lowland(self, landscape_data):
        lowland = landscape_data['L']
        self.herb1 = lowland.fauna_dict['Herbivore'][0]
        herb1_weight_before_eat = self.herb1.weight
        lowland.animal_eats()
        herb1_weight_after_eat = self.herb1.weight
        assert herb1_weight_after_eat >= herb1_weight_before_eat
