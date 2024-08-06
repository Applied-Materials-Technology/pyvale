'''
================================================================================
example: thermocouples on a 2d plate

pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
from pprint import pprint
from typing import Any
from pathlib import Path
import matplotlib.pyplot as plt
import mooseherder as mh
import pyvale
import numpy as np
import pandas as pd


def print_attrs(in_obj: Any) -> None:
    _ = [print(aa) for aa in dir(in_obj) if '__' not in aa]

def main() -> None:
    # Use mooseherder to read the exodus and get a SimData object
    data_path = Path('data/examplesims/plate_2d_thermal_out.e')
    data_reader = mh.ExodusReader(data_path)
    sim_data = data_reader.read_all_sim_data()

    # Create a Field object that will allow the sensors to interpolate the sim
    # data field of interest quickly by using the mesh and shape functions
    spat_dims = 2       # Specify that we only have 2 spatial dimensions
    field_name = 'temperature'    # Same as in the moose input and SimData node_var key
    t_field = pyvale.Field(sim_data,field_name,spat_dims)

    # This creates a grid of 3x2 sensors in the xy plane
    n_sens = (3,2,1)    # Number of sensor (x,y,z)
    x_lims = (0.0,2.0)  # Limits for each coord in sim length units
    y_lims = (0.0,1.0)
    z_lims = (0.0,0.0)
    # Gives a n_sensx3 array of sensor positions where each row is a sensor with
    # coords (x,y,z) - can also just manually create this array
    sens_pos = pyvale.create_sensor_pos_array(n_sens,x_lims,y_lims,z_lims)

    # Now we create a thermocouple array with with the sensor positions and the
    # temperature field from the simulation
    tc_array = pyvale.ThermocoupleArray(sens_pos,t_field)

    # Setup the UQ functions for the sensors. Here we use the basic defaults
    # which is a uniform distribution for the systematic error which is sampled
    # once and remains constant throughout the simulation time creating an
    # offset. The max temp in the simulation is ~200degC so this range [lo,hi]
    # should be visible on the time traces.
    tc_array.set_uniform_systematic_err_func(low=-10.0,high=10.0)
    # The default for the random error is a normal distribution here we specify
    # a standard deviation which should be visible on the time traces. Note that
    # the random error is sampled repeatedly for each time step.
    tc_array.set_normal_random_err_func(std_dev=5.0)

    measurements = tc_array.get_measurements()

    # Now we use pyvista to get a 3D interactive labelled plot of the sensor
    # locations on our simulation geometry.
    pv_sens = tc_array.get_visualiser()
    pv_sim = t_field.get_visualiser()
    pv_plot = pyvale.plot_sensors(pv_sim,pv_sens,field_name)
    # We label the temperature scale bar ourselves and can
    pv_plot.add_scalar_bar('Temperature, T [degC]')
    
    save_vals = True
    
    if save_vals:
        print_attrs(sim_data)
        print()
        read_config = data_reader.get_read_config()
        print()
        print('Attributes of SimReadConfig:')
        print_attrs(read_config)
        print()
        sim_data = data_reader.read_sim_data(read_config)
        #print(measurements)
        #print(f'sim_data.time = {sim_data.time}')
        #print(f'sim_data.coords = {sim_data.coords}')
        #print(f'sim_data.connect = {sim_data.connect}')
        #print(sim_data.connect['connect1'])
        #print()
        #print(sens_pos.shape)
        #print(measurements.shape)
        #print(sim_data.time.shape)
        sens_pos_df = pd.DataFrame(sens_pos)
        sens_data = np.concatenate([np.reshape(sim_data.time,(1,len(sim_data.time))),measurements])
        sens_data = np.transpose(sens_data)
        columns = ["time"]
        for i in range(measurements.shape[0]):
            columns.append(f"s{i+1}")
        sens_data_df = pd.DataFrame(sens_data,columns=columns)
        print(sens_data_df)
        file_path = Path('examples/images/sim_data.csv')
        sens_data_df.to_csv(file_path,columns=columns,index=False)
        


    # Set this to 'interactive' to get an interactive 3D plot of the simulation
    # and labelled sensor locations, set to 'save_fig' to create a vector
    # graphic using a specified camera position.
    pv_plot_mode = None#'interactive'#

    if pv_plot_mode == 'interactive':
        # Shows the pyvista interactive 3D plot
        pv_plot.show()
        # Once the window is closed we plot the camera position to use later to
        # make a nice graphic for a paper/report
        pprint('Camera positions = ')
        pprint(pv_plot.camera_position)
    if pv_plot_mode == 'save_fig':
        # Determined manually by moving camera and then dumping camera position
        # to console after window close - see 'interactive above'
        pv_plot.camera_position = [(-0.295, 1.235, 3.369),
                                (1.0274, 0.314, 0.0211),
                                (0.081, 0.969, -0.234)]
        # Save a vector graphic to file for our selected camera view
        save_render = Path('examples/images/plate_thermal_2d_sim_view.svg')
        pv_plot.save_graphic(save_render) # only for .svg .eps .ps .pdf .tex
        pv_plot.screenshot(save_render.with_suffix('.png'))
    if pv_plot_mode == None:
        pv_plot.close()

    # Set this to 'interactive' to get a matplotlib.pyplot with the sensor
    # traces plotted over time. Set to 'save_fig' to save an image of the plot
    # to file.
    trace_plot_mode = None#'interactive'#

    # Plots the sensor time traces using matplotlib, thin solid lines are ground
    # truth from the simulation and dashed lines with '+' are simulated sensor
    # measurements using the specified UQ functions. The sensor traces should
    # have a uniform offset (systematic error) and noise (random error).
    (fig,ax) = tc_array.plot_time_traces(plot_truth=True)
    if trace_plot_mode == 'interactive':
        plt.show()
    if trace_plot_mode == 'save_fig':
        save_traces = Path('examples/images/plate_thermal_2d_traces.png')
        fig.savefig(save_traces, dpi=300, format='png', bbox_inches='tight')
    if trace_plot_mode == None:
        plt.close()


if __name__ == '__main__':
    main()
