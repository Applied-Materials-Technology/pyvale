'''
================================================================================
pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
import numpy as np

import mooseherder as mh

from pyvale.physics.scalarfield import ScalarField
from pyvale.physics.vectorfield import VectorField
from pyvale.physics.tensorfield import TensorField
from pyvale.sensors.sensordescriptor import SensorDescriptorFactory
from pyvale.sensors.pointsensorarray import PointSensorArray
from pyvale.uncertainty.errorintegrator import ErrorIntegrator
from pyvale.uncertainty.presyserrors import SysErrUnifPercent
from pyvale.uncertainty.randerrors import RandErrNormPercent
from pyvale.uncertainty.postsyserrors import (SysErrDigitisation,
                                              SysErrSaturation)


class SensorArrayFactory:
    @staticmethod
    def basic_thermocouple_array(sim_data: mh.SimData,
                                 positions: np.ndarray,
                                 field_name: str = "temperature",
                                 spat_dims: int = 3,
                                 sample_times: np.ndarray | None = None
                                 ) -> PointSensorArray:

        descriptor = SensorDescriptorFactory.temperature_descriptor()

        t_field = ScalarField(sim_data,field_name,spat_dims)

        sens_array = PointSensorArray(positions,
                                      t_field,
                                      sample_times,
                                      descriptor)

        sens_array = init_basic_errs(sens_array)

        post_sys_err1 = SysErrDigitisation(bits_per_unit=1/5)
        post_sys_err2 = SysErrSaturation(meas_min=0.0,meas_max=1000.0)
        post_sys_err_int = ErrorIntegrator([post_sys_err1,post_sys_err2],
                                            sens_array.get_measurement_shape())
        sens_array.set_post_sys_err_integrator(post_sys_err_int)

        return sens_array

    @staticmethod
    def basic_dispsens_array(sim_data: mh.SimData,
                            positions: np.ndarray,
                            field_name: str = "displacement",
                            spat_dims: int = 3,
                            sample_times: np.ndarray | None = None
                            ) -> PointSensorArray:

        descriptor = SensorDescriptorFactory.displacement_descriptor()

        disp_field = VectorField(sim_data,
                                 field_name,
                                 ('disp_x','disp_y'),
                                 spat_dims)

        sens_array = PointSensorArray(positions,
                                      disp_field,
                                      sample_times,
                                      descriptor)

        sens_array = init_basic_errs(sens_array)

        return sens_array

    @staticmethod
    def basic_straingauge_array(sim_data: mh.SimData,
                                positions: np.ndarray,
                                field_name: str = "strain",
                                spat_dims: int = 3,
                                sample_times: np.ndarray | None = None
                                ) -> PointSensorArray:

        descriptor = SensorDescriptorFactory.strain_descriptor()

        if spat_dims == 2:
            norm_components = ('strain_xx','strain_yy')
            dev_components = ('strain_xy',)
        else:
            norm_components = ('strain_xx','strain_yy','strain_zz')
            dev_components = ('strain_xy','strain_yz','strain_xz')

        strain_field = TensorField(sim_data,
                                 field_name,
                                 norm_components,
                                 dev_components,
                                 spat_dims)

        sens_array = PointSensorArray(positions,
                                      strain_field,
                                      sample_times,
                                      descriptor)

        sens_array = init_basic_errs(sens_array)

        return sens_array


def init_basic_errs(sens_array: PointSensorArray, err_pc: float = 6.0) -> PointSensorArray:

    pre_sys_err_int = ErrorIntegrator([SysErrUnifPercent(-err_pc,err_pc)],
                                    sens_array.get_measurement_shape())
    sens_array.set_pre_sys_err_integrator(pre_sys_err_int)

    rand_err_int = ErrorIntegrator([RandErrNormPercent(err_pc)],
                                        sens_array.get_measurement_shape())
    sens_array.set_rand_err_integrator(rand_err_int)

    return sens_array