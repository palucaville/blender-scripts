import bpy# this is needed and usually NOT included in standard python
from mathutils import Color
import random
import requests




#font_id = blf.load("path/to/your/font.ttf")  # Replace with your font path
def get_chuck():
    url = "https://api.chucknorris.io/jokes/random"
    querystring = {"query":"value"}
    headers = {"accept": "application/json"}
    raw = requests.get(url, headers=headers, params=querystring)
    line =(raw.json()['value'])

    chunk_size = 44
    new_lines = "\n".join(line[i:i+chunk_size] for i in range(0, len(line), chunk_size))
    print(new_lines)

    font_curve = bpy.data.curves.new(type="FONT", name="ChuckNorris")
    font_curve.body = new_lines
    obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    obj.location = (0, 0.5, 0.1) # move on the Z axis
    obj.scale = (0.75, 0.5, 0.5)
    bpy.context.scene.collection.objects.link(obj)

# Get the active scene
scene = bpy.context.scene

get_chuck()
bpy.ops.object.select_all(action='SELECT')
selected_objects = bpy.context.selected_objects
bpy.ops.transform.translate(value=(0, -1, -5))
bpy.context.view_layer.update()

bpy.ops.object.select_all(action='DESELECT')