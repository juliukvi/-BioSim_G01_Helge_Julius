# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal, Adam Julius Olof Kviman'
__email__ = 'hegkleme@nmbu.no, juliukvi@nmbu.no'

import pytest
from biosim.simulation import BioSim
import glob
import os
import os.path

def test_simulation_set_animal_parameters():
    """Test to see that incorrect species string gives ValueError"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1)
    with pytest.raises(ValueError):
        sim.set_animal_parameters("Omnivore", {"w_birth": 8.0})

def test_simulation_set_landscape_parameters():
    """Test to see that incorrect landscape string gives ValueError"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1)
    with pytest.raises(ValueError):
        sim.set_landscape_parameters("D", {"fodder": 8.0})

def test_simulation_make_movie_no_base():
    """Test to see that trying to create movies with no img_base raises
    RuntimeError"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1)
    sim.simulate(5, 1)
    with pytest.raises(RuntimeError):
        sim.make_movie()

@pytest.fixture
def figfile_root():
    """Provide name for figfile root and delete figfiles after test completes"""

    ffroot = os.path.join(".", "data\dv")
    yield ffroot
    for f in glob.glob(ffroot + "_0*.png"):
        os.remove(f)


def test_simulation_make_movie_mp4(figfile_root):
    """Test to see that movie can be made with mp4 format"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1, img_base=figfile_root)
    sim.simulate(5, 1)
    sim.make_movie()
    assert os.path.isfile(figfile_root + ".mp4")


def test_simulation_make_movie_gif(figfile_root):
    """Test to see that movie can be made with gif format"""
    sim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1, img_base=figfile_root)
    sim.simulate(5, 1)
    sim.make_movie(movie_fmt="gif")
    assert os.path.isfile(figfile_root + ".gif")


def test_simulation_large_island():
    """Test to see that a island with column or row length bigger than 23
    initialize self._large_island.
    """
    map = """\
               OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
               ODDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDO
               ODDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDO
               ODDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDO
               ODDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDO
               ODDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDO
               ODDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDO
               ODDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDO
               OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"""
    sim = BioSim(island_map=map,  ini_pop=[], seed=1)
    sim.simulate(1, 1)
    assert sim._large_island