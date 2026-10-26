# 02 — Postgres Destination: Merge and Replace Semantics

**Evidence level: design-only, gate 1 target.** This pattern has not been
runtime-validated on the fleet. It is written from the dlt 1.31.0
documentation and the fleet's dlt installs (see Versions). Do not describe
it as fleet-verified until a gate-3 run exists.

## What it demonstrates

Loading into Postgres with the two write dispositions that matter:
`merge` (upsert by primary key) and `replace` (drop and reload).
The same 10-row synthetic fixture as pattern 01 is used, so row counts
are comparable across patterns.

## Files

- `postgres_pipeline.py` — pre-flight connection check, a merge load
  run twice, and a replace load run twice, with counts printed after
  each run.

## Run

```bash
pip install "dlt[postgres]==1.31.0"
export DLT_DESTINATION__POSTGRES__CREDENTIALS__HOST=localhost
export DLT_DESTINATION__POSTGRES__CREDENTIALS__PORT=5432
export DLT_DESTINATION__POSTGRES__CREDENTIALS__USERNAME=your_user
export DLT_DESTINATION__POSTGRES__CREDENTIALS__PASSWORD=your_password
export DLT_DESTINATION__POSTGRES__CREDENTIALS__DATABASE=your_db
python postgres_pipeline.py
```

All credential values are placeholders. Never put a real password in
the script, a `.dlt` secrets file committed to a repo, or the README.
The fleet's Node-1 demo ran under trust auth with an explicitly-present
empty password — that setup is NOT copied here; use real credentials
from your own environment.

## Auth gate (read before running)

This pattern requires **working Postgres auth**. Node-4's Postgres auth
is blocked (scram-sha-256, passwords file unusable from SSH) — do not
run this pattern against Node-4 until that unblocker lands. The script's
pre-flight check fails fast with a clear message instead of letting dlt
die mid-load.

## Synthetic inputs

The same 10 synthetic quake rows as pattern 01. The second merge run
changes the magnitudes of `q01` (1.2 → 1.5) and `q06` (5.2 → 5.0) and
re-sends all 10 rows.

## Expected output

- After merge run 1: `quakes_merge` holds **10 rows**.
- After merge run 2: still **10 rows** (no duplicates), `q01` magnitude
  **1.5**, `q06` magnitude **5.0** — the merge updated in place.
- After replace run 1: `quakes_replace` holds **10 rows**.
- After replace run 2: still **10 rows** — the table was dropped and
  reloaded, not appended to 20.
- New average after the merge update: (30.7 + 0.3 − 0.2) / 10 = **3.08**.

## Versions

- dlt **1.31.0** (fleet-verified on Node-1, Node-3, Node-4).
- Python 3.12; Postgres 17 (fleet Postgres) via the `dlt[postgres]`
  extra.
- To confirm at validation: the exact merge staging behavior dlt 1.31.0
  applies (staging table vs in-place update), and the exact
  `DLT_DESTINATION__POSTGRES__CREDENTIALS__*` variable names dlt
  1.31.0 reads.

## Failure behavior

- Pre-flight connection failure: the script exits before any load with
  the connection error printed. Fix host/port/credentials/pg_hba on
  your own instance — this pattern never edits pg_hba.
- Merge without a primary key: dlt refuses the merge disposition.
  Declare `primary_key="id"` (as the script does); do not merge on
  unkeyed rows.
- Replace on a table other jobs read: readers see an empty table
  between drop and reload. Never point `replace` at a table serving
  live traffic; use `merge` for those.

## To confirm at validation

- Exact console output for merge run 2 (updated-row reporting).
- Whether dlt 1.31.0's Postgres destination needs `search_path` or
  dataset-schema handling for the `quakes_demo` dataset name.
