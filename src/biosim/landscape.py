# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'

import textwrap
from biosim.animals import Herb
import math as m
import random


class Nature:
    def __init__(self):
        self.fodder = 0
        self.habitable = True
        self.herb_list = []
        self.carn_list = []

    def feed_all_animals(self):
        self.herb_list.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.herb_list:
            if self.fodder > 0:
                self.fodder -= animal.feeding(self.fodder)
        self.carn_list.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.carn_list:
            animal.feeding(self.herb_list)


    def birth_all_animals(self):
        if len(self.herb_list) >= 2:
            num_animal = len(self.herb_list)
            for animal in self.herb_list:
                newborn = animal.will_birth(num_animal)
                if animal.will_birth(num_animal):
                    self.herb_list.append(animal.birth())
        if len(self.carn_list) >= 2:
            num_animal = len(self.carn_list)
            for animal in self.carn_list:
                if animal.will_birth(num_animal):
                    self.carn_list.append(animal.birth())

    def migrate_all_animals(self, neighbors):
        for animal in self.herb_list:
            if animal.migrate():
                north_nature_square = neighbors[0]
                east_nature_square = neighbors[1]
                south_nature_square = neighbors[2]
                west_nature_square = neighbors[3]
                north_relative_abundance = (north_nature_square.fodder)/((len(north_nature_square.herb_list)+1)*animal.F)
                east_relative_abundance =  (east_nature_square.fodder)/((len(east_nature_square.herb_list)+1)*animal.F)
                south_relative_abundance = (south_nature_square.fodder)/((len(south_nature_square.herb_list)+1)*animal.F)
                west_relative_abundance = (west_nature_square.fodder)/((len(west_nature_square.herb_list)+1)*animal.F)
                if north_nature_square.habitable:
                    north_propensity = m.exp(animal._lambda*north_relative_abundance)
                else:
                    north_propensity = 0
                if east_nature_square.habitable:
                    east_propensity = m.exp(animal._lambda*east_relative_abundance)
                else:
                    east_propensity = 0
                if south_nature_square.habitable:
                    south_propensity = m.exp(animal._lambda*south_relative_abundance)
                else:
                    south_propensity = 0
                if west_nature_square.habitable:
                    west_propensity = m.exp(animal._lambda*west_relative_abundance)
                else:
                    west_propensity = 0
                total_propensity = (north_propensity+east_propensity+south_propensity+west_propensity)
                north_move_prob = north_propensity/total_propensity
                east_move_prob = north_move_prob + east_propensity/total_propensity
                south_move_prob = east_move_prob + south_propensity/total_propensity
                west_move_prob = south_move_prob + west_propensity/total_propensity
                number = random.uniform(0, 1)
                if number < north_move_prob:
                    north_nature_square.herb_list.append(animal)
                    self.herb_list.remove(animal)
                if number < east_move_prob:
                    east_nature_square.herb_list.append(animal)
                    self.herb_list.remove(animal)
                if number < south_move_prob:
                    south_nature_square.herb_list.append(animal)
                    self.herb_list.remove(animal)
                if number < west_move_prob:
                    west_nature_square.herb_list.append(animal)
                    self.herb_list.remove(animal)

        for animal in self.carn_list:
            if animal.migrate():
                north_nature_square = neighbors[0]
                east_nature_square = neighbors[1]
                south_nature_square = neighbors[2]
                west_nature_square = neighbors[3]
                north_herb_weight = sum([herb.weight for herb in north_nature_square.herb_list])
                east_herb_weight = sum([herb.weight for herb in east_nature_square.herb_list])
                south_herb_weight = sum([herb.weight for herb in south_nature_square.herb_list])
                west_herb_weight = sum([herb.weight for herb in west_nature_square.herb_list])

                north_relative_abundance = (north_herb_weight) / (
                            (len(north_nature_square.carn_list) + 1) * animal.F)
                east_relative_abundance = (east_herb_weight) / (
                            (len(east_nature_square.carn_list) + 1) * animal.F)
                south_relative_abundance = (south_herb_weight) / (
                            (len(south_nature_square.carn_list) + 1) * animal.F)
                west_relative_abundance = (west_herb_weight) / (
                            (len(west_nature_square.carn_list) + 1) * animal.F)
                if north_nature_square.habitable:
                    north_propensity = m.exp(animal._lambda * north_relative_abundance)
                else:
                    north_propensity = 0
                if east_nature_square.habitable:
                    east_propensity = m.exp(animal._lambda *east_relative_abundance)
                else:
                    east_propensity = 0
                if south_nature_square.habitable:
                    south_propensity = m.exp(animal._lambda *south_relative_abundance)
                else:
                    south_propensity = 0
                if west_nature_square.habitable:
                    west_propensity = m.exp(animal._lambda *west_relative_abundance)
                else:
                    west_propensity = 0
                total_propensity = (north_propensity + east_propensity + south_propensity + west_propensity)
                north_move_prob = north_propensity / total_propensity
                east_move_prob = north_move_prob + east_propensity / total_propensity
                south_move_prob = east_move_prob + south_propensity / total_propensity
                west_move_prob = south_move_prob + west_propensity / total_propensity
                number = random.uniform(0, 1)
                if number < north_move_prob:
                    north_nature_square.carn_list.append(animal)
                    self.carn_list.remove(animal)
                if number < east_move_prob:
                    east_nature_square.carn_list.append(animal)
                    self.carn_list.remove(animal)
                if number < south_move_prob:
                    south_nature_square.carn_list.append(animal)
                    self.carn_list.remove(animal)
                if number < west_move_prob:
                    west_nature_square.carn_list.append(animal)
                    self.carn_list.remove(animal)


    def aging_all_animals(self):
        for animal in self.herb_list:
            animal.age()
            animal.fitness_update()
        for animal in self.carn_list:
            animal.age()
            animal.fitness_update()

    def fodder_update(self):
        pass

    def weightloss_all_animals(self):
        for animal in self.herb_list:
            animal.weightloss()
            animal.fitness_update()
        for animal in self.carn_list:
            animal.weightloss()
            animal.fitness_update()

    def death_all_animals(self):
        self.herb_list = [
            animal for animal in self.herb_list if not animal.death()
        ]
        self.carn_list = [
            animal for animal in self.carn_list if not animal.death()
        ]

    def herbivore_number(self):
        return len(self.herb_list)

    def carnivore_number(self):
        return len(self.carn_list)

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
        if not self.are_params_set:
            self._set_params_as_attributes()
        super().__init__()
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


