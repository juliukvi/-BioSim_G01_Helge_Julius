# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal, Adam Julius Olof Kviman'
__email__ = 'hegkleme@nmbu.no, juliukvi@nmbu.no'

from biosim.island import Island
import pytest
import textwrap

class TestIsland:
    """A test class for the island class.
    """
    @pytest.fixture
    def island_small(self):
        """Creates a fixture of a small island with one jungle square.
        """
        return Island("OOO\nOJO\nOOO")

    @pytest.fixture
    def example_island_big(self):
        """Creates a fixture of a relativly big island.
        """
        geogr = """\
                       OOOOOOOOOOOOOOOOOOOOO
                       OOOOOOOOSMMMMJJJJJJJO
                       OSSSSSJJJJMMJJJJJJJOO
                       OSSSSSSSSSMMJJJJJJOOO
                       OSSSSSJJJJJJJJJJJJOOO
                       OSSSSSJJJDDJJJSJJJOOO
                       OSSJJJJJDDDJJJSSSSOOO
                       OOSSSSJJJDDJJJSOOOOOO
                       OSSSJJJJJDDJJJJJJJOOO
                       OSSSSJJJJDDJJJJOOOOOO
                       OOSSSSJJJJJJJJOOOOOOO
                       OOOSSSSJJJJJJJOOOOOOO
                       OOOOOOOOOOOOOOOOOOOOO"""
        geogr = textwrap.dedent(geogr)
        return Island(geogr)

    def test_initiate_island(self, island_small):
        """Tests that the Island class can be initiated.
        """
        assert isinstance(island_small, Island)

    def test_island_init(self, island_small):
        """Tests that the island attributes are correct.
        """
        assert island_small.map_list != []
        assert island_small.map_columns == 3
        assert island_small.map_rows == 3

    def test_add_population_raises_errors(self, island_small):
        """
        Tests that the island class raises errors if the island map list is
        not correctly indexed, or population is added on non habitable square.
        """
        with pytest.raises(ValueError):
            island_small.add_population([
        {
            "loc": (0, 100),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ])
        with pytest.raises(ValueError):
            island_small.add_population([
        {
            "loc": (100, 0),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ])

        with pytest.raises(ValueError):
            island_small.add_population([
        {
            "loc": (0, 0),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(40)
            ],
        }
    ])

    def test_add_population_raises_error_for_wrong_species(self, island_small):
        """
        Tests that the add_population method raises errors for a wrong
        input animal species.
        """
        with pytest.raises(ValueError):

            island_small.add_population([
        {
            "loc": (2, 9),
            "pop": [
                {"species": "Vulture", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ])
