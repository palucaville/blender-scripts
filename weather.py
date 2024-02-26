
## weather.py   fetch weather info (temp, wind, conditions) of a given town.
# draw the info using temperature as Z axis and wind speed as Y axis.
# create and assign a random material.

import bpy
import requests
import json
import random
from mathutils import Color
from datetime import datetime

def get_response(place):
    
    url = "https://api.weatherapi.com/v1/current.json?key=getyourownkey"
    header = {"accept": "application/json"}
    query = {"q":(place)} # use % if need blank space
    response = requests.get(url, query)
    return (response.json())

def create_AP(place):
    current = (get_response(place)["current"])
    location = (get_response(place)["location"])

    for key in current:
        if key in "condition":
            condition = (current[key])
        if key in "is_day":
            is_day = (current[key])
        if key in "temp_c":
            temp_c = (current[key])
        if key in "humidity":
            humidity = (current[key])
        if key in "wind_kph":
            wind_kph = (current[key])
        if key in "last_updated":
            last_updated = (current[key])
        if key in "localtime":
            localtime = (current[key])

    for key in location:
        if key in "name":
            name = (location[key])
        if key in "region":
            region = (location[key])
        if key in "country":
            country = (location[key])
        if key in "localtime":
            localtime = (location[key])
        if key in "tz_id":
            tz_id = (location[key])
    cond = condition["text"]
    nl = "  \nl  "
      # Getting the current date and time
    datt = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    dt =str(datt)
    ## put together the string to pass to Blender
    AP = f" {name}{nl}{nl}{region}{nl}{country}{nl}Timezone: {tz_id}{nl}Sys time: {dt}{nl}localtime {localtime}{nl}Updated: {last_updated}{nl}{cond} {nl}Temp C: {temp_c}{nl}Wind KPH: {wind_kph}{nl}Humidity: {humidity}%"
    
    ### BLENDER
    font_curve = bpy.data.curves.new(type="FONT", name=(name))
    font_curve.body = AP 
    obj = bpy.data.objects.new(name=(name), object_data=font_curve)

      # -- Set scale and location
    newZ = (temp_c)
    newX = (wind_kph)/2.5
    
    obj.location = ((newX), 0, (newZ))
    obj.scale = (1, 1, 1)
    bpy.context.scene.collection.objects.link(obj)
    random_material = create_random_material()
    obj.data.materials.append(random_material)
    
    # Create a new cube

    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.object
    cube.location = (0, 0, (newZ))
    cube.scale =(0.5, 0.5, 0.1)
    cube.data.materials.append(random_material)
    bpy.context.object.name = (name)
    # Update the view
    bpy.context.view_layer.update()

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
 
town = "London"
create_AP(town)
 
###  or all together
#
#towns =("Anchorage","London","Beijing","Berlin","New%York","Seattle","Los%Angeles","Cairo","Moscow","Sydney","Seoul","Kyoto","Rome","Mexico%City","Reykjavik")
#for town in towns:
#    create_AP(town)



bpy.ops.object.select_all(action='DESELECT')
