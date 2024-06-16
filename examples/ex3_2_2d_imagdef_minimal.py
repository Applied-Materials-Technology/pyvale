"""
================================================================================
pyvale: the python computer aided validation engine

License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
"""

from pprint import pprint
from pathlib import Path

import numpy as np

import mooseherder as mh

from pyvale.imagesim.imagedefopts import ImageDefOpts
from pyvale.imagesim.cameradata import CameraData
import pyvale.imagesim.imagedef as sid


def main() -> None:
    print()
    print('='*80)
    print('PYVALE EXAMPLE: IMAGE DEFORMATION 2D MINIMAL')
    print('='*80)
    # This example assumes no experimental image is provided and a masked one
    # needs to be generated from a full speckled image using the simulation data.
    # This example also deals with complex geometry including holes and notches

    im_path = Path('data/speckleimages')
    im_file = 'OptimisedSpeckle_2464_2056_width5.0_8bit_GBlur1.tiff'
    im_path = im_path / im_file

    print(f'\nLoading image to deform from path:{im_path}\n')
    input_im = sid.load_image(im_path)

    case_str = 'case17'
    sim_path = Path(f'simcases/{case_str}')
    sim_file = f'{case_str}_out.e'

    print(f'\nLoading SimData from exodus in path:\n{sim_path}')

    exodus_reader = mh.ExodusReader(sim_path / sim_file)
    sim_data = exodus_reader.read_all_sim_data()

    print('\nSetting up image deformation inputs.\n')

    # We require the following variables to run the image deformation:
    # - input_im 2D numpy array of floats which is the input image to deform
    # - coords is a Nx2 numpy array where N is the number of nodes in the ROI
    #   with the nodal coords as [X,Y]
    # - disp_x is a NxF numpy array where N is the number of nodes and F is the
    #   is the number of frames/time steps with displacements in 'm'
    # - disp_y as above but the y directions displacements
    # - ImageDefOpts class - see below
    # - CameraData class - see below

    # Could also just extract a sideset here logical indexing
    if sim_data.coords is not None:
        coords = sim_data.coords
    if sim_data.node_vars is not None:
        disp_x = sim_data.node_vars['disp_x']
        disp_y = sim_data.node_vars['disp_y']

    del sim_data # don't need this anymore so can get rid of it

    id_opts = ImageDefOpts()
    id_opts.save_path = sim_path / 'deformed_images'
    id_opts.mask_input_image = True
    id_opts.def_complex_geom = True
    id_opts.crop_on = True
    id_opts.crop_px = np.array([1000,1600])
    id_opts.calc_res_from_fe = True
    id_opts.calc_res_border_px = 10
    id_opts.add_static_ref = 'off'

    print('\n'+'-'*80)
    print('ImageDefOpts:')
    pprint(vars(id_opts))
    print('-'*80+'\n')

    camera = CameraData()
    camera.num_px = id_opts.crop_px
    camera.bits = 8
    if id_opts.calc_res_from_fe:
        camera.m_per_px = sid.calc_res_from_nodes(camera,coords, #type: ignore
                                             id_opts.calc_res_border_px)
    (camera.roi_len,camera.coord_offset) = sid.calc_roi_from_nodes(camera,coords)

    print('-'*80)
    print('CameraData:')
    pprint(vars(camera))
    print('-'*80)
    print('')

    #---------------------------------------------------------------------------
    # Pre-process and the deform images
    sid.deform_images(input_im,
                    camera,
                    id_opts,
                    coords,
                    disp_x,
                    disp_y,
                    print_on = True)


if __name__ == "__main__":
    main()

