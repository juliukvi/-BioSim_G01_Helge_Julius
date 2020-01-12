# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'

import textwrap
from biosim.animals import Herb



class Nature:
    def __init__(self):
        self.color = None
        self.fodder = 0
        self.habitable = True
        self.herb_list = []
        self.carn_list = []

    def feed_all_animals(self):
        self.fodder = self.fodder_update()
        self.herb_list.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.herb_list:
            if self.fodder > 0:
                self.fodder -= animal.feeding(self.fodder)

    def birth_all_animals(self):
        if self.herb_list >= 2:
            for animal in self.herb_list:
                if animal.will_birth(len(self.herb_list)):
                    self.herb_list.append(animal.birth())

    def aging_all_animals(self):
        for animal in self.herb_list:
            animal.age()

    def weightloss_all_animals(self):
        for animal in self.herb_list:
            animal.weightloss()

    def death_all_animals(self):
        self.herb_list = [
            animal for animal in self.herb_list if not animal.death()
        ]


class Ocean(Nature):
    def __init__(self):
        super().__init__()
        self.habitable = False


class Mountain(Nature):
    def __init__(self):
        super().__init__()
        self.habitable = False


class Desert(Nature):
    def __init__(self):
        super().__init__()


class Savannah(Nature):
    standard_parameters = {"f_max": 300, "alpha": 0.3}
    are_params_set = False
    @classmethod
    def set_parameters(cls, new_params):
        for key in new_params:
            if key not in cls.standard_parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
        cls.standard_parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        for key in cls.standard_parameters:
            setattr(cls, key, cls.standard_parameters[key])
        cls.are_params_set = True

    def __init__(self):
        super().__init__()
        if not self.are_params_set:
            self._set_params_as_attributes()
        self.fodder = self.f_max

    def fodder_update(self):
        self.fodder = self.fodder + self.alpha * (self.f_max - self.fodder)




class Jungle(Nature):
    standard_parameters = {"f_max": 800}
    are_params_set = False

    @classmethod
    def set_parameters(cls, new_params):
        for key in new_params:
            if key not in cls.standard_parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
        cls.standard_parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        for key in cls.standard_parameters:
            setattr(cls, key, cls.standard_parameters[key])
        cls.are_params_set = True

    def __init__(self):
        if not self.are_params_set:
            self._set_params_as_attributes()
        super().__init__()
        self.fodder = self.f_max

    def fodder_update(self):
        self.fodder = self.f_max

