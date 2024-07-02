'''
================================================================================
Example: 3d thermocouples on a monoblock

pyvale: the python validation engine
License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
from pprint import pprint
from pathlib import Path

import matplotlib.pyplot as plt

import mooseherder as mh
import pyvale


def main() -> None:
    """pyvale example:
    """
    # Use mooseherder to read the exodus and get a SimData object
    data_path = Path('data/examplesims/monoblock_3d_thermal_out.e')
    data_reader = mh.ExodusReader(data_path)
    sim_data = data_reader.read_all_sim_data()

    # Get the string name used for the scalar field in moose: 'temperature'
    field_name = list(sim_data.node_vars.keys())[0] # type: ignore

    # Scale to mm to make 3D visualisation scaling easier
    sim_data.coords = sim_data.coords*1000.0 # type: ignore

    # This creates a grid of 4x1 sensors in the yz plane
    n_sens = (1,4,1)    # Number of sensor (x,y,z)
    x_lims = (11.5,11.5)  # Limits for each coord in sim length units
    y_lims = (-11.5,19.5)
    z_lims = (0.0,12.0)
    sens_pos = pyvale.create_sensor_pos_array(n_sens,x_lims,y_lims,z_lims)

    # Now we create a thermocouple array with with the sensor positions and the
    # temperature field from the simulation
    tc_array = pyvale.SensorArrayFactory \
        .basic_thermocouple_array(sim_data,
                                  sens_pos,
                                  field_name,
                                  spat_dims=3)


    # We can get an array of measurements as follows:
    measurements = tc_array.get_measurements()
    print(f'\nMeasurements for sensor at top of block:\n{measurements[-1,0,:]}\n')

    # Now we use pyvista to get a 3D interactive labelled plot of the sensor
    # locations on our simulation geometry.
    pv_plot = pyvale.plot_sensors_on_sim(tc_array,field_name)

    # Set this to 'interactive' to get an interactive 3D plot of the simulation
    # and labelled sensor locations, set to 'save_fig' to create a vector
    # graphic using a specified camera position.
    pv_plot_mode = 'interactive'

    if pv_plot_mode == 'interactive':
        # Shows the pyvista interactive 3D plot
        pv_plot.camera_position = [(52.198, 26.042, 60.099),
                                    (0.0, 4.0, 5.5),
                                    (-0.190, 0.960, -0.206)]
        pv_plot.show()
        # Once the window is closed we plot the camera position to use later to
        # make a nice graphic for a paper/report
        pprint('Camera positions = ')
        pprint(pv_plot.camera_position)
    if pv_plot_mode == 'save_fig':
        # Determined manually by moving camera and then dumping camera position
        # to console after window close - see 'interactive above'
        pv_plot.camera_position = [(52.198, 26.042, 60.099),
                                    (0.0, 4.0, 5.5),
                                    (-0.190, 0.960, -0.206)]
        # Save a vector graphic to file for our selected camera view
        save_render = Path('examples/monoblock_thermal_sim_view.svg')
        pv_plot.save_graphic(save_render) # only for .svg .eps .ps .pdf .tex
        pv_plot.screenshot(save_render.with_suffix('.png'))

    # Set this to 'interactive' to get a matplotlib.pyplot with the sensor
    # traces plotted over time. Set to 'save_fig' to save an image of the plot
    # to file.
    trace_plot_mode = 'interactive'

    # Plots the sensor time traces using matplotlib, thin solid lines are ground
    # truth from the simulation and dashed lines with '+' are simulated sensor
    # measurements using the specified UQ functions. The sensor traces should
    # have a uniform offset (systematic error) and noise (random error).
    (fig,_) = pyvale.plot_time_traces(tc_array,field_name)

    if trace_plot_mode == 'interactive':
        plt.show()
    if trace_plot_mode == 'save_fig':
        save_traces = Path('examples/monoblock_thermal_traces.png')
        fig.savefig(save_traces, dpi=300, format='png', bbox_inches='tight')


if __name__ == '__main__':
    main()
