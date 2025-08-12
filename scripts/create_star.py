import bpy
import math

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create star shape as a mesh (simple example using cones)
def create_star(location=(0,0,0), size=1):
    verts = []
    faces = []

    # Create points for a 5-point star in 2D, then extrude to 3D
    angle = math.pi / 5
    for i in range(10):
        r = size if i % 2 == 0 else size / 2
        x = r * math.cos(i * angle)
        y = r * math.sin(i * angle)
        verts.append((x, y, 0))
    faces.append(list(range(10)))

    # Create mesh and object
    mesh = bpy.data.meshes.new("StarMesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    star_obj = bpy.data.objects.new("Star", mesh)
    bpy.context.collection.objects.link(star_obj)

    # Extrude star to give thickness
    bpy.context.view_layer.objects.active = star_obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value":(0, 0, size/3)})
    bpy.ops.object.mode_set(mode='OBJECT')

    star_obj.location = location

    # Add material (yellow emission)
    mat = bpy.data.materials.new(name="StarMaterial")
    mat.use_nodes = True
    emission = mat.node_tree.nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (1, 1, 0, 1)  # Yellow
    emission.inputs['Strength'].default_value = 5
    mat.node_tree.links.new(
        emission.outputs['Emission'], 
        mat.node_tree.nodes['Material Output'].inputs['Surface'])
    star_obj.data.materials.append(mat)

    return star_obj

# Setup camera
camera = bpy.data.objects.get('Camera')
if not camera:
    bpy.ops.object.camera_add(location=(0, -5, 2), rotation=(1.1, 0, 0))
    camera = bpy.context.active_object
camera.location = (0, -5, 2)
camera.rotation_euler = (1.1, 0, 0)

# Setup light
light = bpy.data.objects.get('Light')
if not light:
    bpy.ops.object.light_add(type='POINT', location=(0, -3, 5))
    light = bpy.context.active_object
light.data.energy = 1000

# Create the star object
create_star()

# Render settings
bpy.context.scene.render.engine = 'CYCLES'  # Or 'BLENDER_EEVEE'
bpy.context.scene.render.filepath = "//../assets/star.png"
bpy.context.scene.render.resolution_x = 512
bpy.context.scene.render.resolution_y = 512

# Render and save image
bpy.ops.render.render(write_still=True)
