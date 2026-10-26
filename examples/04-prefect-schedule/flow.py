"""dlt 04-prefect-schedule: dlt pipeline wrapped in a Prefect flow.

Design-only pattern (gate 1 target). Same 10-row fixture as patterns
01-03, DuckDB destination. Prefect 3.9.0, dlt 1.31.0, Python 3.12.

Deployment rule from the fleet: local process-pool deploys need the
real EntrypointType.MODULE_PATH enum (see prefect-cookbook 03).
"""

import sys

import dlt
from prefect import flow, task
from prefect.types.entrypoint import EntrypointType

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


@task
def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="quakes_demo",
        destination="duckdb",
        dataset_name="quakes_demo",
    )
    pipeline.run(quakes())
    return "loaded 10 rows"


@flow(name="quakes-daily-flow")
def quakes_daily_flow():
    return run_pipeline()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        # Fleet cron 0 6 * * *; pool name is a placeholder — replace
        # with your pool (fleet: default on Node-1, n3-pool, n4-pool).
        quakes_daily_flow.deploy(
            name="quakes-daily",
            cron="0 6 * * *",
            work_pool_name="default-pool",
            entrypoint_type=EntrypointType.MODULE_PATH,
        )
        print("deployment quakes-daily registered")
    else:
        print(quakes_daily_flow())
