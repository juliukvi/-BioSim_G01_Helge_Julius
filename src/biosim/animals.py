# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal, Adam Julius Olof Kviman'
__email__ = 'hegkleme@nmbu.no, juliukvi@nmbu.no'
import math as m
import random
import numpy as np

class Animal:

    def __init__(self, age=0, weight=None):
        self.fitness = 0
        if age < 0:
            raise ValueError("animal age cant be below 0")
        if weight and weight <= 0:
            raise ValueError("animal weight cant be less than or equal to 0")
        self.a = age
        self.weight = weight
        # If weight=None, a positive weight from gauisian distrobution is given
        if not self.weight:
            placeholder = -1000
            while placeholder < 0:
                placeholder = np.random.normal(self.w_birth, self.sigma_birth)
                self.weight = placeholder
        self.fitness_update()

    def fitness_update(self):
        if self.weight <= 0:
            self.fitness = 0
        else:
            q_age = 1 / (1 + m.exp(self.phi_age * (self.a - self.a_half)))
            q_weight = 1 / (1 + m.exp(-self.phi_age*(self.weight - self.w_half)))
            self.fitness = q_age * q_weight

    def migrate(self):
        number = random.uniform(0, 1)
        return number < (self.mu * self.fitness)

    def will_birth(self, num_animal):
        prob = min(1, self.gamma * self.fitness * (num_animal-1))
        number = random.uniform(0, 1)
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return False
        if number <= prob:
            newborn = self.birth()
            if (self.xi * newborn.weight) > self.weight:
                return False
            self.weight -= (self.xi * newborn.weight)
            self.fitness_update()
            return newborn
        else:
            return


    def age(self):
        self.a += 1

    def weightloss(self):
        self.weight -= self.eta * self.weight

    def death(self):
        if self.fitness == 0:
            return True
        prob = self.omega * (1 - self.fitness)
        number = random.uniform(0, 1)
        if number <= prob:
            return True
        else:
            return False

class Carn(Animal):
    standard_parameters = {
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 60.0,
        "phi_age": 0.4,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "lambda": 1.0,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.9,
        "F": 50.0,
        "DeltaPhiMax": 10.0
    }
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
            if key == "lambda":
                new_key ="_lambda"
                setattr(cls, new_key, cls.standard_parameters[key])
            else:
                setattr(cls, key, cls.standard_parameters[key])
        cls.are_params_set = True

    def __init__(self, age=0, weight=None ):
        if not self.are_params_set:
            self._set_params_as_attributes()
        super().__init__(age=age, weight=weight)

    def __repr__(self):
        return "Carnivore(age={}, weight={})".format(self.a, self.weight)


    def feeding(self, sorted_herb_list):
        amount_to_eat = self.F
        for herb in reversed(sorted_herb_list):
            if amount_to_eat <= 0:
                break #Stop eating if carnivore is full
            fitness_diff = (self.fitness - herb.fitness)
            if fitness_diff < 0:
                break
            elif fitness_diff < self.DeltaPhiMax:
                chance_to_kill = fitness_diff/self.DeltaPhiMax
            else:
                chance_to_kill = 1
            number = random.uniform(0, 1)
            if number < chance_to_kill:
                if herb.weight > amount_to_eat:
                    self.weight += self.beta * amount_to_eat
                    self.fitness_update()
                    sorted_herb_list.remove(herb)
                    break
            self.weight += self.beta * herb.weight
            amount_to_eat -= herb.weight
            self.fitness_update()
            sorted_herb_list.remove(herb)

    @staticmethod
    def birth():
        return Carn()

class Herb(Animal):
    standard_parameters = {
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.2,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "lambda": 1.0,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
    }
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
            if key == "lambda":
                new_key ="_lambda"
                setattr(cls, new_key, cls.standard_parameters[key])
            else:
                setattr(cls, key, cls.standard_parameters[key])
        cls.are_params_set = True

    def __init__(self, age=0, weight=None ):
        if not self.are_params_set:
            self._set_params_as_attributes()
        super().__init__(age=age, weight=weight)

    def __repr__(self):
        return "Herbivore(age={}, weight={})".format(self.a, self.weight)

    def feeding(self, fodder):
        if fodder > self.F:
            self.weight += self.beta * self.F
            return self.F
        elif (fodder > 0) and (fodder < self.F):
            self.weight += self.beta * fodder
            return fodder
        if fodder < 0:
            raise ValueError("Cannot have negative fodder value")
    @staticmethod
    def birth():
        return Herb()