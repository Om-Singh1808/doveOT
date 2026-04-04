import bpy
import sys
import argparse
import json

import os
# Add the blender scripts dir to sys.path so we can import archetypes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from archetypes.stand import generate_stand

def cleanup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", required=True, help="Path to JSON parameters file")
    parser.add_argument("--output", required=True, help="Path to output STL")
    
    # Blender passes everything after "--" to the script
    argv = sys.argv
    if "--" not in argv:
        argv = []
    else:
        argv = argv[argv.index("--") + 1:]
        
    args = parser.parse_args(argv)
    
    with open(args.params, "r") as f:
        params = json.load(f)
        
    cleanup_scene()
    
    # Generate based on archetype
    archetype = params.get("archetype", "stand")
    if archetype == "stand":
        obj = generate_stand(params)
    else:
        print(f"Archetype '{archetype}' not implemented, falling back to stand")
        obj = generate_stand(params)
        
    if not obj:
        raise ValueError(f"Failed to generate geometry for {archetype}")
        
    # Setup for export
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    bpy.ops.export_mesh.stl(
        filepath=args.output,
        use_selection=True,
        global_scale=1.0,
        use_scene_unit=False
    )
    print(f"Successfully exported {args.output}")

if __name__ == "__main__":
    main()
