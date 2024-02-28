import bpy
import requests
import json
import socks
import socket
import random


def run_n_times():
    
    push_scene() # move everything
    get_internals()

    # Make a request through the Tor connection
    # print IP visible through Tor
    session = get_tor_session()
    tor_ip = (session.get("http://httpbin.org/ip").json())["origin"]
    #print("tor IP address",tor_ip)

    tor_ip_info = get_torip_info(session,tor_ip)
    AP = create_AP(tor_ip_info)
### BLENDER     
    font_curve = bpy.data.curves.new(type="FONT", name=(tor_ip))
    font_curve.body = AP 
    obj = bpy.data.objects.new(name=(tor_ip), object_data=font_curve)
    obj.location = (-10, 0, 0 )
    obj.scale = (1, 1, 1)
   
    bpy.context.scene.collection.objects.link(obj)
    random_material = create_random_material()
    obj.data.materials.append(random_material)

#    ## CAREFUL!!!  public IP NON-tor !!!
    pub_ip = (requests.get("http://httpbin.org/ip").json())["origin"]
    #print("public IP address ",pub_ip)
    pub_ip_info = get_ip_info(pub_ip)
    AP2 = create_AP(pub_ip_info)


    
### BLENDER
    font_curve = bpy.data.curves.new(type="FONT", name=(pub_ip))
    font_curve.body = AP2 
    obj2 = bpy.data.objects.new(name=(pub_ip), object_data=font_curve)
    obj2.location = (2, 0 , 0 )
    obj2.scale = (1, 1, 1)
    
    bpy.context.scene.collection.objects.link(obj2)
    random_material = create_random_material()
    obj2.data.materials.append(random_material)
 #    ## END  public IP NON-tor       
    
    bpy.context.view_layer.update()

    #draw_dt(counter)


def get_torip_info(session,raw_ip):
    try:
        ipify = session.get("https://geo.ipify.org/api/v2/country,city?apiKey=MYAPILEYL")
        return (ipify.json())
    except requests.RequestException:
        print("Exception occurred: ")

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def create_AP(info):
    e = (info['ip'])
    f = (info['location']['geonameId'])
    g = (info['location']['city'])  
    h = (info['location']['country'])
    i = (info['location']['region'])
    l = (info['location']['timezone'])
    m = (info['isp'])
    nl =  ' \n '
    AP = f'{e}{nl}GeonameId: {f}{nl}City: {g}{nl}Country: {h}{nl}Region: {i}{nl}Timezone: {l}{nl}ISP: {m}{nl}'
    return (AP)
    #own["AP"] = (ap)
    #print (AP)
    #own["Text"] = (own["AP"])

def get_internals():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")


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



## CAREFUL!!!  public IP NON-tor below. Is VPN ON???!!!
## CAREFUL!!!  public IP NON-tor below!!!
def get_ip_info(raw_ip):
    try:
        ipify = requests.get("https://geo.ipify.org/api/v2/country,city?apiKey=MYAPIKEY")
        return (ipify.json())
    except requests.RequestException:
        print("Exception occurred: ")

### CAREFUL!!!  public IP NON-tor !!!  Is VPN ON?

# Get the active scene
scene = bpy.context.scene
run_n_times()
bpy.ops.object.select_all(action='DESELECT')
