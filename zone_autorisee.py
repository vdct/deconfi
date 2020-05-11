#!./venv37/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json

# import db

from requetes import get_zone,get_commune,get_longest_line

cgitb.enable()

params = cgi.FieldStorage()
lat = params['lat'].value
lon = params['lon'].value
# lat = 47.85919
# lon = -3.52112

epsg = 2154
commune_dept = get_commune(lat,lon)
if commune_dept:
    dept = commune_dept[1]
    if len(dept) !=2:
        epsg = 3857
    if dept == '971':
        epsg = 4559
    if dept == '972':
        epsg = 4559
    if dept == '973':
        epsg = 2972
    if dept == '974':
        epsg = 2975
    if dept == '976':
        epsg = 4471

geojson = get_zone(lat,lon,epsg)
geom_ll,longueur,lon_dest,lat_dest = get_longest_line(lat,lon,epsg,geojson)

print ("Content-Type: application/json")
print ("")

print(f"[{geojson},{json.JSONEncoder().encode(get_commune(lat,lon))},{geom_ll},{longueur},{lon_dest},{lat_dest},{json.JSONEncoder().encode(get_commune(lat_dest,lon_dest))}]")
