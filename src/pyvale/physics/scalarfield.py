'''
================================================================================
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
import numpy as np
import pyvista as pv

import mooseherder as mh

from pyvale.physics.field import (IField,
                                  FieldError,
                                  conv_simdata_to_pyvista,
                                  sample_pyvista)

class ScalarField(IField):
    def __init__(self,
                 sim_data: mh.SimData,
                 field_key: str,
                 spat_dim: int) -> None:

        self._field_key = field_key

        if sim_data.time is None:
            raise(FieldError("SimData.time is None. SimData does not have time steps"))
        self._time_steps = sim_data.time

        self._pyvista_grid = conv_simdata_to_pyvista(sim_data,
                                                    (field_key,),
                                                    spat_dim)

    def get_time_steps(self) -> np.ndarray:
        return self._time_steps

    def get_visualiser(self) -> pv.UnstructuredGrid:
        return self._pyvista_grid

    def get_all_components(self) -> tuple[str, ...]:
        return (self._field_key,)

    def get_component_index(self,comp: str) -> int:
        return 0 # scalar fields only have one component!

    def sample_field(self,
                    sample_points: np.ndarray,
                    sample_times: np.ndarray | None = None
                    ) -> np.ndarray:

        return sample_pyvista((self._field_key,),
                                self._pyvista_grid,
                                self._time_steps,
                                sample_points,
                                sample_times)

