'''
================================================================================
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''

import numpy as np

from pyvale.physics.field import IField
from pyvale.uncertainty.errorcalculator import IErrCalculator


class SysErrPosition(IErrCalculator):

    def __init__(self,
                 field: IField,
                 sens_pos: np.ndarray,
                 std_by_ax: tuple[float | None,float | None,float | None],
                 sample_times: np.ndarray | None = None,
                 seed: int | None = None) -> None:

        self._field = field
        self._sens_pos_original = np.copy(sens_pos)
        self._sens_pos_perturbed = np.copy(sens_pos)
        self._std_by_ax = std_by_ax
        self._sample_times = sample_times
        self._rng = np.random.default_rng(seed)

    def get_perturbed_pos(self) -> np.ndarray:
        
        return self._sens_pos_perturbed

    def calc_errs(self,
                  err_basis: np.ndarray) -> np.ndarray:

        self._sens_pos_perturbed = np.copy(self._sens_pos_original)

        for ii,ss in enumerate(self._std_by_ax):
            if ss is not None:
                self._sens_pos_perturbed[:,ii] = self._sens_pos_perturbed[:,ii]\
                    + self._rng.normal(loc=0.0,
                                        scale=ss,
                                        size=self._sens_pos_perturbed.shape[0])

        sys_errs = self._field.sample_field(self._sens_pos_perturbed,
                                            self._sample_times) - err_basis
        return sys_errs


class SysErrSpatialAverage(IErrCalculator):

    def __init__(self, field: IField) -> None:
        self._field = field

    def calc_errs(self,
                  err_basis: np.ndarray) -> np.ndarray:

        return np.array([])


class SysErrTemporalAverage(IErrCalculator):

    def __init__(self, field: IField) -> None:
        self._field = field


    def calc_errs(self,
                  err_basis: np.ndarray) -> np.ndarray:

        return np.array([])