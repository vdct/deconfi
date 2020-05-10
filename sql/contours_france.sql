DROP TABLE IF EXISTS contours_france_geo CASCADE;
CREATE TABLE contours_france_geo
AS
SELECT ST_SetSRID(ST_Subdivide(ST_SimplifyPreserveTopology(ST_Union(geometrie),0.001),60000),4326) geometrie
FROM depts_geo;
CREATE INDEX gidx_contours_france_geo ON contours_france_geo USING GIST(geometrie);