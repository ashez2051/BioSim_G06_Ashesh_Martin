.. biosim documentation master file, created by
   sphinx-quickstart on Sun Jun 14 19:51:01 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to biosim's documentation!
==================================

.. toctree::
   fauna
   landscape
   island
   graphics
   simulation



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`




Modelling the ecosystem of Rossumøya
------------------------------------
This project models the population dynamics on a fictional island, Rossumøya. The code is developed by Ashesh Raj Gnawali and Martin Bø. The simulation includes a a series of interactions between the two species of animals (carnivores and herbivores) and simulates their migration, reproduction and eating behavior for 400 years.

The Terrain
-----------
The terrain are tile based with water covering the top, bottom and sides of the map so that it resembles an island. The water is unreachable terrain such that the herbivores and carnivores cannot migrate there. They are restricted to only entering highland, lowland and the desert. Highland has limited fodder whereas lowland is fast growing and has higher fodder value. At the end of the eyar, the available fodder is reset to the maximum value.

The Animals
-----------
Herbivores graze on lowland and highlands at a given value F and they eat in random order. Weight is gained based on how much they eat and fitness is based on a gaussian distribution.

Carnivores are dependent on herbivores for food and are therefore more mobile than herbivores. They can only eat herbivores if they are on the same terrain tile as them. If there are multiple herbivores then they eat based on their own fitness. Weight gained is increased by the proportion of the weight from the eaten herbivore. Carnivores can only eat the herbivores with a lower fitness than themselves.

Movement
--------
Movement is based on the probability of moving and the fitness. Carnivores are more mobile and have a higher chance of moving.
