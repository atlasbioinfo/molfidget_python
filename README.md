# molfidget

> This library is a fork of https://github.com/longjie0723/molfidget.  
> The main contributions of this project are:  
> - Added a Python entry point so you can run it directly with Python, rather than using Poetry.  
> - The original version always launched the GUI by default; I have added an option to make the GUI optional.


### Requirements

* Python 3.10 or higher
* You can use conda to install Python 3.10: `conda install python=3.10`
* Dependencies

```
pip install scipy trimesh manifold3d "pyglet<2" pyyaml
```
### Usage

```
python run_molfidget.py --scale 10.0 --shaft-gap 0.2 pdb/thermosupermin.pdb
```

### Parameters

- `file_name` (required): PDB or MOL file to load
- `--scale` (optional, default: 10.0): Molecule scale factor. The original model units are in Angstroms, so scale=1.0 would make the STL file extremely small. Use scale=10.0 or similar for printable STL files.
- `--shaft-gap` (optional, default: 0.2): Shaft gap in mm. The gap between the movable shaft and hole. For normal 3D printers, 0.2~0.3 range should work fine.
- `--output-dir` (optional, default: 'output'): STL files output directory
- `--show-gui` (optional): Show GUI (requires display environment). Press 'q' key to exit preview.

### Output

* Corresponding STL files will be generated in the specified output directory
* Files include: molecule.stl, molecule.ply, individual atom STL files, and config.yaml
