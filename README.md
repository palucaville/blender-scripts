## **insult.py**

Blender 3.6 python script using evilinsult.com/ API to 
fetch random insults, create text objects and add a timestamp

https://www.youtube.com/watch?v=R07Uy_3S9D8


## **chucknorris_fact.py**

Blender 3.6 script fetching from api.chucknorris.io/jokes/random
Text get formatted (sliced) and then turned into a text object


## **weather.py**

A Blender 3.6 script fetching from api.weatherapi.com/v1/current.json
fetch weather info (temp, wind, conditions) of a given town.
draw the info using temperature as Z axis and wind speed as Y axis.
create and assign a random material.

[https://youtu.be/8AZPu8Egmvo](https://youtu.be/P-3MIEQzlt8)


## **geolocate.py**

Blender 3.6 script to get and display:
the Public IP calling "httpbin.org/ip" and then "geo.ipify.org/api/v2/country,city?apikey" 
the TOR IP address and info using socket session with "requests" 127.0.0.1:9050

[https://youtu.be/0WZZvzC5zZE](https://youtu.be/0WZZvzC5zZE) (geolocate and internals)
 
## **platform_internals.py**

Blender script to get informations about the host computer using the "patform" and "psutil" modules.
Network name, Ram usage, CPU type/cores/frequency, OS type/version.
