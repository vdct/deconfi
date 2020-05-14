#!/bin/bash

wget https://www.data.gouv.fr/fr/datasets/r/eb36371a-761d-44a8-93ec-3d728bec17ce
mv eb36371a-761d-44a8-93ec-3d728bec17ce depts_osm_2018.shp.zip
unzip depts_osm_2018.shp.zip 
shp2pgsql -s 4326 -d -g geometrie -I departements-20180101.shp depts_geo |psql -d <base> -U <user>
psql -d <base> -U <user> -f sql/contours_france.sql