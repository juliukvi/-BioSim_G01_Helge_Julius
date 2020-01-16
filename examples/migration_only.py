# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim





if __name__ == "__main__":
    plt.ion()

    geogr = """\
               OOOOOOO
               OJJJJJO
               OJJJJJO
               OJJJJJO
               OOOOOOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (2, 3),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 50}
                for _ in range(500)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (2, 3),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(500)
            ],
        }
    ]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456, cmax_animals={"Herbivore":50, "Carnivore": 50 })

    sim.set_animal_parameters('Herbivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'a_half': 1000})
    sim.set_animal_parameters('Carnivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'F': 20, 'a_half': 1000})

    sim.set_landscape_parameters("J", {"f_max": 700})
    sim._img_pause_time = 2
    sim.simulate(num_years=2, vis_years=1, img_years=2000)

    sim.add_population(population=ini_carns)
    #sim.simulate(num_years=100, vis_years=1, img_years=2000)

    plt.savefig("check_sim.pdf")

    input("Press ENTER")
