# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 18:00:00 2023

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

import datetime
import numpy as np
from .base import Schedule
from .enums import (ENUM_DAYCOUNT_CONVENTION, ENUM_COMPOUNDING_FREQUENCY,
                    ENUM_INTERPOLATION_METHOD, ENUM_EXTRAPOLATION_METHOD)

class ForwardCurve(Schedule):
    """
    Inheriting from `Schedule` base class to represent a futures
    forward curve. Facilitates the conversion of price data to 
    annualized rates data.

    Parameters
    ----------
    dates : np.ndarray
        numpy array of `datetime.datetime` objects
    prices : np.ndarray
        numpy array of `np.floating` type
    daycount_convention : ENUM_DAYCOUNT_CONVENTION, optional
        daycount convention to annualize data (default is actual/365)
    curve_id : str, optional
        unique identifier (default is `uuid.uuid4()`)

    Attributes
    ----------
    dates
    prices
    daycount_convention
    compounding_frequency
    interpolation_method
    extrapolation_method
    curve_id
    """
    def __init__(self, dates: np.ndarray, prices: np.ndarray, 
                    daycount_convention: ENUM_DAYCOUNT_CONVENTION.ACT_365,
                    compounding_frequency: ENUM_COMPOUNDING_FREQUENCY.CONTINUOUS,
                    interpolation_method: ENUM_INTERPOLATION_METHOD.LINEAR,
                    extrapolation_method: ENUM_EXTRAPOLATION_METHOD.FLAT,
                    curve_id: str = '') -> None:
        super().__init__(dates, prices, curve_id)

        self.daycount_convention = daycount_convention
        self.compounding_frequency = compounding_frequency
        self.interpolation_method = interpolation_method
        self.extrapolation_method = extrapolation_method

    def __call__(self, date: datetime.datetime) -> float:
        return self.get_forward_rate(date)

    def get_forward_rate(self, date: datetime.datetime) -> float:
        pass

    def calibrate(self, spot: float) -> None:
        pass

    @property
    def prices(self) -> np.ndarray:
        return self.values
    
    @property
    def daycount_convention(self) -> ENUM_DAYCOUNT_CONVENTION:
        return self.__enum_daycount_convention

    @daycount_convention.setter
    def daycount_convention(self, daycount_convention: ENUM_DAYCOUNT_CONVENTION) -> None:
        if isinstance(daycount_convention, ENUM_DAYCOUNT_CONVENTION):
            self.__enum_daycount_convention = daycount_convention
        else:
            raise TypeError('`ForwardCurve.daycount_convention` must be of `ENUM_DAYCOUNT_CONVENTION` type.')
    
    @property
    def compounding_frequency(self) -> ENUM_COMPOUNDING_FREQUENCY:
        return self.__enum_compounding_frequency
    
    @compounding_frequency.setter
    def compounding_frequency(self, compounding_frequency: ENUM_COMPOUNDING_FREQUENCY) -> None:
        if isinstance(compounding_frequency, ENUM_COMPOUNDING_FREQUENCY):
            self.__enum_compounding_frequency = compounding_frequency
        else:
            raise TypeError('`ForwardCurve.compounding_frequency` must be of `ENUM_COMPOUNDING_FREQUENCY` type.')

    @property
    def interpolation_method(self) -> ENUM_INTERPOLATION_METHOD:
        return self.__enum_interpolation_method
    
    @interpolation_method.setter
    def interpolation_method(self, interpolation_method) -> None:
        if isinstance(interpolation_method, ENUM_INTERPOLATION_METHOD):
            self.__enum_interpolation_method = interpolation_method
        else:
            raise TypeError('`ForwardCurve.interpolation_method` must be of `ENUM_INTERPOLATION_METHOD` type.')
    
    @property
    def extrapolation_method(self) -> ENUM_EXTRAPOLATION_METHOD:
        return self.__enum_extrapolation_method
    
    @extrapolation_method.setter
    def extrapolation_method(self, extrapolation_method: ENUM_EXTRAPOLATION_METHOD) -> None:
        if isinstance(extrapolation_method, ENUM_EXTRAPOLATION_METHOD):
            self.__enum_extrapolation_method = extrapolation_method
        else:
            raise TypeError('`ForwardCurve.extrapolation_method` must be of `ENUM_EXTRAPOLATION_METHOD` type.')

    @property
    def curve_id(self) -> str:
        return self.schedule_id
    
