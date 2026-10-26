"""dlt 03-duckdb-dest: load the 10-row fixture, then query it.

Design-only pattern (gate 1 target). Same fixture as patterns 01-02.
dlt 1.31.0, Python 3.12, DuckDB via the dlt[duckdb] extra.
"""

import dlt

QUAKES = [
    {"id": "q01", "place": "Synthetic Bay", "magnitude": 1.2,
     "time": "2026-01-01T00:00:00Z", "longitude": -122.4, "latitude": 37.8},
    {"id": "q02", "place": "Synthetic Ridge", "magnitude": 2.4,
     "time": "2026-01-02T00:00:00Z", "longitude": -122.1, "latitude": 37.5},
    {"id": "q03", "place": "Synthetic Valley", "magnitude": 3.1,
     "time": "2026-01-03T00:00:00Z", "longitude": -121.9, "latitude": 37.2},
    {"id": "q04", "place": "Synthetic Coast", "magnitude": 4.0,
     "time": "2026-01-04T00:00:00Z", "longitude": -122.6, "latitude": 38.0},
    {"id": "q05", "place": "Synthetic Plain", "magnitude": 2.8,
     "time": "2026-01-05T00:00:00Z", "longitude": -121.5, "latitude": 36.9},
    {"id": "q06", "place": "Synthetic Peak", "magnitude": 5.2,
     "time": "2026-01-06T00:00:00Z", "longitude": -122.3, "latitude": 37.9},
    {"id": "q07", "place": "Synthetic Basin", "magnitude": 1.8,
     "time": "2026-01-07T00:00:00Z", "longitude": -122.0, "latitude": 37.4},
    {"id": "q08", "place": "Synthetic Fault", "magnitude": 3.6,
     "time": "2026-01-08T00:00:00Z", "longitude": -121.8, "latitude": 37.6},
    {"id": "q09", "place": "Synthetic Hills", "magnitude": 2.2,
     "time": "2026-01-09T00:00:00Z", "longitude": -122.5, "latitude": 37.7},
    {"id": "q10", "place": "Synthetic Shore", "magnitude": 4.4,
     "time": "2026-01-10T00:00:00Z", "longitude": -121.7, "latitude": 37.1},
]


@dlt.resource(name="quakes", write_disposition="replace")
def quakes():
    yield from QUAKES


def main():
    pipeline = dlt.pipeline(
        pipeline_name="quakes_demo",
        destination="duckdb",
        dataset_name="quakes_demo",
    )
    pipeline.run(quakes())
    print("loaded quakes_demo.quakes; run queries.sql for the analysis")


if __name__ == "__main__":
    main()
