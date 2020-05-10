#!./venv37/bin/python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json

import db

def get_zone(lat,lon,epsg):
    with db.bano_cache.cursor() as cur:
        cur.execute(f"""
                        SELECT ST_AsGeoJSON(ST_Union(geometrie))
                        FROM
                        (SELECT geometrie FROM depts_geo WHERE ST_Contains(geometrie,ST_SetSRID(ST_MakePoint({lon},{lat}),4326))
                        UNION ALL
                        SELECT ST_Transform(ST_Buffer(ST_Transform(ST_SetSRID(ST_MakePoint({lon},{lat}),4326),{epsg}),100000),4326)) a
                     """)
        return((cur.fetchone()[0]))

def get_commune(lat,lon):
    with db.bano_cache.cursor() as cur:
        cur.execute(f"""
                        SELECT p.nom,c.dep
                        FROM polygones_insee p
                        JOIN cog_commune c
                        ON p.insee_com = c.com
                        WHERE ST_Intersects(p.geometrie,ST_Transform(ST_SetSRID(ST_MakePoint({lon},{lat}),4326),3857)) AND
                              c.typecom != 'COMD'
                     """)
        return((cur.fetchone()))

def get_longest_line(lat,lon,epsg):
    with db.bano_cache.cursor() as cur:
        cur.execute(f"""
                        WITH
                        zone
                        AS
                        (SELECT ST_Transform(geometrie,{epsg}) as geom_zone FROM depts_geo WHERE ST_Contains(geometrie,ST_SetSRID(ST_MakePoint({lon},{lat}),4326))
                        UNION ALL
                        SELECT ST_Buffer(ST_Transform(ST_SetSRID(ST_MakePoint({lon},{lat}),4326),{epsg}),100000)),
                        centre
                        AS
                        (SELECT ST_Transform(ST_SetSRID(ST_MakePoint({lon},{lat}),4326),{epsg}) as geom_centre),
                        ll_all
                        AS
                        (SELECT ST_LongestLine(geom_centre,geom_zone) geom_ll
                        FROM centre,zone),
                        ll
                        AS
                        (SELECT ST_Transform(geom_ll,4326) AS geometrie,
                        ST_Length(geom_ll) AS longueur
                        FROM ll_all
                        ORDER BY 2 DESC
                        LIMIT 1)
                        SELECT ST_AsGeoJSON(geometrie),
                        longueur,
                        ST_X(ST_EndPoint(geometrie)),
                        ST_Y(ST_EndPoint(geometrie))
                        FROM ll
                     """)
        return((cur.fetchone()))

cgitb.enable()

params = cgi.FieldStorage()
lat = params['lat'].value
lon = params['lon'].value
# lat = 48
# lon = 2

epsg = 2154
commune, dept = get_commune(lat,lon)
if len(dept) !=2:
    epsg = 3857

geom_ll,longueur,lon_dest,lat_dest = get_longest_line(lat,lon,epsg)

print ("Content-Type: application/json")
print ("")

print(f"[{get_zone(lat,lon,epsg)},{json.JSONEncoder().encode(get_commune(lat,lon))},{geom_ll},{longueur},{lon_dest},{lat_dest},{json.JSONEncoder().encode(get_commune(lat_dest,lon_dest))}]")
# print(f"{get_zone(lat,lon)}")
