import pytest

from biosim.landscape import Landscape, Lowland, Water, Highland, Desert
from biosim.fauna import Herbivore, Carnivore


class TestLandscape:

    @pytest.fixture(autouse=True)
    def animal_objects(self):
        self.herb1 = Herbivore(10, 50)
        self.herb2 = Herbivore(20, 35)
        self.carn1 = Carnivore(5, 50)
        self.carn2 = Carnivore(20, 40)
        return self.herb1, self.herb2, self.carn1, self.carn2

    @pytest.fixture
    def landscape_data(self, animal_objects):
        herb1, herb2, carn1, carn2 = animal_objects
        animals = {'Herbivore': [herb1, herb2], 'Carnivore': [carn1, carn2]}

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
        assert herb1_weight_after_eat > herb1_weight_before_eat

    def test_carnivore_eats_herbivore_in_lowland(self, landscape_data):
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        weight_before = self.carn1.weight
        self.carn1 = lowland.fauna_dict["Carnivore"][0]
        lowland.animal_eats()
        # print("herb", self.herb1.animal_fitness)
        # print("carn", self.carn1.animal_fitness)
        assert self.carn1.weight >= weight_before  ### Ask for help


    def test_place_carn_and_herb_in_cell(self, landscape_data):
        lowland = landscape_data["L"]
        count = lowland.cell_fauna_count
        assert count['Herbivore'] == 2 and count["Carnivore"] == 2

    def test_animals_cannot_migrate_in_water(self):
        pass

    def test_herbivore_doesnt_eat_in_the_desert(self, landscape_data):
        desert = landscape_data["D"]
        self.herb1 = desert.fauna_dict['Herbivore'][0]
        herb1_weight_before_eat = self.herb1.weight
        herb1_fitness_before_eat = self.herb1.animal_fitness
        desert.animal_eats()
        herb1_weight_after_eat = self.herb1.weight
        herb1_fitness_after_eat = self.herb1.animal_fitness

        assert herb1_weight_after_eat == herb1_weight_before_eat
        assert herb1_fitness_after_eat == herb1_fitness_before_eat

    def test_place_carn_in_cell_without_food(self, landscape_data):
        """
        Check if they all die
        """
        highland = landscape_data["H"]
        self.carn1 = highland.fauna_dict["Carnivore"][0]
        weight_before = self.carn1.weight
        highland.animal_eats()
        weight_after = self.carn1.weight
        assert weight_before == weight_after

    def test_equal_probability_of_migration_to_each_cell(self):
        pass

    def test_resets_fodder_each_year(self, landscape_data):
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        for _ in range(10):
            lowland.animal_eats()
            lowland.update_fodder()
        assert lowland.remaining_food["Herbivore"] == 800

    def test_animal_count_reduces_when_animal_dies(self, landscape_data):
        """
        This test might not pass always because of the probability 
        """""
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        # self.herb2 = lowland.fauna_dict["Herbivore"][1]
        # self.carn1 = lowland.fauna_dict["Carnivore"][0]
        # self.carn2 = lowland.fauna_dict["Carnivore"][1]
        initial_herb_count = lowland.cell_fauna_count['Herbivore']
        herb1.set_parameter
        # initial_carn_count = lowland.cell_fauna_count["Carnivore"]
        for _ in range(10):
            lowland.carnivore_eats()
            lowland.animal_dies()
        assert lowland.cell_fauna_count["Herbivore"] == 0
        assert lowland.cell_fauna_count["Carnivore"] == 2  ### Ask help

    def test_animal_count_increases_when_animal_is_born(self, landscape_data):
        lowland = landscape_data["L"]
        self.herb1 = lowland.fauna_dict["Herbivore"][0]
        self.herb2 = lowland.fauna_dict["Herbivore"][1]
        initial_count = lowland.cell_fauna_count["Herbivore"]
        lowland.animal_gives_birth()
        lowland.add_children_to_adult_animals()
        assert initial_count < lowland.cell_fauna_count["Herbivore"]  ### Ask for help

    def test_calculation_of_total_herbivore_weight(self):
        pass

    def test_remaining_food_for_herbs_is_correctly_calculated(self):
        pass

    # Statistical tests
    # Things that has to do with probability

    def test_sort_by_fitness_herb(self, landscape_data):
        lowland = landscape_data['L']
        lowland.sort_by_fitness()
        herb1 = lowland.fauna_dict['Herbivore'][0]
        herb2 = lowland.fauna_dict['Herbivore'][1]
        assert herb1.animal_fitness < herb2.animal_fitness

    def test_sort_by_fitness_carn(self, landscape_data):
        lowland = landscape_data['L']
        lowland.sort_by_fitness()
        carn1 = lowland.fauna_dict['Carnivore'][0]
        carn2 = lowland.fauna_dict['Carnivore'][1]
        assert carn1.animal_fitness > carn2.animal_fitness

    def test_animal_migrates_maximum_once_per_year(self):
        pass

    def test_carnivore_eats_least_fit_herbivore(self):
        pass

    class TestWater:
        @pytest.fixture
        def water(self):
            return Water()

        def test_initiate_water(self, water):
            assert water

        def test_water_not_migratable(self, water):
            assert water.is_migratable is False

        def test_water_food_available(self, water):
            with pytest.raises(ValueError):
                water.remaining_food()

    class TestDesert:
        @pytest.fixture
        def desert(self):
            return Desert()

        def test_initiate_mountain(self, desert):
            assert desert

        def test_desert_not_migratable(self, desert):
            assert desert.is_migratable is True

        def test_desert_food_available(self, desert):
            assert desert.remaining_food['Herbivore'] == 0
            assert desert.remaining_food['Carnivore'] == desert.total_herbivore_weight
