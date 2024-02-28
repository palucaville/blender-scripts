#### platform_internals.py
#### Blender script to get informations about the host computer using the "patform" and "psutil" modules.
#### Network name, Ram usage, CPU type/cores/frequency, OS type/version.
####
import bpy
import platform
import random
import psutil

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

nl =  ' \n '
internals = platform.uname()
nname = (f"Net name: {platform.node()[:15]}") #hostname
cpu_type = (f"Processor type: {platform.processor()}")
os_cc = (f"Sys OS:  {platform.system()}")
os_dd = (f"OS release: {platform.release()}")
os_vv = (f"OS version: {platform.version()[:15]}")

ff = platform.python_compiler()
gg = platform.python_implementation()
hh = platform.python_version()
#Physical cores
phy_cores = psutil.cpu_count(logical=False)
#Logical cores
log_cores = psutil.cpu_count(logical=True)
CPU_freq = psutil.cpu_freq().current
inst_RAM = (f"RAM installed: {round(psutil.virtual_memory().total/1000000000, 2)} GB")
avail_RAM = (f"Available RAM: {round(psutil.virtual_memory().available/1000000000, 2)} GB")
used_RAM = (f"Used RAM: {round(psutil.virtual_memory().used/1000000000, 2)} GB")
usage_RAM =(f"RAM usage: {psutil.virtual_memory().percent}%")

BB = f'{nname}{nl}{avail_RAM}{nl}{used_RAM}{nl}{usage_RAM}{nl}{os_cc}{nl}{os_dd}{nl}{os_vv}{nl}Compiler: {ff}{nl}Python ver: {hh}{nl}Implement: {gg}{nl}{cpu_type}{nl}CPU frequency: {round(CPU_freq)}{nl}CPU cores:{phy_cores}{nl}Logic cores: {log_cores}{nl}{inst_RAM}{nl}'

#print (BB)
### BLENDER  
font_curve = bpy.data.curves.new(type="FONT", name=("internals"))
font_curve.body = BB 
obj = bpy.data.objects.new(name=("internals"), object_data=font_curve)
obj.location = (-30, 10, 5)
obj.scale = (1.5, 1.5, 1.5)
bpy.context.scene.collection.objects.link(obj)
random_material = create_random_material()
obj.data.materials.append(random_material)
push_scene()
bpy.ops.object.select_all(action='DESELECT')
