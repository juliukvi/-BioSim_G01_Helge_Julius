# -*- coding: utf-8 -*-

__author__ = "Helge Helo Klemetsdal, Adam Julius Olof Kviman"
__email__ = "hegkleme@nmbu.no, juliukvi@nmbu.no"
import math as m
import random
import numpy as np


class BaseAnimal:
    """ Baseclass for the animal species which lives on the island.

    Parameters
    ----------
    age: int
        Initial age of the animal.
    weight: float
        Initial weight of the animal.

    Attributes
    ----------
    fitness: int
        Value describing the animals fitness
    a: int
        Initial age of the animal.
    weight: float
         Weight drawn from the Gaussian distribution if not assigned a value.
    parameters : dict
        Values that describe the behaviour of the animals.

    Raises
    ------
    ValueError
        If age is below 0 or if weight is below, 0 or None.

    """

    parameters = None

    @classmethod
    def set_default_parameters_for_species(cls):
        """Sets the species default parameters as attributes on a class level

        This is achieved by copying the subjective DEFAULT_PARAMETERS class,
        and then using the _set_params_as_attributes method to assign them
        as class attributes.
        """
        cls.parameters = cls.DEFAULT_PARAMETERS.copy()
        cls._set_params_as_attributes()

    @classmethod
    def set_parameters(cls, new_params):
        """Updates the parameters for the respective subclass with new values.

        Parameters
        ----------
        new_params: dict
            Dictionary containing key(s) that exist in the DEFAULT_PARAMETERS.
        Raises
        ------
        KeyError
            If the key(s) in new_params does not exist in parameters.
        ValueError
            If the new value assigned to the key(s) is not of type float or int
        ValueError
            If the assigned parameter values are not in the right ranges.
        """

        for key in new_params:
            if key not in cls.parameters.keys():
                raise KeyError(f"Parameter {key} is not valid")
            if isinstance(new_params[key], int) or isinstance(
                new_params[key], float
            ):
                continue
            else:
                raise ValueError(
                    f"Value needs to be int or float, "
                    f"got:{type(new_params[key]).__name__}"
                )
        for key in new_params:
            if new_params[key] < 0:
                raise ValueError("All values must be positive")
            if key == "DeltaPhiMax" and new_params[key] <= 0:
                raise ValueError("DeltaPhiMax must be strictly positive")
            if key == "eta" and new_params[key] > 1:
                raise ValueError("Eta must be less or equal to one")
        cls.parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        """Sets the animal parameters to attributes on class level.
        """
        for key in cls.parameters:
            if key == "lambda":
                new_key = "_lambda"
                setattr(cls, new_key, cls.parameters[key])
            else:
                setattr(cls, key, cls.parameters[key])

    def __init__(self, age=0, weight=None):
        if self.parameters is None:
            self.set_default_parameters_for_species()
        self.fitness = 0
        if not isinstance(age, int):
            raise ValueError("Animal age must be an integer")
        if age < 0:
            raise ValueError("Animal age cant be below 0")
        if (
            weight is None
            or isinstance(weight, int)
            or isinstance(weight, float)
        ):
            pass
        else:
            raise ValueError("Animal weight must be int or float")
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
        r"""Updates the animals fitness value

        The fitness value :math:`\Phi`, is updated by:

        .. math::
            \Phi = 0
        if :math:`\omega \leq 0`,

        .. math::
            q^{+}(a,a_{\frac{1}{2}},\phi_{age})\times
            q^{+}(\omega,\omega_{\frac{1}{2}},\phi_{weight})

        else

        where

        .. math::
            q^{\pm}(x,x_{\frac{1}{2}},\phi) =
            \frac{1}{1 + e^{\pm\phi(x-x_{\frac{1}{2}})}}
        """
        if self.weight <= 0:
            self.fitness = 0
        else:
            q_age = 1 / (1 + m.exp(self.phi_age * (self.a - self.a_half)))
            q_weight = 1 / (
                1 + m.exp(-self.phi_weight * (self.weight - self.w_half))
            )
            self.fitness = q_age * q_weight

    def migrate(self):
        """Estimates the probability for an animal to migrate

        The probability of an animal migrating is given by :math:`\mu\Phi`

        Returns
        -------
        bool
            Returns True if the animal migrates, false if not
        """
        number = random.uniform(0, 1)
        return number <= (self.mu * self.fitness)

    def will_birth(self, num_animal):
        r"""Determines if an animal will give birth or not.

        The probability for an animal to give birth is given by formula:

        .. math::

            min(1, \gamma \times \Phi \times(N-1))

        where N is the number of animals of the same species in the cell
        at the start of the breeding season.
        If there are no animals in the cell the probability is 0.
        The probability will also be zero if:

        .. math::
            \omega < \zeta(\omega_{birth}+\sigma_{birth})

        When a mother gives birth it looses :math:`\xi` times the actual
        birthweight of the baby.

        Returns
        -------
        Nonetype
            If the animal doesnt give birth
        newborn: BaseAnimal
            If the animal gives birth
        """
        prob = min(1, self.gamma * self.fitness * (num_animal - 1))
        number = random.uniform(0, 1)
        if self.weight < (self.zeta * (self.w_birth + self.sigma_birth)):
            return
        if number <= prob:
            newborn = self.birth()
            if self.weight < (self.xi * newborn.weight):
                return
            self.weight -= self.xi * newborn.weight
            self.fitness_update()
            return newborn
        else:
            return

    def age_animal(self):
        """Ages the animal by one year
        """
        self.a += 1

    def weightloss(self):
        r"""Updates the weight of the animal.

        Every year the animals weight decreases by :math:`\eta\omega`

        """
        self.weight -= self.eta * self.weight

    def death(self):
        r"""Estimates if an animal dies or not.

        Death is guaranteed if :math:`\Phi = 0`, and else it occurs with
        probability given by the formula:

        .. math::
            p_{death} = \omega(1-\Phi)

        Returns
        -------
        bool
            Returns True if the animal dies, false if not
        """
        if self.fitness == 0:
            return True
        p_death = self.omega * (1 - self.fitness)
        number = random.uniform(0, 1)
        if number < p_death:
            return True
        else:
            return False

    def birth(self):
        """Returns a new class object of the same species that gave birth

        Returns
        -------
        BaseAnimal
            An instance of the same classtype that gave birth
        """
        return self.__class__()


class Carn(BaseAnimal):
    """Carnivore species which lives on the island.

    The Carn class is a subclass of the BaseAnimal class, and it inherits
    the classmethods and attributes from the parent class by the super()
    function.

    Parameters
    ----------
    age: int
        Initial age of the carnivore.
    weight: float
        Initial weight of the carnivore.

    Attributes
    ----------
    DEFAULT_PARAMETERS : dict
        Default parameters for the carnivore species.
    fitness: int
        Value describing the carnivore's fitness.
    age: int
        Initial age of the carnivore.
    weight: float
         Weight drawn from the Gaussian distribution if not assigned a value.
    parameters: dict
        Values that determines the behaviour of the carnivores.

    Raises
    ------
    ValueError
        If age is below 0 or if weight is below 0, 0 or None.
    """

    DEFAULT_PARAMETERS = {
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
        "DeltaPhiMax": 10.0,
    }

    def __init__(self, age=0, weight=None):
        super().__init__(age=age, weight=weight)

    def feeding(self, sorted_herb_list):
        r"""Feeds a carnivore and updates the weight and fitness accordingly.

        The carnivores prey and feed on herbivores only. The carnivore eats
        by the herbivores order of fitness, i.e., the herbivore with the lowest
        fitness gets eaten first. A carnivore eats from a list of herbivores
        until it's appetite, given by the parameter F, is 0.

        The probability of the carnivore killing a herbivore is given by:

        .. math::
            p = 0

        if :math:`\Phi_{carn} \leq \Phi_{herb}`,

        .. math::
            p = \frac{\Phi_{carn}-\Phi_{herb}}{\Delta\Phi_{max}}

        if :math:`0 < \Phi_{carn}-\Phi_{herb} < \Delta\Phi_{max}`
        and

        .. math::
             p = 1

        otherwise.

        The weight of the carnivore increases by :math:`\beta\omega_{herb}`
        where :math:`\omega_{herb}` is the weight of the herbivore eaten.
        If the weight of the herbivore is greater than the carnivore's
        appetite, the carnivore eats only a part of the
        herbivore and the weight is updated by :math:`\beta F`.
        The carnivore's fitness is reevaluated every time it feeds by using
        the fitness_update method.

        Parameters
        ----------
        sorted_herb_list: list
            List of herbivores sorted in order of increasing fitness.
        Returns
        -------
        eaten_herbs: list

        """
        amount_to_eat = self.F
        eaten_herbs = []
        for herb in reversed(sorted_herb_list):
            if amount_to_eat <= 0:
                break
            fitness_diff = self.fitness - herb.fitness
            if fitness_diff < 0:
                break
            elif fitness_diff < self.DeltaPhiMax:
                chance_to_kill = fitness_diff / self.DeltaPhiMax
            else:
                chance_to_kill = 1
            number = random.uniform(0, 1)
            if number <= chance_to_kill:
                if amount_to_eat < herb.weight:
                    self.weight += self.beta * amount_to_eat
                    self.fitness_update()
                    eaten_herbs.append(herb)
                    return eaten_herbs
                self.weight += self.beta * herb.weight
                amount_to_eat -= herb.weight
                self.fitness_update()
                eaten_herbs.append(herb)
        return eaten_herbs


class Herb(BaseAnimal):
    """Herbivore species which lives on the island.

    The Herb class is a subclass of the BaseAnimal class, and it inherits
    the classmethods and attributes from the parent class by the super()
    function.

    Parameters
    ----------
    age: int
        Initial age of the Herbivore.
    weight: float
        Initial weight of the Herbivore.

    Attributes
    ----------
    DEFAULT_PARAMETERS : dict
        Default parameters for the herbivore species.
    fitness: int
        Value describing the herbivore's fitness
    age: int
        Initial age of the herbivore.
    weight: float
         Weight drawn from the Gaussian distribution if not assigned a value.
    parameters: dict
        Values that determines the behaviour of the herbivores.
    Raises
    ------
    ValueError
        If age is below 0 or if weight is below 0, 0 or None.
    """

    DEFAULT_PARAMETERS = {
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

    def __init__(self, age=0, weight=None):
        super().__init__(age=age, weight=weight)

    def feeding(self, fodder):
        r"""Feeds a herbivore, updates weight and returns the fodder eaten.

        The herbivore tries to eat an amount of fodder equal to its appetite F
        on the square it habits.
        The herbivores weight increases by
        :math:`\beta \times fodder_{eaten}` where the fodder_eaten
        depends on how much fodder the given square has.If the square has more
        fodder than the the herbivore's appetite,fodder_eaten is equal to the
        appetite.

        Parameters
        ----------
        fodder : int
            The amount of fodder on the square

        Returns
        -------
        F : int
            If the fodder amount of the square is greater than the appetite
        fodder : int
            If the fodder amount is greater than 0 and less than the appetite.

        Raises
        ------
        ValueError
            If the fodder value is negative
        """

        if fodder >= self.F:
            self.weight += self.beta * self.F
            return self.F
        elif (fodder > 0) and (fodder < self.F):
            self.weight += self.beta * fodder
            return fodder
        if fodder < 0:
            raise ValueError("Cannot have negative fodder value")
