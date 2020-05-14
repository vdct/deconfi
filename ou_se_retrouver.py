#!./venv37/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json

# import db

from requetes import get_zone,get_commune,get_longest_line,get_epsgcode_by_dept,get_common_part

cgitb.enable()

params = cgi.FieldStorage()
lon1 = params['x1'].value
lat1 = params['y1'].value
lon2 = params['x2'].value
lat2 = params['y2'].value

# lon1 = -4.614257812500001
# lat1 = 48.459645973442484
# lon2 = -2.8784179687500004
# lat2 = 48.08524371619902

epsg1 = None
epsg2 = None
geojson1 = None
geojson2 = None

commune_dept1 = get_commune(lat1,lon1)
if commune_dept1:
    epsg1 = get_epsgcode_by_dept(commune_dept1[1])

commune_dept2 = get_commune(lat2,lon2)
if commune_dept2:
    epsg2 = get_epsgcode_by_dept(commune_dept2[1])

if (epsg1) and (epsg1 == epsg2):
    geojson1 = get_zone(lat1,lon1,epsg1)
    # with open('debug1.geojson','w') as g:
    #     g.write(geojson1)
    geojson2 = get_zone(lat2,lon2,epsg2)
    # with open('debug2.geojson','w') as g:
    #     g.write(geojson2)
    geojson_intersect = get_common_part(geojson1,geojson2)

print ("Content-Type: application/json")
print ("")

print(f"[{geojson1},{geojson2},{geojson_intersect}]")
