'''
================================================================================
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
import numpy as np

from pyvale.uncertainty.errorcalculator import ErrCalculator


class SysErrUniform(ErrCalculator):

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

        err_shape = np.array(meas_shape)
        err_shape[-1] = 1
        sys_errs = self._rng.uniform(low=self._low,
                                    high=self._high,
                                    size=err_shape)

        tile_shape = np.array(meas_shape)
        tile_shape[0:-1] = 1
        sys_errs = np.tile(sys_errs,tuple(tile_shape))

        return sys_errs


class SysErrNormal(ErrCalculator):

    def __init__(self,
                 std: float,
                 seed: int | None = None) -> None:
        self._std = std
        self._rng = np.random.default_rng(seed)

    def calc_errs(self,
                  meas_shape: tuple[int,...],
                  truth_values: np.ndarray,
                  ) -> np.ndarray:

        err_shape = np.array(meas_shape)
        err_shape[-1] = 1
        sys_errs = self._rng.normal(loc=0.0,
                                    scale=self._std,
                                    size=err_shape)

        tile_shape = np.array(meas_shape)
        tile_shape[0:-1] = 1
        sys_errs = np.tile(sys_errs,tuple(tile_shape))

        return sys_errs





