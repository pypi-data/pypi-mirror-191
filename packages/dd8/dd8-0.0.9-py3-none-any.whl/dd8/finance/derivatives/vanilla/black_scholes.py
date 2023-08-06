# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 18:00:00 2023

@author: yqlim
"""

import logging
logger = logging.getLogger(__name__)

from typing import List
from .base import PricingModel, Option

class BlackScholesMertonModel(PricingModel):
    """
    Implements the generalized Black-Scholes-Merton model for pricing of European
    options.
    
    Attributes
    ----------
    option : vanilla.VanillaOption
        vanilla European option object    
        
    Methods
    -------
    price
    """    
    def __init__(self) -> None:
        pass

    def set_forward_curve(self) -> None:
        pass

    def set_volatility_surface(self) -> None:
        pass

    def price(self, options: List[Option]) -> None:
        for option in options:
            pass

    def imply_volatility(self) -> None:
        pass

        


