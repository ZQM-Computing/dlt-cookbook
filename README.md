# dlt Cookbook

<!-- ZQM-START -->
<!-- markdownlint-disable MD033 -->
<p align="center">
  <strong>ZQM Computing — Geospatial Engineering & Scientific Computing</strong><br>
  <a href="https://github.com/ZQM-Computing">ZQM Computing</a>
</p>
<!-- markdownlint-enable MD033 -->
<!-- ZQM-END -->

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A **dlt cookbook** for ELT pipelines from Python into Postgres and DuckDB. Patterns are drawn from the ZQM fleet's dlt 1.31.0 installs and its USGS demo pipelines (191 rows kept on Node-1 and Node-3). It is intended for Data engineers who load APIs and files into queryable tables with minimal boilerplate. Validate each pattern against your own data, software versions, and operating environment before adopting it.

## Repository role and status

**Status:** Active, public — first pattern pass written (design-only, gate 1 target; runtime validation pending). The table below lists what is written; no pattern has been runtime-validated yet.

**What this repository is:** dlt patterns — see the table below.

**What it contributes:** Part of the ZQM Computing geospatial portfolio. The umbrella index for the series is [geospatial-cookbooks](https://github.com/ZQM-Computing/geospatial-cookbooks).

**Standing:** This repository is maintained independently. Automated checks cover only the paths and environments configured in its workflows; they do not establish production readiness or operational certification.

## Who this is for

Data engineers who load APIs and files into queryable tables with minimal boilerplate.

## Prerequisites

- dlt 1.31.0
- Python 3.11+
- Postgres or DuckDB as a destination

## Patterns

| # | Example | Status | What it demonstrates |
|---|---------|--------|----------------------|
| 01 | [01-first-pipeline](examples/01-first-pipeline/README.md) | Written (design-only) | A first pipeline: source, resource, and destination |
| 02 | [02-postgres-dest](examples/02-postgres-dest/README.md) | Written (design-only) | Loading into Postgres with merge and replace semantics |
| 03 | [03-duckdb-dest](examples/03-duckdb-dest/README.md) | Written (design-only) | Loading into DuckDB for analytical queries |
| 04 | [04-prefect-schedule](examples/04-prefect-schedule/README.md) | Written (design-only) | Scheduling a dlt pipeline under Prefect (see prefect-cookbook) |

## Repository layout

```text
dlt-cookbook/
├── examples/01-first-pipeline/    # first pipeline into DuckDB
├── examples/02-postgres-dest/     # merge and replace semantics
├── examples/03-duckdb-dest/       # analytical queries
├── examples/04-prefect-schedule/  # Prefect flow + deployment
├── README.md
└── LICENSE
```

## Roadmap

- First pattern pass: complete (all 4 patterns, design-only).
- Next: gate-3 runtime validation against the fleet's dlt installs.

## Contributing

A contributing guide lands with the first pattern pass. Report security issues to <zqmcomputing@gmail.com> — please do not open a public issue for those.

## More from this series

- [prefect-cookbook](https://github.com/ZQM-Computing/prefect-cookbook) — Workflow orchestration, schedules, and deployments
- [duckdb-spatial-cookbook](https://github.com/ZQM-Computing/duckdb-spatial-cookbook) — Analytical geospatial SQL with DuckDB Spatial
- [postgis-cookbook](https://github.com/ZQM-Computing/postgis-cookbook) — Spatial indexing, joins & KNN, SRID management, vector tiles
