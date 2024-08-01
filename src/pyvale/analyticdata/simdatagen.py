'''
================================================================================
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
from typing import Self
from dataclasses import dataclass
import numpy as np
import sympy

import mooseherder as mh

from pyvale.analyticdata.meshgen import rectangle_mesh_2d, fill_dims

@dataclass
class AnalyticCaseData2D:
    length_x: float = 10.0
    length_y: float = 7.5
    num_elem_x: int = 4
    num_elem_y: int = 3
    time_steps: np.ndarray | None = None
    field_keys: tuple[str,...] = ('scalar',)
    funcs_x: tuple[sympy.Expr,...] | None = None
    funcs_y: tuple[sympy.Expr,...] | None = None
    funcs_t: tuple[sympy.Expr,...] | None = None
    symbols: tuple[sympy.Symbol,...] = (sympy.Symbol("y"),
                                        sympy.Symbol("x"),
                                        sympy.Symbol("t"))
    offsets_space: tuple[float,...] = (0.0,)
    offsets_time: tuple[float,...] = (0.0,)
    nodes_per_elem: int = 4


class AnalyticSimDataGenerator:
    def __init__(self, case_data: AnalyticCaseData2D
                 ) -> None:

        self._case_data = case_data
        (self._coords,self._connect) = rectangle_mesh_2d(case_data.length_x,
                                                         case_data.length_y,
                                                         case_data.num_elem_x,
                                                         case_data.num_elem_y)

        self._field_sym_funcs = dict()
        self._field_lam_funcs = dict()
        for ii,kk in enumerate(case_data.field_keys):
            self._field_sym_funcs[kk] = ((case_data.funcs_x[ii] *
                                          case_data.funcs_y[ii] +
                                          case_data.offsets_space[ii]) *
                                        (case_data.funcs_t[ii] +
                                         case_data.offsets_time[ii]))

            self._field_lam_funcs[kk] = sympy.lambdify(case_data.symbols,
                                                self._field_sym_funcs[kk],
                                                'numpy')
        #self._field_eval = np.zeros()

    def evaluate_fields(self) -> dict[str,np.ndarray]:
        (x_eval,y_eval,t_eval) = fill_dims(self._coords[:,0],
                                           self._coords[:,1],
                                           self._case_data.time_steps)
        eval_comps = dict()
        for kk in  self._case_data.field_keys:
            eval_comps[kk] = self._field_lam_funcs[kk](y_eval,
                                                        x_eval,
                                                        t_eval)
        return eval_comps

    def generate_sim_data(self) -> mh.SimData:
        sim_data = mh.SimData()
        sim_data.num_spat_dims = 2
        sim_data.time = self._case_data.time_steps
        sim_data.coords = self._coords
        sim_data.connect = {'connect1': self._connect}
        sim_data.node_vars = eval_comps
        return sim_data


    def get_visualisation_grid(self,
                               time_step: int = -1
                               ) -> tuple[np.ndarray,np.ndarray,np.ndarray]:

        grid_shape = (self._case_data.num_elem_y+1,
                      self._case_data.num_elem_x+1)
        grid_x = np.atleast_2d(self._coords[:,0]).T.reshape(grid_shape)
        grid_y = np.atleast_2d(self._coords[:,1]).T.reshape(grid_shape)
        #scalar_grid = np.reshape(scalar_vals[:,time_step],grid_shape)

        return (grid_x,grid_y)


