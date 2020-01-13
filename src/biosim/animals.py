# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal, Adam Julius Olof Kviman'
__email__ = 'hegkleme@nmbu.no, juliukvi@nmbu.no'
import math as m
import random
import numpy as np


class Animal:
    """Animal which lives on an island. Parent class for different animal types

    Parameters
    ----------
    age: int
        Initial age of the animal
    weight: float
        Initial weight of the animal

    Raises
    ------
    ValueError
        If age is below 0 or if weight is below, 0 or None.
    Attributes
    ----------
    fitness: int
        Value describing the animals fitness
    age: int
        Initial age of the animal which can't be assigned a value below 0
    weight: float
         Weight drawn from the Gaussian distribution if not assigned a value

    """
    def __init__(self, age=0, weight=None):
        self.fitness = 0
        if age < 0:
            raise ValueError("Animal age cant be below 0")
        if weight and weight <= 0:
            raise ValueError("Animal weight cant be less than or equal to 0")
        self.a = age
        self.weight = weight
        if not self.weight:
            placeholder = -1000
            while placeholder < 0:
                placeholder = np.random.normal(self.w_birth, self.sigma_birth)
                self.weight = placeholder
        self.fitness_update()

    def fitness_update(self):
        """Updates the animals fitness value
        """
        if self.weight <= 0:
            self.fitness = 0
        else:
            q_age = 1 / (1 + m.exp(self.phi_age * (self.a - self.a_half)))
            q_weight = 1 / (1 + m.exp(-self.phi_age*(self.weight - self.w_half)))
            self.fitness = q_age * q_weight

    def migrate(self):
        """Estimates the probability for an animal to migrate

        Returns
        -------
        bool
            Returns True if the animal migrates, false if not
        """
        number = random.uniform(0, 1)
        return number <= (self.mu * self.fitness)

    def will_birth(self, num_animal):
        """Determines if an animal will give birth or not

        Returns
        -------
        Nonetype
            If the animal doesnt give birth
        __main__Animal??
            If the animal gives birth
        """
        prob = min(1, self.gamma * self.fitness * (num_animal-1))
        number = random.uniform(0, 1)
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return
        if number <= prob:
            newborn = self.birth()
            if (self.xi * newborn.weight) > self.weight:
                return
            self.weight -= (self.xi * newborn.weight)
            self.fitness_update()
            return newborn
        else:
            return


    def age(self):
        """Ages the animal by one year
        """
        self.a += 1

    def weightloss(self):
        """Updates the weight of the animal according to formula:

           :math: w = w \cdot(1-\eta)

        """
        self.weight -= self.eta * self.weight

    def death(self):
        """

        Returns
        -------
        bool
            Returns True if the animal dies, false if not
        """
        if self.fitness == 0:
            return True
        prob = self.omega * (1 - self.fitness)
        number = random.uniform(0, 1)
        if number <= prob:
            return True
        else:
            return False

class Carn(Animal):
    """Carnivore species which lives on the island. Subclass of Animal class.
    Parameters
    ----------
    age: int
        Initial age of the animal
    weight: float
        Initial weight of the animal
    are_params_set: bool
        True if the
    Raises
    ------
    ValueError
        If age is below 0 or if weight is below, 0 or None.
    Attributes
    ----------
    fitness: int
        Value describing the animals fitness
    age: int
        Initial age of the animal which can't be assigned a value below 0
    weight: float
         Weight drawn from the Gaussian distribution if not assigned a value
    standard_parameters: dict
        Values that determines the behaviour of the animal
    """
    #Gi nytt navn parameters? Denne oppdateres av set_parameters.
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
        """Updates the standard_parameters dictionary with new values.

        Parameters
        ----------
        new_params: dict
            Dictionary containing key(s) that exist in standard_parameters
            The dict is on the form:
                {
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
        Raises
        ------
        KeyError
            If the key in new_params does not exist in standard_parameters
        ValueError
            If the new value assigned to key is not of type float or int
        """
        for key in new_params:
            if key not in cls.standard_parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
            if isinstance(new_params[key], int) or isinstance(new_params[key], float):
                continue
            else:
                raise ValueError(f'Value needs to be int or float, got:{type(new_params[key]).__name__}')
        cls.standard_parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        """Sets the standard_parameters as attributes on a class level
        """
        for key in cls.standard_parameters:
            #Setting a new attribute name for lambda
            if key == "lambda":
                new_key ="_lambda"
                setattr(cls, new_key, cls.standard_parameters[key])
            else:
                setattr(cls, key, cls.standard_parameters[key])
        cls.are_params_set = True

    def __init__(self, age=0, weight=None):
        if not self.are_params_set:
            self._set_params_as_attributes()
        super().__init__(age=age, weight=weight)

    def __repr__(self):
        return "Carnivore(age={}, weight={})".format(self.a, self.weight)


    def feeding(self, sorted_herb_list):
        """Handles the eating and weight of the carnivores
        This function also handles the killing of herbivores by carnivores
        when they eat.
        Parameters
        ----------
        sorted_herb_list: list
            List of herbivores sorted in order of fitness
        The carnivores kill the herbivores with a probability:
        :math:
            \documentclass{article}
            \usepackage{amsmath}
            \begin{document}
            \begin{equation}
                 p =
                  \begin{cases}
                   0 & \text{if \phi_{carn} \leq \phi_{herb}\\
                   2 & \text{if bank $i$ issues CBs at time $t$}\\
                   0 & \text{otherwise}
                  \end{cases}
            \end{equation}
            \end{document}
        """
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
            if number <= chance_to_kill:
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
        """Static method that returns a new carnivore class instance.
        Returns
        -------
        __main__Carn
            A new class instance of the carnivore class
        """
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
            if isinstance(new_params[key], int) or isinstance(new_params[key], float):
                continue
            else:
                raise ValueError('Value needs to be int or float, got' + str(type(new_params[key])))
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