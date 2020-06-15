from biosim.island import Island
import numpy as np

np.random.seed(1)

if __name__ == "__main__":
    ini_herbs = [{'loc': (1, 1),
                  'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20} for _ in range(100)]}]

    geogr = """\
    WWWW
    WLHW
    WWWW"""

    i = Island(geogr)
    i.convert_string_to_array()
    bb = i.array_with_landscape_objects()
    i.add_animals(ini_herbs)

    num_herb = []
    num_herb2 = []

    for year in range(10):
        # print(year)
        cells = i.cells()
        i.life_cycle_in_rossumoya()

        num_herb.append(cells[1, 1].cell_fauna_count['Herbivore'])

        num_herb2.append(cells[1, 2].cell_fauna_count['Herbivore'])

    print("herb, ", num_herb)
    print("herb", num_herb2)
