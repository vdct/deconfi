#!./venv37/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json

# import db

from requetes import get_commune

cgitb.enable()

params = cgi.FieldStorage()
lat = params['lat'].value
lon = params['lon'].value

# commune_dept = get_commune(lat,lon)

print ("Content-Type: application/json")
print ("")

print(f"{json.JSONEncoder().encode(get_commune(lat,lon))}")
