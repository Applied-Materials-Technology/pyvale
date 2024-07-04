'''
================================================================================
example: thermocouples on a 2d plate

pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
from pathlib import Path
import matplotlib.pyplot as plt
import mooseherder as mh
import pyvale


def main() -> None:
    """Pyvale example: Point sensors on a 2D thermal simulation
    ----------------------------------------------------------------------------
    - Explanation of the usage of 'get_measurements()' and 'calc_measurements()'

    NOTES:
    - A sensor measurement is defined as:
        measurement = truth + systematic error + random error.
    - Calling the 'get' methods of the sensor array will retrieve the results
      for the current experiment.
    - Calling the 'calc' methods will generate a new
      experiment by sampling/calculating the systematic and random errors.

    """
    data_path = Path('data/examplesims/plate_2d_thermal_out.e')
    data_reader = mh.ExodusReader(data_path)
    sim_data = data_reader.read_all_sim_data()
    field_key = list(sim_data.node_vars.keys())[0] # type: ignore

    n_sens = (4,1,1)
    x_lims = (0.0,2.0)
    y_lims = (0.0,1.0)
    z_lims = (0.0,0.0)
    sens_pos = pyvale.create_sensor_pos_array(n_sens,x_lims,y_lims,z_lims)

    tc_array = pyvale.SensorArrayFactory \
        .basic_thermocouple_array(sim_data,
                                  sens_pos,
                                  field_key,
                                  spat_dims=2)


    measurements = tc_array.get_measurements()

    print('\n'+80*'-')
    print('For a sensor: measurement = truth + sysematic error + random error')
    print(f'measurements.shape = {measurements.shape} = '+
          '(n_sensors,n_field_components,n_timesteps)\n')
    print("The truth, systematic error and random error arrays have the same "+
          "shape.")

    print(80*'-')
    print('Looking at the last 5 time steps (measurements) of sensor 0:')
    pyvale.print_measurements(tc_array,
                              (0,1),
                              (0,1),
                              (measurements.shape[2]-5,measurements.shape[2]))
    print(80*'-')
    print("If we call the 'calc_measurements' method then the errors are "+
          "(re)calculated.")
    measurements = tc_array.calc_measurements()

    pyvale.print_measurements(tc_array,
                              (0,1),
                              (0,1),
                              (measurements.shape[2]-5,measurements.shape[2]))


    (_,ax) = pyvale.plot_time_traces(tc_array,field_key)
    ax.set_title('Exp 1: called calc_measurements()')

    print(80*'-')
    print("If we call the 'get_measurements' method then the errors are the "+
          "same:")
    measurements = tc_array.get_measurements()

    pyvale.print_measurements(tc_array,
                              (0,1),
                              (0,1),
                              (measurements.shape[2]-5,measurements.shape[2]))

    (_,ax) = pyvale.plot_time_traces(tc_array,field_key)
    ax.set_title('Exp 2: called get_measurements()')

    print(80*'-')
    print("If we call the 'calc_measurements' method again we generate/sample"+
           "new errors:")
    measurements = tc_array.calc_measurements()

    pyvale.print_measurements(tc_array,
                              (0,1),
                              (0,1),
                              (measurements.shape[2]-5,measurements.shape[2]))

    (_,ax) = pyvale.plot_time_traces(tc_array,field_key)
    ax.set_title('Exp 3: called calc_measurements()')

    print(80*'-')

    plot_on = True
    if plot_on:
        plt.show()


if __name__ == '__main__':
    main()
