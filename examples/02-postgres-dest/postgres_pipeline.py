"""dlt 02-postgres-dest: merge and replace semantics against Postgres.

Design-only pattern (gate 1 target). Credentials come ONLY from the
DLT_DESTINATION__POSTGRES__CREDENTIALS__* environment variables
(placeholders in the README). Requires working Postgres auth; the
pre-flight check fails fast if auth is unavailable (e.g. Node-4's
auth block). dlt 1.31.0, Python 3.12.
"""

import os
import sys

import dlt

BASE_QUAKES = [
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


def preflight():
    """Fail fast when Postgres auth is unavailable. No load is attempted."""
    import psycopg

    try:
        with psycopg.connect(
            host=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__HOST"],
            port=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__PORT"],
            user=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__USERNAME"],
            password=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__PASSWORD"],
            dbname=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__DATABASE"],
            connect_timeout=10,
        ):
            pass
    except Exception as exc:  # noqa: BLE001 - pre-flight reports, then exits
        print(f"PREFLIGHT FAILED: {exc}")
        print("Fix host/port/credentials/pg_hba on your own instance.")
        sys.exit(2)
    print("PREFLIGHT OK")


def count_rows(table):
    import psycopg

    with psycopg.connect(
        host=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__HOST"],
        port=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__PORT"],
        user=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__USERNAME"],
        password=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__PASSWORD"],
        dbname=os.environ["DLT_DESTINATION__POSTGRES__CREDENTIALS__DATABASE"],
    ) as con, con.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM quakes_demo.{table}")
        return cur.fetchone()[0]


def main():
    preflight()
    pipeline = dlt.pipeline(
        pipeline_name="quakes_pg_demo",
        destination="postgres",
        dataset_name="quakes_demo",
    )

    @dlt.resource(name="quakes_merge", write_disposition="merge",
                  primary_key="id")
    def quakes_merge(rows):
        yield from rows

    pipeline.run(quakes_merge(BASE_QUAKES))
    print(f"merge run 1 rows={count_rows('quakes_merge')}")
    updated = [dict(r, magnitude=1.5) if r["id"] == "q01" else r
               for r in BASE_QUAKES]
    updated = [dict(r, magnitude=5.0) if r["id"] == "q06" else r
               for r in updated]
    pipeline.run(quakes_merge(updated))
    print(f"merge run 2 rows={count_rows('quakes_merge')} (expect 10, updated)")

    @dlt.resource(name="quakes_replace", write_disposition="replace")
    def quakes_replace(rows):
        yield from rows

    pipeline.run(quakes_replace(BASE_QUAKES))
    print(f"replace run 1 rows={count_rows('quakes_replace')}")
    pipeline.run(quakes_replace(BASE_QUAKES))
    print(f"replace run 2 rows={count_rows('quakes_replace')} (expect 10)")


if __name__ == "__main__":
    main()
