'''
================================================================================
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
import numpy as np

from pyvale.uncertainty.errorcalculator import ErrCalculator


class RandErrUniform(ErrCalculator):

    def __init__(self,
                 low: float,
                 high: float,
                 seed: int | None = None) -> None:
        self._low = low
        self._high = high
        self._rng = np.random.default_rng(seed)

    def calc_errs(self,
                  meas_shape: tuple[int,...],
                  truth_values: np.ndarray) -> np.ndarray:
        rand_errs = self._rng.uniform(low=self._low,
                                    high=self._high,
                                    size=meas_shape)
        return rand_errs


class RandErrUnifPercent(ErrCalculator):

    def __init__(self,
                 low_percent: float,
                 high_percent: float,
                 seed: int | None = None) -> None:
        self._low = low_percent
        self._high = high_percent
        self._rng = np.random.default_rng(seed)


    def calc_errs(self,
                  meas_shape: tuple[int,...],
                  truth_values: np.ndarray) -> np.ndarray:

        norm_rand = self._rng.uniform(low=self._low/100,
                                    high=self._high/100,
                                    size=meas_shape)

        rand_errs = truth_values*norm_rand
        return rand_errs


class RandErrNormal(ErrCalculator):

    def __init__(self,
                 std: float,
                 seed: int | None = None) -> None:
        self._std = std
        self._rng = np.random.default_rng(seed)

    def calc_errs(self,
                  meas_shape: tuple[int,...],
                  truth_values: np.ndarray) -> np.ndarray:
        rand_errs = self._rng.normal(loc=0.0,
                                    scale=self._std,
                                    size=meas_shape)
        return rand_errs


class RandErrNormPercent(ErrCalculator):

    def __init__(self,
                 std_percent: float,
                 seed: int | None = None) -> None:
        self._std = std_percent/100
        self._rng = np.random.default_rng(seed)


    def calc_errs(self,
                  meas_shape: tuple[int,...],
                  truth_values: np.ndarray) -> np.ndarray:

        norm_rand = self._rng.normal(loc=0.0,
                                    scale=1.0,
                                    size=meas_shape)

        rand_errs = truth_values*self._std*norm_rand
        return rand_errs
