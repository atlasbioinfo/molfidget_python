#!/usr/bin/env python3
"""
Directly call molfidget using Python, replacing command line calls
Equivalent to: poetry run molfidget --scale 10.0 --shaft-gap 0.2 pdb/ethanol.pdb
"""

import os
import sys
import argparse
import dataclasses
import yaml
from molfidget.molfidget import Molecule, ShapeConfig

def run_molfidget(file_name, scale=10.0, shaft_gap=0.2, output_dir='output', show_gui=False):
    """
    Directly call molfidget functionality
    
    Args:
        file_name (str): PDB or MOL file path
        scale (float): Scale factor
        shaft_gap (float): Shaft gap
        output_dir (str): Output directory
        show_gui (bool): Whether to show GUI
    """
    # Create configuration
    config = ShapeConfig()
    config.scale = scale
    config.shaft_gap = min(0.05, shaft_gap / scale)
    
    # Create molecule object
    molecule = Molecule()
    
    # Load file
    if file_name.endswith(".pdb"):
        molecule.load_pdb_file(file_name)
    elif file_name.endswith(".mol"):
        molecule.load_mol_file(file_name)
    else:
        raise ValueError(f"Unsupported file format: {file_name}. Please provide .pdb or .mol file.")
    
    # Create 3D scene
    scene = molecule.create_trimesh_scene(config)
    
    # Only show GUI when display environment is available and user requests it
    if show_gui:
        try:
            import pyglet
            from molfidget.labeled_scene_viewer import LabeledSceneViewer
            viewer = LabeledSceneViewer(scene)
            pyglet.app.run()
        except Exception as e:
            print(f"Unable to start GUI: {e}")
            print("Continuing with file processing...")
    
    # Save output files
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    scene.export(os.path.join(output_dir, "molecule.stl"))
    scene.export(os.path.join(output_dir, "molecule.ply"))
    
    molecule.save_stl_files(config, output_dir=output_dir)
    print(f"Loaded {len(molecule.atoms)} atoms from {file_name}")
    
    molecule.merge_atoms()
    molecule.save_group_stl_files(config, output_dir=output_dir)
    
    # Save configuration file
    config_data = dataclasses.asdict(config)
    config_data["file_name"] = file_name
    with open(os.path.join(output_dir, "config.yaml"), 'w') as file:
        yaml.dump(config_data, file, default_flow_style=False)
    
    print(f"Files saved to: {output_dir}")
    
    return molecule, scene

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Molecule visualization and processing")
    parser.add_argument("file_name", type=str, help="PDB or MOL file to load")
    parser.add_argument("--scale", type=float, default=10.0, help="Molecule scale factor (default: %(default)s)")
    parser.add_argument("--shaft-gap", type=float, default=0.2, help="Shaft gap [mm] (default: %(default)s)")
    parser.add_argument("--output-dir", type=str, default='output', help="STL files output directory (default: %(default)s)")
    parser.add_argument("--show-gui", action="store_true", help="Show GUI (requires display environment)")
    
    args = parser.parse_args()
    
    # Run molfidget
    molecule, scene = run_molfidget(
        args.file_name, 
        scale=args.scale, 
        shaft_gap=args.shaft_gap, 
        output_dir=args.output_dir,
        show_gui=args.show_gui
    )