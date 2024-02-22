import bpy
import requests
import json


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

#    print("name: ", name)
#    print("country ", country)
#    print("last updated", last_updated)
#    print("Temp C", temp_c) 

    cond = condition["text"]
    nl = "\nl"
    AP = f" {name}{nl}{region}{nl}{country}{nl}localtime {localtime}{nl}Last Updated: {last_updated}{nl}{cond} {nl}Temp C: {temp_c}{nl}Temp F: {temp_f}{nl}Wind KPH: {wind_kph}{nl}Sunlight:(0/1):{is_day}"
    
    ### BLENDER
    font_curve = bpy.data.curves.new(type="FONT", name=(name))
    font_curve.body = AP 
    obj = bpy.data.objects.new(name=(name), object_data=font_curve)

      # -- Set scale and location
    obj.location = (0, 0, 0) # move on the Z axis
    obj.scale = (1, 1, 1)
    bpy.context.scene.collection.objects.link(obj)
    
    #comment this out if you don't want the background node changed
    if (is_day) == 1:
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 1.2
    else:
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.6
    #create_light(is_day)
    pass

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

town = "London"
#town = "Glasgow"
#town = "Dublin"
#town = "Manchester"
#town = "Belfast"
#town = "Berlin"
#town = "Pescara"
#town = "L'Aquila"
#town = "Valletta"

#town = "London"
#town = "Los%Angeles"
#town = "Miami"
#town = "Cairo"
#town = "Moscow"
#town = "Berlin"
#town = "Sydney"
#town = "Hong%Kong"
create_AP(town)
