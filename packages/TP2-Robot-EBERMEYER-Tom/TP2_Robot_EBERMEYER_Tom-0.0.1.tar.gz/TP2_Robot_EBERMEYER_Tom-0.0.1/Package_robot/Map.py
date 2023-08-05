#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 17:06:08 2023

@author: tom.ebermeyer
"""
from numpy import zeros


class Grid:
    """Classe de Map"""

    def __init__(self, nb_lignes, nb_colonnes):
        """Initialisation de la grille"""
        if (nb_lignes < 10 or nb_colonnes < 10) and (
            isinstance(nb_lignes, int) and isinstance(nb_colonnes, int)
        ):
            self.nb_lignes = nb_lignes
            self.nb_colonnes = nb_colonnes
        else:
            if not (nb_lignes < 10 or nb_colonnes < 10):
                raise ValueError("Values can't be superior to 10 !")
            if not (
                isinstance(nb_lignes, int) == True
                and isinstance(nb_colonnes, int) == True
            ):
                raise ValueError("Values must be integer !")
            self.nb_lignes = 10
            self.nb_colonnes = 10
        self.grid = zeros((self.nb_lignes, self.nb_colonnes), int)
        self.X_robot = 0
        self.Y_robot = 0
        self.robot = self.grid[self.X_robot][self.Y_robot] = 1

    def print_grid(self):
        """Affichage de la grille"""
        print(self.grid)
        print("-------------------------------\n")

    def clean(self):
        """Retire l'ancienne position du robot"""
        self.robot = self.grid[self.X_robot][self.Y_robot] = 0

    def update(self):
        """Met à jour la nouvelle position du robot"""
        self.robot = self.grid[self.X_robot][self.Y_robot] = 1

    def down(self):
        """Descendre d'un cran dans la grille"""
        if self.X_robot < self.nb_lignes - 1:
            self.clean()
            self.X_robot += 1
            self.update()
        else:
            return "OUT OF BORDERS !"

    def up(self):
        """Monter d'un cran dans la grille"""
        if self.X_robot > 0:
            self.clean()
            self.X_robot -= 1
            self.update()
        else:
            return "OUT OF BORDERS !"

    def right(self):
        """Monter d'un cran dans la grille"""
        if self.Y_robot < self.nb_colonnes - 1:
            self.clean()
            self.Y_robot += 1
            self.update()
        else:
            return "OUT OF BORDERS !"

    def left(self):
        """Monter d'un cran dans la grille"""
        if self.Y_robot > 0:
            self.clean()
            self.Y_robot -= 1
            self.update()
        else:
            return "OUT OF BORDERS !"
