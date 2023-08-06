# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 18:00:00 2023

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

from .base import Underlying

class Security(Underlying):
    def __init__(self) -> None:
        pass

class Cryptocurrency(Underlying):
    def __init__(self) -> None:
        pass