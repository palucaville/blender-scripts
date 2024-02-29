# connect and authenticate to the TOR Control port 9051.
# get a new TOR identity (node). Display a timestamp

import bpy
import time
import random
from datetime import datetime

from stem import Signal
from stem.control import Controller

def create_random_material():
    # Create a new material
    material = bpy.data.materials.new(name="Random Material")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    #  diffuse shader node
    diffuse = nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuse.location = (0, 0)
    output = nodes.new(type='ShaderNodeOutputMaterial')
    output.location = (200, 0)
    links = material.node_tree.links
    link = links.new(diffuse.outputs['BSDF'], output.inputs['Surface'])
    # random color for the diffuse node
    diffuse.inputs['Color'].default_value = [random.random() for _ in range(3)] + [1]  # RGBA format
    return material  

def push_scene():
    # Get the active collection
    active_collection = bpy.context.collection
    # Select all objects in the collection
    for obj in active_collection.objects:
        obj.select_set(True)
    # Move the selected objects 5 units on the y-axis
    bpy.ops.transform.translate(value=(0, 0, -5))

push_scene()
with Controller.from_port(port = 9051) as controller:
    controller.authenticate("torpassword")

    bytes_read = controller.get_info("traffic/read")
    bytes_written = controller.get_info("traffic/written")
    nl = " \nl "
    datt = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    dt =str(datt)
    tor_info = f'{dt}{nl} Tor has read {bytes_read} bytes{nl} and written {bytes_written} bytes{nl} new tor node requested. {nl} Give it a minute...'

#   # switch to new circuits, so new application requests don't share 
    #any circuits with old ones (this also clears our DNS cache)
    controller.signal(Signal.NEWNYM)
    print("new tor node requested...")
    
    ##reload torc config file
    #controller.signal(Signal.HUP)
### BLENDER     
    font_curve = bpy.data.curves.new(type="FONT", name=(dt))
    font_curve.body = tor_info 
    obj = bpy.data.objects.new(name=(dt), object_data=font_curve)
    obj.location = (-1, 0, 0 )
    obj.scale = (1, 1, 1)
   
    bpy.context.scene.collection.objects.link(obj)
    random_material = create_random_material()
    obj.data.materials.append(random_material)
    bpy.ops.object.select_all(action='DESELECT')
