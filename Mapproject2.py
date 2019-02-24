"""

# -*- coding: utf-8 -*-
Created on          27 Jan 2019 at 5.55 PM
@author:            Arvind Sachidev Chilkoor
Created using:      PyCharm
Name of Project:    World Map Project - Interactive




This project demonstrates the use of folium library and displaying an interactive world map with geolocation markers
indicating locations of volcanoes in USA, also world population data of all countries.
The program also allows the user to do a web search of the volcanoes.
The program also provides the user with map layers, where the user can turn on/off the various layers from the base map
"""





import folium
import pandas
import json
from html import escape

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])                 # convert Latitude points from file into a List
lon = list(data["LON"])                 # convert Longitude points from file into a List
elev = list(data["ELEV"])               # convert elevation data from file into a list
nam = list(data["NAME"])                # convert names of mountains from file into a list
loca = list(data["LOCATION"])           # convert location of mountains from file into a list
typ = list(data["TYPE"])                # convert location of Type from file into a list


# HTML code for highlighting the name of the volcano in the pop-up and do a google search #
html = """
Name of the Volcano:-<br/>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br/>
Location:- %s<br/>
Elevation:- %s meters<br/>
Type of Volcano:- %s<br/>
"""

def elevation_color(elecol):
    """
    Function to create dynamic coloring for markers for volcanoes depending on the elevation
    :param elecol:
    :return:
    """
    if elecol <= 500:
        return "pink"
    elif 500 < elecol <=1000:
        return "blue"
    elif 1000 < elecol <= 1500:
        return "green"
    elif 1500 < elecol <= 2000:
        return "red"
    elif 2000 < elecol <= 2500:
        return "orange"
    elif 2500 < elecol <= 3000:
        return "lightgray"
    elif 3000 < elecol <= 4000:
        return "cadetblue"


# [contains the longitude and latitude of the map] extracted from the web
        
map = folium.Map(location=[38.58,-99.09],zoom_start=5,tiles="Mapbox Bright")

fgv = folium.FeatureGroup(name="US_Volcano_Map")        # Folium FeatureGroup() declaration.


for lt, ln, el, nm, loc, ty in zip(lat,lon,elev,nam,loca,typ):
    """
    6 var created for ranging over the list of lat,long,elevation,name,location,type: 
    using ZIP function used  traversing multiple lists
    """
    iframe = folium.IFrame(html=html % (nm,nm,loc,el,ty), width=250, height=150)
    fgv.add_child(folium.Marker(location=[lt,ln], popup=folium.Popup((iframe),parse_html=True),
                               icon=folium.Icon(color=elevation_color(el))))  # passing the iframe into popup parameter..

fgp = folium.FeatureGroup(name="World_Population_Color_Map")

# Folium Add_Child() and Folium.GeoJson() declared and initialized

fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
       style_function=lambda x: {'fillColor':'gray' if x['properties']['POP2005']<=10000000 else 'yellow'
       if 10000000 < x['properties']['POP2005'] <= 35000000 else "red"
       if 35000000 < x['properties']['POP2005'] <= 60000000 else "green"
                                 if 60000000 < x['properties']['POP2005'] <= 100000000 else 'orange'}))

# Below code is for displaying the name of the country and the population as of Year 2005

world_data = json.load(open('world.json', 'r', encoding='utf-8-sig'))

for country in world_data['features']:
    """
    For displaying the population on popup window of each country, user clicks on the respective countries circle marker
    """
    pop_up = '<br />'.join([escape('Name of the Country: '+country['properties']['NAME']), 'Population data recorded as on 2005:  ' + str(country['properties']['POP2005'])])
    fgp.add_child(folium.CircleMarker(location=[country['properties']['LAT'], country['properties']['LON']], radius = 6,popup=pop_up,  fill_color="white", color="gray", fill_opacity=0.6))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map_Advanced_final.html")

"""
Self Note: 
Important point to note FOLIUM prints a blank page incase there are any apostrophe elements such as < ` > in a POPUP statement as in line 68
Hence care must be taken to keep strings with out < ` >
"""