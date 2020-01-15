# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

"""
Compatibility check for BioSim simulations.

This script shall function with biosim packages written for
the INF200 project January 2019.
"""

__author__ = "Hans Ekkehard Plesser, NMBU"
__email__ = "hans.ekkehard.plesser@nmbu.no"


if __name__ == "__main__":
    plt.ion()

    geogr = """\
               OOOOOOOOOO
               OJJJJJJJJO
               OJJJJJJJOO
               OOOOOOOOOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ]

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456)

    sim.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
    sim.set_animal_parameters(
        "Carnivore",
        {
            "a_half": 70,
            "phi_age": 0.5,
            "omega": 0.3,
            "F": 65,
            "DeltaPhiMax": 9.0,
        },
    )
    sim.set_landscape_parameters("J", {"f_max": 700})
    print(sim.num_animals)
    print(sim.num_animals_per_species)
    sim.simulate(num_years=100, vis_years=None, img_years=2000)
    print(sim.num_animals)
    print(sim.num_animals_per_species)
    sim.add_population(population=ini_carns)
    print(sim.num_animals)
    print(sim.num_animals_per_species)
    sim.simulate(num_years=100, vis_years=None, img_years=2000)
    print(sim.num_animals)
    print(sim.num_animals_per_species)


