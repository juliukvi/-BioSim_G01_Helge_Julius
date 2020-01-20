# -*- coding: utf-8 -*-

__author__ = 'Helge Helo Klemetsdal'
__email__ = 'hegkleme@nmbu.no'

import textwrap
from biosim.animals import Herb
import math as m
import random


class BaseNature:
    """Baseclass for the landscape types on the island.

    Attributes
    ----------
    fodder : int
        Initial fodder amount on the landscape type.
    habitable : bool
        Determines if the landscpape can be habited by animals.
    herb_list : list
        A list with all the herbivores on the landscape cell.
    carn_list : list
        A list with all the herbivores on the landscape cell.
    herb_move_to_list : list
        A list with all the herbivores that shall migrate to another cell
    herb_move_from_list : list
        A list with all the herbivores that shall migrate from the cell
    carn_move_to_list : list
        A list with all the carnivores that shall migrate to another cell
    carn_move_from_list : list
        A list with all the carnivores that shall migrate from the cell
    """
    def __init__(self):
        self.fodder = 0
        self.habitable = True
        self.herb_list = []
        self.carn_list = []
        self.herb_move_to_list = []
        self.herb_move_from_list = []
        self.carn_move_to_list = []
        self.carn_move_from_list = []

    def feed_all_animals(self):
        """Feeds all animals in the landscape cell.

        The animals feed in order of fitness, i.e., the animal with the
        highest fitness eats first.
        """
        self.herb_list.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.herb_list:
            if self.fodder > 0:
                self.fodder -= animal.feeding(self.fodder)
            else:
                break
        self.carn_list.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.carn_list:
            if len(self.herb_list) == 0:
                break
            eaten_herbs = animal.feeding(self.herb_list)
            for eaten_herb in eaten_herbs:
                self.herb_list.remove(eaten_herb)

    def birth_all_animals(self):
        """Determines which of the animals in the cell that give birth.

        Two animals are required to give birth. If a new animal is born the
        newborn is added to the list of the newborn's species.
        """
        num_herb = len(self.herb_list)
        if num_herb >= 2:
            newborn_list = []
            for animal in self.herb_list:
                newborn = animal.will_birth(num_herb)
                if newborn:
                    newborn_list.append(newborn)
            for newborn in newborn_list:
                self.herb_list.append(newborn)
        num_carn = len(self.carn_list)
        if num_carn >= 2:
            newborn_list = []
            for animal in self.carn_list:
                newborn = animal.will_birth(num_carn)
                if newborn:
                    newborn_list.append(newborn)
            for newborn in newborn_list:
                self.carn_list.append(newborn)

    def migrate_all_animals(self, neighbors):
        r"""Determines all animals in the cell that shall migrate.

        The animals can migrate to the cell located directly north, west,
        south, or east of their current cell. This set of cells are defined
        as the set :math:`\emph{C^{i}}`.
        For all the four neighbour cells we define a relative abundance of
        fodder given by following formula:
        .. math::
            \epsilon_{k} = \frac{\emph{f_{k}}}{(\emph{n_{k}+1)}F'}

        where :math:`\emph{f_{k}` is the amount of relevant fodder for the
        species available in the cell k :math:`\emph{n_{k}}` is the
        number of animals of the same species in cell k,
        and "F" the appetite of the species.

        The propensity of moving to a neighbour cell is dependent on the
        relative abundance of fodder and is given by formula:
        .. math::

            \pi_{\emph{i}\rightarrow\emph{j}}=
                 \begin{cases}
                     0, & \text{if \emph{j} is Mountain or Ocean} \\
                     e^{\lambda\epsilon_{j}}, & \text{\emph{otherwise}}
                 \end{cases}

        given that the animal would move from cell i to cell j.
        If the animal migrates, the probability of moving to each of the four
        neighbour cell is calculated based on the propensity to move to each
        cell. The probability to move from i to j follows the formula:

        ..math::
            p_{\emph{i}\rightarrow\emph{j}}= \frac{\pi_{\emph{i}\rightarrow\emph{j}}}{\Sigma_{\emph{j}\in C^{({\emph{i}})}}\pi_{\emph{i}\rightarrow\emph{j}}}

        The animals that migrate to a neighbouring cell are placed in lists
        according to their current cell and the cell they will migrate to.
        Notes
        -----
        In the case that all cells in :math:`\emph{C^{i}}` are Mountain or
        ocean, the animal will not migrate.

        If the animals appetite is 0
        the probability of moving to either of the neighbour cells is 0.

        Parameters
        ----------
        neighbors : tuple with four BaseNature classes
            A tuple containing the set of different neighbour locations.

        """
        for animal in self.herb_list:
            if animal.migrate():
                north_nature_square = neighbors[0]
                east_nature_square = neighbors[1]
                south_nature_square = neighbors[2]
                west_nature_square = neighbors[3]
                if animal.F == 0:
                    (north_relative_abundance,  east_relative_abundance,
                     south_relative_abundance, west_relative_abundance) = (0, 0,
                                                                           0, 0)
                else:
                    north_relative_abundance = north_nature_square.fodder/((len(north_nature_square.herb_list)+1)*animal.F)
                    east_relative_abundance = east_nature_square.fodder/((len(east_nature_square.herb_list)+1)*animal.F)
                    south_relative_abundance = south_nature_square.fodder/((len(south_nature_square.herb_list)+1)*animal.F)
                    west_relative_abundance = west_nature_square.fodder/((len(west_nature_square.herb_list)+1)*animal.F)
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
                # if total_propensity is zero no animal can move so loop breaks
                if total_propensity == 0:
                    break
                north_move_prob = north_propensity/total_propensity
                east_move_prob = north_move_prob + east_propensity/total_propensity
                south_move_prob = east_move_prob + south_propensity/total_propensity
                west_move_prob = south_move_prob + west_propensity/total_propensity
                number = random.uniform(0, 1)
                if number < north_move_prob:
                    north_nature_square.herb_move_to_list.append(animal)
                    self.herb_move_from_list.append(animal)
                elif number < east_move_prob:
                    east_nature_square.herb_move_to_list.append(animal)
                    self.herb_move_from_list.append(animal)
                elif number < south_move_prob:
                    south_nature_square.herb_move_to_list.append(animal)
                    self.herb_move_from_list.append(animal)
                elif number < west_move_prob:
                    west_nature_square.herb_move_to_list.append(animal)
                    self.herb_move_from_list.append(animal)

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

                if animal.F == 0:
                    (north_relative_abundance,  east_relative_abundance,
                     south_relative_abundance, west_relative_abundance) = (0, 0,
                                                                           0, 0)
                else:
                    north_relative_abundance = north_herb_weight / (
                                (len(north_nature_square.carn_list) + 1) * animal.F)
                    east_relative_abundance = east_herb_weight / (
                                (len(east_nature_square.carn_list) + 1) * animal.F)
                    south_relative_abundance = south_herb_weight / (
                                (len(south_nature_square.carn_list) + 1) * animal.F)
                    west_relative_abundance = west_herb_weight / (
                                (len(west_nature_square.carn_list) + 1) * animal.F)

                if north_nature_square.habitable:
                    north_propensity = m.exp(animal._lambda * north_relative_abundance)
                else:
                    north_propensity = 0
                if east_nature_square.habitable:
                    east_propensity = m.exp(animal._lambda * east_relative_abundance)
                else:
                    east_propensity = 0
                if south_nature_square.habitable:
                    south_propensity = m.exp(animal._lambda * south_relative_abundance)
                else:
                    south_propensity = 0
                if west_nature_square.habitable:
                    west_propensity = m.exp(animal._lambda * west_relative_abundance)
                else:
                    west_propensity = 0
                total_propensity = (north_propensity + east_propensity + south_propensity + west_propensity)
                if total_propensity == 0:
                    break
                north_move_prob = north_propensity / total_propensity
                east_move_prob = north_move_prob + east_propensity / total_propensity
                south_move_prob = east_move_prob + south_propensity / total_propensity
                west_move_prob = south_move_prob + west_propensity / total_propensity
                number = random.uniform(0, 1)
                if number < north_move_prob:
                    north_nature_square.carn_move_to_list.append(animal)
                    self.carn_move_from_list.append(animal)
                elif number < east_move_prob:
                    east_nature_square.carn_move_to_list.append(animal)
                    self.carn_move_from_list.append(animal)
                elif number < south_move_prob:
                    south_nature_square.carn_move_to_list.append(animal)
                    self.carn_move_from_list.append(animal)
                elif number < west_move_prob:
                    west_nature_square.carn_move_to_list.append(animal)
                    self.carn_move_from_list.append(animal)

    def aging_all_animals(self):
        """Determines which of the animals in the cell give birth.
        """
        for animal in self.herb_list:
            animal.age()
            # animal.fitness_update()
        for animal in self.carn_list:
            animal.age()
            # animal.fitness_update()

    def fodder_update(self):
        """An empty function that is overwritten by certain landscape types.
        """
        pass

    def weightloss_all_animals(self):
        """Decrease of weight for all animals in the cell.
        """
        for animal in self.herb_list:
            animal.weightloss()
            animal.fitness_update()
        for animal in self.carn_list:
            animal.weightloss()
            animal.fitness_update()

    def death_all_animals(self):
        """Determines which of the animals in the cell that dies.

        Replaces the list of animals with new lists that do not contain
        the ones that died.

        """
        self.herb_list = [
            animal for animal in self.herb_list if not animal.death()
        ]
        self.carn_list = [
            animal for animal in self.carn_list if not animal.death()
        ]

    def herbivore_number(self):
        """Returns the number of herbivores in the cell.

        Returns
        -------
        int
        """
        return len(self.herb_list)

    def carnivore_number(self):
        """Returns the number of carnivores in the cell.

        Returns
        -------
        int
        """
        return len(self.carn_list)


class Ocean(BaseNature):
    """Ocean type landscape.

    This landscape is unhabitable for animals.

    Attributes
    ----------
    fodder : int
        Initial fodder amount on the Ocean cell.
    habitable : bool
        Determines if the landscpape can be habited by animals.
    herb_list : list
        A list with all the herbivores on the landscape cell.
    carn_list : list
        A list with all the herbivores on the landscape cell.
    herb_move_to_list : list
        A list with all the herbivores that shall migrate to another cell
    herb_move_from_list : list
        A list with all the herbivores that shall migrate from the cell
    carn_move_to_list : list
        A list with all the carnivores that shall migrate to another cell
    carn_move_from_list : list
        A list with all the carnivores that shall migrate from the cell
        """
    def __init__(self):
        super().__init__()
        self.habitable = False


class Mountain(BaseNature):
    """Mountain type landscape.

    This landscape is unhabitable for animals.

    Attributes
    ----------
    fodder : int
        Initial fodder amount on the Mountain cell.
    habitable : bool
        Determines if the Mountain landscape can be habited by animals.
    herb_list : list
        A list with all the herbivores on the Mountain cell.
    carn_list : list
        A list with all the herbivores on the Mountain cell.
    herb_move_to_list : list
        A list with all the herbivores that shall migrate to another cell
    herb_move_from_list : list
        A list with all the herbivores that shall migrate from the cell
    carn_move_to_list : list
        A list with all the carnivores that shall migrate to another cell
    carn_move_from_list : list
        A list with all the carnivores that shall migrate from the cell
    """
    def __init__(self):
        super().__init__()
        self.habitable = False


class Desert(BaseNature):
    """Desert type landscape.

    This landscape type has no fodder available for herbivores.

    Attributes
    ----------
    fodder : int
        Initial fodder amount on the Desert cell.
    habitable : bool
        Determines if the Desert can be habited by animals.
    herb_list : list
        A list with all the herbivores on the Desert cell.
    carn_list : list
        A list with all the herbivores on the Desert cell.
    herb_move_to_list : list
        A list with all the herbivores that shall migrate to another cell
    herb_move_from_list : list
        A list with all the herbivores that shall migrate from the cell
    carn_move_to_list : list
        A list with all the carnivores that shall migrate to another cell
    carn_move_from_list : list
        A list with all the carnivores that shall migrate from the cell
    """
    def __init__(self):
        super().__init__()


class Savannah(BaseNature):
    """Savannah type landscape.

    Attributes
    ----------
    DEFAULT_PARAMETERS : dict
        Default parameters for savannah.
    parameters : dict
        Initiated by set_default_parameters method.
    fodder : int
        Initial fodder amount on the Savannah cell equal to f_max parameter.
    habitable : bool
        Determines if the Savannah can be habited by animals.
    herb_list : list
        A list with all the herbivores on the Savannah cell.
    carn_list : list
        A list with all the herbivores on the savannah cell.
    herb_move_to_list : list
        A list with all the herbivores that shall migrate to another cell
    herb_move_from_list : list
        A list with all the herbivores that shall migrate from the cell
    carn_move_to_list : list
        A list with all the carnivores that shall migrate to another cell
    carn_move_from_list : list
        A list with all the carnivores that shall migrate from the cell
    """
    DEFAULT_PARAMETERS = {"f_max": 300, "alpha": 0.3}
    parameters = None

    @classmethod
    def set_default_parameters_for_savannah(cls):
        """Sets the savannah default parameters as attributes on a class level.

        This is achieved by copying the subjective DEFAULT_PARAMETERS class,
        and then using the _set_params_as_attributes method to assign them
        as class attributes.
        """
        cls.parameters = cls.DEFAULT_PARAMETERS.copy()
        cls._set_params_as_attributes()

    @classmethod
    def set_parameters(cls, new_params):
        """Updates the parameters for the savannah subclass with new values.

        Parameters
        ----------
        new_params: dict
            Dictionary containing key(s) that exist in DEFAULT_PARAMETERS.
        Raises
        ------
        KeyError
            If the key in new_params does not exist in parameters.
        ValueError
            If the new value assigned to the key is not of type float or int.
        ValueError
            If the assigned parameter values are not in the right ranges.
        """
        for key in new_params:
            if key not in cls.parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
            if isinstance(new_params[key], int) or isinstance(new_params[key], float):
                continue
            else:
                raise ValueError(f'Value needs to be int or float, got:{type(new_params[key]).__name__}')
        cls.parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        """Sets the Savannah parameters to attributes on a class level.
        """
        for key in cls.parameters:
            setattr(cls, key, cls.parameters[key])

    def __init__(self):
        if self.parameters is None:
            self.set_default_parameters_for_savannah()
        super().__init__()
        self.fodder = self.f_max

    def fodder_update(self):
        """Updates the fodder in the savannah cell.

        The fodder grows yearly by the formula:

        .. math::
            \emph{f} \leftarrow \emph{f} + \alpha\times({f^{Sav}_{max}}-\emph{f})
        where f is the fodder amount on the savannah cell,
        and :math: {f^{Sav}_{max}} is the maximum available fodder.
        """
        self.fodder = self.fodder + self.alpha * (self.f_max - self.fodder)


class Jungle(BaseNature):
    """Jungle type landscape.

    Attributes
    ----------
    DEFAULT_PARAMETERS : dict
        Default parameters for the jungle landscape.
    parameters : bool or dict?
        something
    fodder : int
        Initial fodder amount on the Jungle cell equal to f_max parameter.
    habitable : bool
        Determines if the Jungle cell can be habited by animals.
    herb_list : list
        A list with all the herbivores on the Jungle cell.
    carn_list : list
        A list with all the herbivores on the Jungle cell.
    herb_move_to_list : list
        A list with all the herbivores that shall migrate to another cell
    herb_move_from_list : list
        A list with all the herbivores that shall migrate from the cell
    carn_move_to_list : list
        A list with all the carnivores that shall migrate to another cell
    carn_move_from_list : list
        A list with all the carnivores that shall migrate from the cell
        """
    DEFAULT_PARAMETERS = {"f_max": 800}
    parameters = None

    @classmethod
    def set_default_parameters_for_jungle(cls):
        """Sets the jungle default parameters as attributes on a class level.

        This is achieved by copying the subjective DEFAULT_PARAMETERS class,
        and then using the _set_params_as_attributes method to assign them
        as class attributes.
        """
        cls.parameters = cls.DEFAULT_PARAMETERS.copy()
        cls._set_params_as_attributes()

    @classmethod
    def set_parameters(cls, new_params):
        """Updates the parameters for the jungle subclass with new values.

        Parameters
         ----------
        new_params: dict
            Dictionary containing key(s) that exist in DEFAULT_PARAMETERS.
        Raises
        ------
        KeyError
             If the key in new_params does not exist in parameters.
        ValueError
             If the new value assigned to the key is not of type float or int.
        ValueError
            If the assigned parameter values are not in the right ranges.
        """
        for key in new_params:
            if key not in cls.parameters.keys():
                raise KeyError(f'Parameter {key} is not in valid')
            if isinstance(new_params[key], int) or isinstance(new_params[key], float):
                continue
            else:
                raise ValueError(f'Value needs to be int or float, got:{type(new_params[key]).__name__}')
        cls.parameters.update(new_params)
        cls._set_params_as_attributes()

    @classmethod
    def _set_params_as_attributes(cls):
        """Sets the Savannah parameters to attributes on a class level.
        """
        for key in cls.parameters:
            setattr(cls, key, cls.parameters[key])

    def __init__(self):
        if self.parameters is None:
            self.set_default_parameters_for_jungle()
        super().__init__()
        self.fodder = self.f_max

    def fodder_update(self):
        """Updates the fodder in the jungle cell.

        The jungle grows fodder back to maximum level every year.

        """
        self.fodder = self.f_max
