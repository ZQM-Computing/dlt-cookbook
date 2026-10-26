# 04 — Prefect Schedule: Running a dlt Pipeline on a Cron

**Evidence level: design-only, gate 1 target.** This pattern has not been
runtime-validated on the fleet. It is written from the Prefect 3.9.0 and
dlt 1.31.0 documentation and the fleet's Prefect-scheduled dlt flows
(see Versions). Do not describe it as fleet-verified until a gate-3 run
exists. See also [prefect-cookbook](https://github.com/ZQM-Computing/prefect-cookbook).

## What it demonstrates

Wrapping a dlt pipeline in a Prefect flow and deploying it on a daily
cron, the way the fleet runs its USGS quake flows: a flow task runs the
pipeline, a deployment schedules it, a worker executes it.

## Files

- `flow.py` — Prefect flow with one task that runs the 10-row synthetic
  fixture into DuckDB, plus the deployment definition.
- `prefect.yaml` — deployment sketch (labeled as a sketch, not a
  verbatim Prefect 3.9.0 file; see the Prefect 03 note in
  prefect-cookbook).

## Run

```bash
pip install "dlt[duckdb]==1.31.0" "prefect==3.9.0"
python flow.py            # direct run: flow completes, 10 rows loaded
python flow.py deploy     # registers the daily deployment (see below)
```

The direct run needs only Prefect's local execution; the deployment
step needs a running Prefect server and a work pool (see Failure
behavior). The flow writes `quakes.duckdb` in the working directory.

## Synthetic inputs

The same 10 synthetic quake rows as patterns 01–03. The fleet's real
shape evidence is its USGS flows — Node-1 deployment
`usgs-quakes-daily` → 184 rows, Node-3 → 59 rows, Node-4 → 50 rows
(DuckDB) — all on cron `0 6 * * *`. This example's 10 rows are its own
fixture and say nothing about those counts.

## Expected output

- Direct run: flow state **Completed**, `quakes_demo.quakes` holds
  **10 rows** in `quakes.duckdb`.
- Deployment: a deployment named `quakes-daily` on cron `0 6 * * *`
  (the fleet cron), work pool placeholder `default-pool` (replace with
  your pool: the fleet uses `default` on Node-1, `n3-pool` on Node-3,
  `n4-pool` on Node-4).
- A worker pick-up run completes the same way as the direct run.

## Versions

- Prefect **3.9.0** (fleet-verified on Node-1 on :4300, Node-3 on :4200;
  note Node-1's port: 4200 sits in Windows' excluded range 4141–4240
  and cannot bind there).
- dlt **1.31.0**, Python 3.12, DuckDB 2.0.0.
- Deployment rule from the fleet (see prefect-cookbook 03): local
  process-pool deploys need the real `EntrypointType.MODULE_PATH`
  enum — the string form and `push=False` both still fail Prefect's
  image/storage check. That rule is honored in `flow.py`.
- To confirm at validation: the verbatim `prefect.yaml` schema for
  3.9.0 (the file here is a sketch), and the exact `flow.deploy`
  vs `serve` spelling for this shape.

## Failure behavior

- No Prefect server reachable: the direct run still completes (local
  execution); only the deployment step fails, with a connection error.
  Start the server first; do not fake a deployment.
- No worker for the pool: the deployment shows as active but runs
  stay Scheduled/Late. Start a worker for that pool; a deployment
  without a worker is a configuration error, not a schedule error.
- dlt load failure inside the task: the task (and flow) fail with the
  dlt error, and the run is retried only if retries are configured
  (this flow sets none — add `retries=2` deliberately, not by accident).

## To confirm at validation

- Exact deployment-creation output for Prefect 3.9.0.
- Whether the flow's DuckDB file lands in the worker's working
  directory or the flow's (the fleet's Node-1 worker runs as
  LocalSystem, so dlt state sits under the system profile — the same
  trap applies to any file the flow writes).
