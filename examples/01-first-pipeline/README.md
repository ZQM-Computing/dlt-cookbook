# 01 — First Pipeline: Source, Resource, and Destination

**Evidence level: design-only, gate 1 target.** This pattern has not been
runtime-validated on the fleet. It is written from the dlt 1.31.0
documentation and the fleet's dlt installs (see Versions). Do not describe
it as fleet-verified until a gate-3 run exists.

## What it demonstrates

A first dlt pipeline: one `@dlt.resource` yielding synthetic earthquake
rows, loaded into a local DuckDB file. Source, resource, and destination
are the only three concepts a first pipeline needs.

## Files

- `pipeline.py` — the pipeline: resource definition, pipeline creation,
  load, and a verification query.

## Run

```bash
pip install "dlt[duckdb]==1.31.0"
python pipeline.py
```

The pipeline writes `quakes.duckdb` in the working directory. Delete the
file to re-run from scratch; the resource uses `write_disposition="replace"`,
so re-runs reload rather than append.

## Synthetic inputs

Ten synthetic earthquake rows, fixed in `pipeline.py` (ids `q01`–`q10`,
magnitudes 1.2–5.2, synthetic place names, fixed lon/lat pairs). No real
feed data, no credentials, no network access. The fleet's real shape
evidence is the USGS demo pipeline (191 rows kept on Node-1 and Node-3,
184 rows on Node-4 via the DuckDB fallback) — this example's 10 rows are
its own fixture and say nothing about those counts.

## Expected output

- `quakes_demo` dataset in `quakes.duckdb`, table `quakes`, **10 rows**.
- Average magnitude **3.07** (sum 30.7 over 10 rows).
- Maximum magnitude **5.2**, minimum **1.2**.
- The script prints the count and average itself; if either differs,
  the fixture or the destination changed — do not hand-edit the output
  to match.

## Versions

- dlt **1.31.0** (fleet-verified on Node-1, Node-3, Node-4).
- Python 3.12 (fleet Python); DuckDB 2.0.0 via the `dlt[duckdb]` extra.
- To confirm at validation: the exact `dlt[duckdb]` dependency set for
  1.31.0, and the on-disk dataset/table naming dlt applies
  (`quakes_demo.quakes` assumed here).

## Failure behavior

- Empty resource (no rows yielded): the load succeeds with 0 rows and
  the verification query prints 0 — a data problem, not a crash. Check
  the generator before re-running.
- Missing `dlt[duckdb]` extra: the pipeline constructor fails with an
  unknown-destination error. Install the extra; do not swap in another
  destination silently.
- A second resource with a different schema for the same table name:
  dlt raises a schema-evolution error. Rename the resource or the
  dataset; do not force-merge schemas in a first pipeline.

## To confirm at validation

- Exact console output of `pipeline.run` for dlt 1.31.0.
- Whether `pipeline.py`'s verification query needs the `duckdb` module
  import or can use dlt's SQL client instead.
