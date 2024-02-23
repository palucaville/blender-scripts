

## weather.py   fetch weather info (temp, wind, conditions) of a given town.
# draw the info using temperature as Z axis and wind speed as Y axis.
# create and assigb a random material.

import bpy
import requests
import json
import random
from mathutils import Color


def get_response(place):
    
    url = "https://api.weatherapi.com/v1/current.json?key=MYAPIKEY"
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
        if key in "temp_f":
            temp_f = (current[key])
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

    cond = condition["text"]
    nl = "\nl"
    ## put together the string to pass to Blender
    AP = f" {name}{nl}{region}{nl}{country}{nl}localtime {localtime}{nl}Updated: {last_updated}{nl}{cond} {nl}Temp C: {temp_c}{nl}{nl}Wind KPH: {wind_kph}{nl}Sunlight:(0/1):{is_day}"
    
    ### BLENDER
    font_curve = bpy.data.curves.new(type="FONT", name=(name))
    font_curve.body = AP 
    obj = bpy.data.objects.new(name=(name), object_data=font_curve)

      # -- Set scale and location
    newYZ = (temp_c)
    newX = (wind_kph)/2
    obj.location = ((newX), 0, (newYZ)) # move on the Z axis reprenting temperature
    obj.scale = (1, 1, 1)
    
    bpy.context.scene.collection.objects.link(obj)
    random_material = create_random_material()
    #selected_objects = bpy.context.selected_objects
    #bpy.ops.transform.translate(value=(0, -1, -5))
    # Assign the random material to all selected objects
    #for obj in selected_objects:
    if obj.type == 'FONT':
        if obj.data.materials:
            # If the object already has materials, replace the first one with the random material
            obj.data.materials[0] = random_material
        else:
            # If the object doesn't have any materials, create a new one and assign it
            obj.data.materials.append(random_material)
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
 
#    #comment this out if you don't want the background node changed
#    if (is_day) == 1:
#        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 1.2
#    else:
#        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.6
#    #create_light(is_day)
#    pass

#def create_light(isday):
#    
#    # create light datablock, set attributes
#    light_data = bpy.data.lights.new(name="light_2", type='POINT')
#    if (isday) == 1:
#            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 1.2

#    else:
#            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.6
# 
#    # create new object with our light datablock
#    light_object = bpy.data.objects.new(name="daylight", object_data=light_data)
#    # link light object
#    bpy.context.collection.objects.link(light_object)
#    # make it active 
#    bpy.context.view_layer.objects.active = light_object
#    #change location
#    light_object.location = (2, 2, 5)

#    # update scene, if needed
#    dg = bpy.context.evaluated_depsgraph_get() 
#    dg.update()
#    pass

#town = "London"
#town = "New%York"
#town = "Dublin"
#town = "Berlin"
#town = "Valletta"
#town = "Los%Angeles"
#town = "Miami"
#town = "Cairo"
town = "Mexico%City"
create_AP(town)
 
###  or all together
#
#towns =("London","Beijing","Berlin","New%York","Seattle","Los%Angeles","Cairo","Moscow","Sydney","Seoul","Kyoto","Rome","Mexico%City","Reykjavik")
#for town in towns:
#    create_AP(town)



bpy.ops.object.select_all(action='DESELECT')
