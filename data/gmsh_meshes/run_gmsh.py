'''
================================================================================
pycave: the python computer aided validation engine

License: MIT
Copyright (C) 2024 The Computer Aided Validation Team
================================================================================
'''
from pathlib import Path
import time
import mooseherder as mh

def main() -> None:
    gmsh_path = Path().home() / 'moose-workdir/gmsh/bin/gmsh'
    gmsh_runner = mh.GmshRunner(gmsh_path)

    base_dir = Path('data/gmsh_meshes/')
    gmsh_in = base_dir / 'monoblock_3d.geo'
    gmsh_runner.set_input_file(gmsh_in)

    start_time = time.perf_counter()
    gmsh_runner.run()
    run_time = time.perf_counter() - start_time

    print()
    print("="*80)
    print(f'Gmsh run time = {run_time:.3f} seconds')
    print("="*80)
    print()


if __name__ == '__main__':
    main()