'''
================================================================================
pycave: dev_main

authors: thescepticalrabbit
================================================================================
'''
from pprint import pprint
from pathlib import Path
from functools import partial
from dataclasses import asdict

import numpy as np

import mooseherder as mh

import pycave

def main() -> None:
    data_path = Path('data/monoblock_thermal_out.e')
    dim = 3
    field_name = 'temperature'

    data_reader = mh.ExodusReader(data_path)
    sim_data = data_reader.read_all_sim_data()

    x_sens = 1
    x_min = 11.5e-3
    x_max = 11.5e-3

    y_sens = 4
    y_min = -11.5e-3
    y_max = 19.5e-3

    z_sens = 3
    z_min = 0
    z_max = 12e-3

    sens_pos_x = np.linspace(x_min,x_max,x_sens+2)[1:-1]
    sens_pos_y = np.linspace(y_min,y_max,y_sens+2)[1:-1]
    sens_pos_z = np.linspace(z_min,z_max,z_sens+2)[1:-1]
    (sens_grid_x,sens_grid_y,sens_grid_z) = np.meshgrid(
        sens_pos_x,sens_pos_y,sens_pos_z)

    sens_pos_x = sens_grid_x.flatten()
    sens_pos_y = sens_grid_y.flatten()
    sens_pos_z = sens_grid_z.flatten()
    sens_pos = np.vstack((sens_pos_x,sens_pos_y,sens_pos_z)).T
    pprint(sens_pos.shape)

    t_field = pycave.Field(sim_data,field_name,dim)
    tc_array = pycave.ThermocoupleArray(sens_pos,t_field)

    rand_err_func = partial(np.random.default_rng().normal,
                            loc=0.0,
                            scale=20.0)
    sys_err_func = partial(np.random.default_rng().uniform,
                            low=-20.0,
                            high=20.0)

    tc_array.set_random_err_func(rand_err_func)
    tc_array.set_systematic_err_func(sys_err_func)

    sens_data = tc_array.get_measurement_data()

    sens_dict = asdict(sens_data)
    for ss in sens_dict:
        print()
        print(f'{ss} =')
        pprint(sens_dict[ss])

    pv_sens = tc_array.get_visualiser()
    pv_sim = t_field.get_visualiser()
    pycave.plot_sensors(pv_sim,pv_sens,field_name)


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
