#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:54:37 2023

@author: tom.ebermeyer
"""

from setuptools import setup

setup(
    name="TP2_Robot_EBERMEYER_Tom",
    version="0.0.1",
    author="Tom Ebermeyer",
    author_email="tom.ebermeyer@cpe.fr",
    description="Deplacement d'un robot (modélisé par un '1') dans un grille de '0' de taille définie par l'user.",
    packages=['Package_robot'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
