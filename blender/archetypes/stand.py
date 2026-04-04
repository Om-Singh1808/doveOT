import bpy
import math

def generate_stand(params: dict):
    """
    Parametric phone/tablet stand generator based on MVP vibe parameters.
    Returns the final Blender object.
    """
    # 1. Base Parameters
    # We use some of the vibe dimensions directly
    softness = params.get("softness", 0.5)
    weight = params.get("weight", 0.5)
    height_ratio = params.get("height_ratio", 0.5)
    
    # Calculate geometric properties
    stand_angle = 50 + (30 * params.get("fluidity", 0.5))  # 50 to 80 degrees
    thickness = 2.0 + (3.0 * weight)                      # 2mm to 5mm
    base_width = 60.0 + (30.0 * weight)                   # 60mm to 90mm
    z_scale = 0.5 + (2.0 * height_ratio)                  # 0.5 to 2.5 multiplier for height
    extrude_depth = 80.0                                  # mm width of the stand
    
    # Start fresh curve
    curve_data = bpy.data.curves.new("StandProfile", type='CURVE')
    curve_data.dimensions = '2D'
    curve_data.extrude = extrude_depth / 2.0  # Extrudes symmetrically
    
    spline = curve_data.splines.new('BEZIER')
    
    # Points defining the L/V shape of the stand (from side view)
    base_length = 50.0 * z_scale
    back_length = 80.0 * z_scale
    lip_length = 15.0
    
    # Start: Tip of the lip
    p0 = (0, lip_length, thickness)
    # Cradle bottom
    p1 = (0, 0, thickness)
    # Back rest angle calculation
    # Convert angle to radians
    angle_rad = math.radians(stand_angle)
    p2_y = -base_length
    p2_z = thickness + (math.sin(angle_rad) * back_length)
    p2 = (0, p2_y, p2_z)
    
    points = [p0, p1, p2]
    spline.bezier_points.add(len(points) - 1)
    
    for i, p in enumerate(points):
        bp = spline.bezier_points[i]
        bp.co = p
        bp.handle_left_type = 'AUTO'
        bp.handle_right_type = 'AUTO'
    
    stand_obj = bpy.data.objects.new("VibeStand", curve_data)
    bpy.context.collection.objects.link(stand_obj)
    
    # Convert curve to mesh to apply modifiers like solidify/bevel
    bpy.context.view_layer.objects.active = stand_obj
    stand_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    
    # Solidify (give it thickness)
    solidify = stand_obj.modifiers.new("Solidify", 'SOLIDIFY')
    solidify.thickness = thickness
    solidify.offset = 0  # center
    
    # Apply Solidify before Bevel to have real geometry
    bpy.ops.object.modifier_apply(modifier="Solidify")
    
    # Bevel (controlled by softness)
    if softness > 0.1:
        bevel = stand_obj.modifiers.new("Bevel", 'BEVEL')
        bevel.segments = int(softness * 10) + 2
        bevel.width = softness * 5.0  # max 5mm fillet
        bevel.limit_method = 'ANGLE'
        bpy.ops.object.modifier_apply(modifier="Bevel")
        
    # Rotate to sit flat on build plate (Z=0)
    # Simplest way is to ensure bounding box minimum Z is 0 after generation
    # But for a basic stand, we already started around Z=thickness.
    
    return stand_obj
