#!./venv37/bin/python
# -*- coding: utf-8 -*-

import db

def get_zone(lat,lon,epsg):
    with db.bano_cache.cursor() as cur:
        cur.execute(f"""
                        WITH
                        zone_full
                        AS
                        (SELECT (ST_Union(geometrie)) geometrie
                        FROM
                        (SELECT geometrie FROM dept_geo WHERE ST_Contains(geometrie,ST_SetSRID(ST_MakePoint({lon},{lat}),4326))
                        UNION ALL
                        SELECT ST_Transform(ST_Buffer(ST_Transform(ST_SetSRID(ST_MakePoint({lon},{lat}),4326),{epsg}),100000),4326))a),
                        zone_stricte
                        AS
                        (SELECT ST_Intersection(zf.geometrie,fr.geometrie) geometrie
                        FROM zone_full AS zf
                        JOIN contour_france_geo AS fr
                        ON zf.geometrie && fr.geometrie)
                        SELECT ST_AsGeoJSON(ST_Union(geometrie),5)
                        FROM zone_stricte
                     """)

        return((cur.fetchone()[0]))

def get_common_part(geojson1,geojson2):
    with db.bano_cache.cursor() as cur:
        cur.execute(f"""
                        WITH
                        z1
                        AS
                        (SELECT ST_SetSRID(ST_MakeValid(ST_GeomFromGeoJSON('{geojson1}')),4326) AS geometrie),
                        z2
                        AS
                        (SELECT ST_SetSRID(ST_MakeValid(ST_GeomFromGeoJSON('{geojson2}')),4326) AS geometrie)
                        SELECT ST_AsGeoJSON(ST_Intersection(z1.geometrie,z2.geometrie),5)
                        FROM z1,z2
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

def get_longest_line(lat,lon,epsg,geojson):
    with db.bano_cache.cursor() as cur:
        cur.execute(f"""
                        WITH
                        zone
                        AS
                        (SELECT ST_Transform(ST_SetSRID(ST_GeomFromGeoJSON('{geojson}'),4326),{epsg}) AS geom_zone),
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
                        ST_X(ST_LineInterpolatePoint(geometrie,0.999)),
                        ST_Y(ST_LineInterpolatePoint(geometrie,0.999))
                        FROM ll
                     """)
        return((cur.fetchone()))

def get_epsgcode_by_dept(dept):
    epsg = 2154
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
    return epsg
