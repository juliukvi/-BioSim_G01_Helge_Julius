# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'
from biosim.landscape import *

def test_ocean():
    O = Ocean()
    assert O.habitable == False
    assert O.fodder == 0

def test_mountain():
    M = Mountain()
    assert M.habitable == False


def test_desert():
    D = Desert()
    assert D.habitable == True

def test_savannah():
    S = Savannah()
    assert S.fodder == 300

    S.eating_rules(10)
    assert S.fodder == 290
    S.fodder = 5
    S.eating_rules(10)
    assert S.fodder == 0

    S.fodder = 150
    S.fodder_update(300, 0.3)
    assert S.fodder == 195



def test_jungle():
    J = Jungle()
    assert J.fodder == 800
    J.eating_rules(10)
    assert J.fodder == 790
    J.fodder = 4
    J.eating_rules(10)
    assert J.fodder == 0

    J.fodder = 300
    J.fodder_update(800)
    assert J.fodder == 800
