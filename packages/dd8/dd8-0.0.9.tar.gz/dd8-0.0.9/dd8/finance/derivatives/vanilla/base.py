# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 18:00:00 2023

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

from typing import Union
import uuid
import datetime
import pytz

from .enums import ENUM_OPTION_TYPE, ENUM_OPTION_STYLE

class PricingModel(object):
    """
    Abstract Base Class for vanilla pricing models. `PricingModel` objects 
    should always be initiated with model parameters and not with the instrument
    to be priced, for consistent implementation. The instrument is then passed
    to the `PricingModel` object via the `price()` method.
    """
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    def __repr__(self):
        pass
        
    def __str__(self):
        pass
    
    def __len__(self):
        pass    
    
    def price(self):
        pass
    
class Underlying(object):
    def __init__(self) -> None:
        pass

class Option(object):
    """
    Each instance represents a vanilla option. Does not assume any asset class
    but instead takes parameters that have asset-class specific properties or 
    behaviour (e.g. `cost_of_carry` can take a equity.Dividend object).
    
    Attributes
    ----------
    expiration : datetime.datetime
        expiration datetime of option - if no timezone information
        is provided, utc is assumed
    strike : double
        strike price of option
    option_type : ENUM_OPTION_TYPE
        type of option (put, call and eventually exotic options)
    option_style : ENUM_OPTION_STYLE
        style of option (european, american or path_dependent)
    underlying : finance.derivatives.vanilla.base.Underlying, optional
        underlying object or any other inherited object 
        (e.g. finance.derivatives.vanilla.instruments.Security)
        (default is None, which implies a generic vanilla option)  
    option_id : str, optional
        unique identifier of the option (default is uuid.uuid4())
    """    
    def __init__(self, expiration: datetime.datetime,
                    strike: float, option_type: ENUM_OPTION_TYPE, 
                    option_style: ENUM_OPTION_STYLE,
                    underlying: Underlying = None,
                    option_id: str = '') -> None:
        self.expiration = expiration
        self.strike = strike
        self.option_type = option_type
        self.option_style = option_style
        self.underlying = underlying
        self.option_id = option_id
    
    @property
    def expiration(self) -> datetime.datetime:
        return self.__dte_expiration

    @expiration.setter  
    def expiration(self, expiration: datetime.datetime) -> None:
        if isinstance(expiration, datetime.datetime):
            if not expiration.tzinfo:
                self.__dte_expiration = expiration.replace(tzinfo=pytz.utc)
        else:
            raise TypeError('`expiration` must be of `datetime.datetim` type.')
    
    @property
    def strike(self) -> float:
        return self.__dbl_strike
    
    @strike.setter
    def strike(self, strike: float) -> None:
        if isinstance(strike, float):
            self.__dbl_strike = strike
        else:
            raise TypeError('`strike` must be of `float` type.')

    @property
    def option_type(self) -> ENUM_OPTION_TYPE:
        return self.__enum_option_type

    @option_type.setter
    def option_type(self, option_type: ENUM_OPTION_TYPE) -> None:
        if isinstance(option_type, ENUM_OPTION_TYPE):
            self.__enum_option_type = option_type
        else:
            raise TypeError('`option_type` must be of `ENUM_OPTION_TYPE` type.')

    @property
    def option_style(self) -> ENUM_OPTION_STYLE:
        return self.__enum_option_style

    @option_style.setter
    def option_style(self, option_style: ENUM_OPTION_STYLE) -> None:
        if isinstance(option_style, ENUM_OPTION_STYLE):
            self.__option_style = option_style
        else:
            raise TypeError('`option_style` must be of `ENUM_OPTION_STYLE` type.')
    
    @property
    def underlying(self) -> Underlying:
        return self.__obj_underlying
    
    @underlying.setter
    def underlying(self, underlying: Underlying) -> None:
        if isinstance(underlying, Underlying):
            self.__obj_underlyin = underlying
        else:
            raise TypeError('`underlying` must be of `Underlying` type.')
    
    @property
    def option_id(self) -> str:
        return self.__str_option_id
    
    @option_id.setter
    def option_id(self, option_id: Union[str, None]) -> None:
        if option_id:
            self.__str_option_id = str(option_id)
        else:
            self.__str_option_id = str(uuid.uuid4())