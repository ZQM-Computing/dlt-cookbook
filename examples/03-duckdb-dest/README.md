# 03 — DuckDB Destination: Analytical Queries

**Evidence level: design-only, gate 1 target.** This pattern has not been
runtime-validated on the fleet. It is written from the dlt 1.31.0
documentation and the fleet's dlt installs (see Versions). Do not describe
it as fleet-verified until a gate-3 run exists.

## What it demonstrates

Loading into DuckDB and answering analytical questions with plain SQL:
counts, averages, and a bounding-box filter. DuckDB is the destination
that needs no server and no credentials, which is why the fleet's
Node-4 dlt flow fell back to it (184 rows) when Postgres auth blocked.

## Files

- `duckdb_pipeline.py` — loads the same 10-row synthetic fixture as
  patterns 01–02 into `quakes.duckdb`.
- `queries.sql` — the three analytical queries, one per question.

## Run

```bash
pip install "dlt[duckdb]==1.31.0"
python duckdb_pipeline.py
duckdb quakes.duckdb < queries.sql
```

(If the `duckdb` CLI is absent, run the queries through Python's
`duckdb` module instead; the SQL is identical.)

## Synthetic inputs

The same 10 synthetic quake rows as patterns 01–02 (ids `q01`–`q10`).
No network, no credentials.

## Expected output

- Query 1 (count): **10**.
- Query 2 (average magnitude): **3.07**.
- Query 3 (bounding box: longitude −122.5 to −122.0, latitude 37.4 to
  37.9, both bounds inclusive): **5 rows** — `q01`, `q02`, `q06`, `q07`,
  `q09`. Boundary rows count: `q06` sits exactly on latitude 37.9,
  `q07` exactly on longitude −122.0, `q09` exactly on longitude −122.5.
- Query 4 (maximum magnitude): **5.2** (`q06`, Synthetic Peak).

## Versions

- dlt **1.31.0** (fleet-verified on Node-1, Node-3, Node-4).
- Python 3.12; DuckDB 2.0.0 via the `dlt[duckdb]` extra.
- To confirm at validation: the DuckDB file path dlt 1.31.0 uses by
  default (`quakes.duckdb` in the working directory assumed here) and
  the dataset/table naming (`quakes_demo.quakes`).

## Failure behavior

- Query against a missing table: DuckDB reports a catalog error naming
  the table. Re-run the pipeline first; do not create the table by
  hand to satisfy the query.
- Empty box result: the query returns 0 rows, not an error. Widen the
  box or check the fixture coordinates before assuming a load failure.
- Stale file from an earlier run: the loader uses
  `write_disposition="replace"`, so re-runs reload 10 rows rather than
  appending to 20. If the count is 20, the file came from a different
  loader — delete it and re-run this pattern alone.

## To confirm at validation

- Exact DuckDB CLI output formatting for the four queries.
- Whether dlt 1.31.0's DuckDB destination stores the dataset as a
  schema named `quakes_demo` (assumed) or flattens it.
