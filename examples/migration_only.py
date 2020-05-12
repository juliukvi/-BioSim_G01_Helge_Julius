# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim


if __name__ == "__main__":
    plt.ion()

    geogr = """\
               OOOOOOOOO
               ODDDDDDDO
               ODDDDDDDO
               ODDDDDDDO
               ODDDDDDDO
               ODDDDDDDO
               ODDDDDDDO
               ODDDDDDDO
               OOOOOOOOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (4, 4),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 50}
                for _ in range(1000)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (4, 4),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 50}
                for _ in range(1000)
            ],
        }
    ]

    sim = BioSim(
        island_map=geogr,
        ini_pop=ini_herbs,
        seed=123456,
        img_base="..\\..\\Exam\\dv",
        cmax_animals={"Herbivore": 100, "Carnivore": 50},
    )

    sim.set_animal_parameters(
        "Herbivore", {"mu": 1, "omega": 0, "gamma": 0, "a_half": 1000}
    )
    sim.set_animal_parameters(
        "Carnivore", {"mu": 1, "omega": 0, "gamma": 0, "F": 0, "a_half": 1000}
    )

    sim.set_landscape_parameters("J", {"f_max": 700})
    sim._img_pause_time = 1
    sim.simulate(num_years=10, vis_years=1)
    sim.make_movie()
    sim.make_movie(movie_fmt="gif")
    # sim.add_population(population=ini_carns)
    # sim.simulate(num_years=100, vis_years=1, img_years=2000)

    # plt.savefig("check_sim.pdf")

    # input("Press ENTER")
