CREATE TEMP TABLE 
poly_dump
AS
SELECT (ST_Dump(geometrie)).geom geometrie,code_insee
FROM depts_geo;

DROP TABLE IF EXISTS dept_geo CASCADE;
CREATE TABLE dept_geo
AS
SELECT ST_Union(geometrie) AS geometrie,
       code_insee
FROM poly_dump
WHERE ST_Area(ST_Transform(geometrie,3857)) > 8000 and ST_NPoints(geometrie) > 5
GROUP BY code_insee;

CREATE INDEX gidx_dept_geo
ON dept_geo USING GIST(geometrie);

DROP TABLE IF EXISTS contour_france_geo CASCADE;
CREATE TABLE contour_france_geo
AS
SELECT ST_SetSRID(ST_Subdivide(ST_SimplifyPreserveTopology(ST_Union(geometrie),0.001),6000),4326) geometrie
FROM dept_geo;

CREATE INDEX gidx_contour_france_geo
ON contour_france_geo USING GIST(geometrie);