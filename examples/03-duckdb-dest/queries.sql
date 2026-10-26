-- dlt 03-duckdb-dest: analytical queries over the 10-row fixture.
-- Expected: count 10, avg magnitude 3.07, bounding-box rows 5, max 5.2.

-- Query 1: row count.
SELECT COUNT(*) AS row_count FROM quakes_demo.quakes;

-- Query 2: average magnitude.
SELECT AVG(magnitude) AS avg_magnitude FROM quakes_demo.quakes;

-- Query 3: bounding box, both bounds inclusive.
-- Expected ids: q01, q02, q06, q07, q09.
SELECT id, place, magnitude, longitude, latitude
FROM quakes_demo.quakes
WHERE longitude BETWEEN -122.5 AND -122.0
  AND latitude BETWEEN 37.4 AND 37.9
ORDER BY id;

-- Query 4: maximum magnitude.
SELECT id, place, magnitude FROM quakes_demo.quakes
ORDER BY magnitude DESC LIMIT 1;
