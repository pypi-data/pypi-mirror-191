# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 18:00:00 2023

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

import datetime
import pytz
from dateutil.relativedelta import relativedelta
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
    compounding_frequency : ENUM_COMPOUNDING_FREQUENCY, optional
        compounding frequency to annualize data (default is continuous)
    interpolation_method : ENUM_INTERPOLATION_METHOD, optional
        numerical method to interpolate between dates (default is linear)
    extrapolation_method : ENUM_EXTRAPOLATION_METHOD, optional
        numerical method to extrapolate data beyond dates provided (default is flat)
    as_at : datetime.datetime, optional
        timestamp of forward curve (default is `datetime.datetime.utcnow()`)
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
    as_at
    curve_id
    """
    def __init__(self, dates: np.ndarray, prices: np.ndarray, 
                    daycount_convention: ENUM_DAYCOUNT_CONVENTION = ENUM_DAYCOUNT_CONVENTION.ACT_365,
                    compounding_frequency: ENUM_COMPOUNDING_FREQUENCY = ENUM_COMPOUNDING_FREQUENCY.CONTINUOUS,
                    interpolation_method: ENUM_INTERPOLATION_METHOD = ENUM_INTERPOLATION_METHOD.LINEAR,
                    extrapolation_method: ENUM_EXTRAPOLATION_METHOD = ENUM_EXTRAPOLATION_METHOD.FLAT,
                    as_at: datetime.datetime = datetime.datetime.utcnow(),
                    curve_id: str = '') -> None:
        super().__init__(dates, prices, curve_id)

        self.daycount_convention = daycount_convention
        self.compounding_frequency = compounding_frequency
        self.interpolation_method = interpolation_method
        self.extrapolation_method = extrapolation_method
        self.as_at = as_at

        self.curve = np.empty(len(self.prices))
        self.is_calibrated = False

    def __call__(self, date: datetime.datetime) -> float:
        return self.get_forward_rate(date)

    def get_forward_rate(self, date: datetime.datetime) -> float:
        pass

    def calibrate(self, spot: float) -> None:
        numerator, denominator = self.daycount_convention.value.split('/')
        duration = ((self.dates - self.as_at).astype('timedelta64[ms]').astype(int)/1000.0)/86400.0
        
        if denominator == 'ACT':
            denominator = ((self.as_at + relativedelta(years=1)) - self.as_at).total_seconds() / 86400.0
        else:
            denominator = int(denominator)
        
        if numerator == 'ACT':
            numerator = duration
        else:
            numerator = int(numerator)
        
        year_fraction = numerator / denominator

        if self.compounding_frequency == ENUM_COMPOUNDING_FREQUENCY.CONTINUOUS:
            self.curve = np.log(self.prices / spot) / year_fraction

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
    def as_at(self) -> datetime.datetime:
        return self.__dte_as_at

    @as_at.setter
    def as_at(self, as_at: datetime.datetime) -> None:
        if isinstance(as_at, datetime.datetime):
            if not as_at.tzinfo:
                self.__dte_as_at = as_at.replace(tzinfo=pytz.utc)
        else:
            raise TypeError('`as_at` must be of `datetime.datetime` type.')

    @property
    def curve_id(self) -> str:
        return self.schedule_id
    
