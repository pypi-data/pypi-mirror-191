# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 15:23:00 2022

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

from typing import Union, List, Tuple
import uuid
import pandas as pd
import numpy as np
from .enums import ENUM_RATE_OF_CHANGE_METHOD, ENUM_SMOOTHING_TYPE

def rolling_window(array1d: np.ndarray, window_size: int, stride: int) -> np.ndarray:
    """
    Generator yielding rolling windows to conserve memory.

    Parameters
    ----------
    array1d : np.ndarray
        initial array to generate rolling windows from
    window_size : int
        size of rolling window
    stride : int
        steps to generate rolling windows  (e.g. stride of 1 will have 
        `window_size`-1 overlapping elements with previous window)

    Yields
    ------
    np.ndarray
        one rolling window
    """
    N = len(array1d)
    for i in range(0, N-window_size+1, stride):
        yield array1d[i: i+window_size]    

class TechnicalIndicator(object):
    def __init__(self, uid: str = ''):
        self.uid = uid

    def fit(self, X: np.ndarray) -> np.ndarray:
        pass

    def target_level(self, target: float) -> float:
        pass

    @property
    def uid(self) -> str:
        return self.__str_uid
    
    @uid.setter
    def uid(self, uid: str) -> None:
        if uid:
            self.__str_uid = str(uid)
        else:
            self.__str_uid = uuid.uuid4()

    def _to_numpy_array(self, X: Union[pd.Series, np.ndarray]) -> np.ndarray:
        if not isinstance(X, np.ndarray):
            if isinstance(X, pd.Series):
                return X.values
            else:
                raise TypeError('`X` must be np.ndarray or pd.Series.')
        else:
            return X

class Label(TechnicalIndicator):
    def __init__(self, bins: List[Tuple[int, float]], uid: str = '') -> None:        
        super().__init__(uid)
        self.bins = bins
    
    @property
    def bins(self) -> List[Tuple[int, float]]:
        return self.__lst_bins

    @bins.setter
    def bins(self, bins: List[Tuple[int, float]]) -> None:
        self.__lst_bins = sorted(bins, key=lambda x: x[0])

    def fit(self, X: np.ndarray) -> np.ndarray:
        data = self._to_numpy_array(X).astype('float64')

        unique = np.unique(data)
        output = np.empty(len(data))
        output[:] = np.nan
        if len(unique) == len(self.bins):
            # discrete
            for label, value in self.bins:
                output[data==value] = label
        else:
            # continuous

            # labels, values = tuple(zip(*self.bins))
            # idx = np.digitize(X, values, right=False)
            # print(labels)
            # output[:] = np.asarray(labels)[idx]            
            
            for i in range(len(self.bins)-1):
                output[(~np.isnan(data)) & (data>=self.bins[i][1]) & (data<self.bins[i+1][1])] = self.bins[i+1][0]
            output[(~np.isnan(data)) & (data<self.bins[0][1])] = self.bins[0][0]
            output[(~np.isnan(data)) & (data>=self.bins[-1][1])] = self.bins[-1][0] + 1

        return output

class RateOfChange(TechnicalIndicator):
    def __init__(self, period: int, 
            method: ENUM_RATE_OF_CHANGE_METHOD = ENUM_RATE_OF_CHANGE_METHOD.NATURAL_LOG,
            shift: int = 0, uid: str = '') -> None:
        super().__init__(uid)
        self.period = period
        self.method = method
        self.shift = shift
        
    def fit(self, X: Union[pd.Series, np.ndarray], Y: Union[None, pd.Series, np.ndarray] = None) -> np.ndarray:
        data = self._to_numpy_array(X)
        if not Y is None:
            denominator = self._to_numpy_array(Y)
        else:
            denominator = data

        if self.method == ENUM_RATE_OF_CHANGE_METHOD.SIMPLE:
            rate_of_change = data[self.period : ] / denominator[ : -self.period] - 1.0
        elif self.method == ENUM_RATE_OF_CHANGE_METHOD.NATURAL_LOG:
            rate_of_change = np.log(data[self.period : ] / denominator[ : -self.period])
        if self.shift > 0:
            rate_of_change = rate_of_change[:-self.shift]
        padding = np.empty(self.period + self.shift)
        padding[:] = np.nan
        rate_of_change = np.concatenate([padding, rate_of_change], axis=0)
        
        return rate_of_change

    def target_level(self, target: float) -> float:
        pass

class RelativeStrengthIndex(TechnicalIndicator):
    def __init__(self, period: int, shift: int=0, uid: str = '') -> None:
        super().__init__(uid)
        self.period = period
        self.shift = shift

    def fit(self, X: Union[pd.Series, np.ndarray]) -> np.ndarray:
        data = self._to_numpy_array(X)                
        diff = np.diff(data)
        gains = np.abs(diff * (diff>0))
        losses = np.abs(diff * (diff<0)) 
        gains = (np.convolve(gains, np.ones(self.period), 'valid') / 
                     self.period)
        losses = (np.convolve(losses, np.ones(self.period), 'valid') / 
                      self.period)
        rsi = 100.0 - (100.0 / (1.0 + gains/losses))
        if self.shift > 0:
            rsi = rsi[:-self.shift]
        padding = np.empty(self.period + self.shift)
        padding[:] = np.nan
        rsi = np.concatenate([padding, rsi], axis=0)
        return rsi    
    
    def target_level(self, target: float) -> float:
        pass

class MovingAverage(TechnicalIndicator):
    def __init__(self, period: int, method: ENUM_SMOOTHING_TYPE = ENUM_SMOOTHING_TYPE.EXPONENTIAL_AVERAGING,
                    shift: int = 0, uid: str = ''):
        super().__init__(uid)
        self.period = period
        self.method = method
        self.shift = shift

    def fit(self, X: Union[pd.Series, np.ndarray]) -> np.ndarray:
        data = self._to_numpy_array(X)        
        result = []        
        if self.method == ENUM_SMOOTHING_TYPE.LINEAR_WEIGHTED_AVERAGING:
            windows = rolling_window(data, self.period, 1)
            for window in windows:
                result.append(np.mean(window))
        elif self.method == ENUM_SMOOTHING_TYPE.EXPONENTIAL_AVERAGING: 
            alpha = 2.0 / (self.period + 1.0)
            alpha_rev = 1-alpha
            n = data.shape[0]
            pows = alpha_rev**(np.arange(n+1))
            scale_arr = 1/pows[:-1]
            offset = data[0]*pows[1:]
            pw0 = alpha*alpha_rev**(n-1)

            mult = data*pw0*scale_arr
            cumsums = mult.cumsum()
            result = offset + cumsums*scale_arr[::-1]
            result = result[self.period-1:]

        result = np.asarray(result)
        if self.shift > 0:
            result = result[:-self.shift]        
        padding = np.empty(self.period - 1 + self.shift)
        padding[:] = np.nan
        result = np.concatenate([padding, result], axis=0)

        return result

    def target_level(self):
        pass

class StandardDeviation(TechnicalIndicator):
    def __init__(self, period: int, demean: bool = True, degrees_of_freedom: int = 0, 
                    smoothing_type: ENUM_SMOOTHING_TYPE = ENUM_SMOOTHING_TYPE.EXPONENTIAL_AVERAGING,
                    shift: int = 0, uid: str = '') -> None:
        super().__init__(uid)
        self.period = period
        self.demean = demean
        self.degrees_of_freedom = degrees_of_freedom
        self.smoothing_type = smoothing_type
        self.shift = shift

    def fit(self, X: Union[pd.Series, np.ndarray]) -> np.ndarray:
        mean = 0        
        _ = X
        result = []
        windows = rolling_window(_, self.period, 1)
        if self.demean:
            for window in windows:
                mean = np.average(window)
                result.append( np.sqrt(np.sum(np.square(window - mean)) / (self.period-1)) )
        else:
            for window in windows:                
                result.append( np.sqrt(np.sum(np.square(window - mean)) / (self.period-1)) )
        
        result = np.asarray(result)
        if self.shift > 0:
            result = result[:-self.shift]        
        padding = np.empty(self.period - 1 + self.shift)
        padding[:] = np.nan
        result = np.concatenate([padding, result], axis=0)
        
        return result   
