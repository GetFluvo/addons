# Provenance & status

This module was **salvaged from the archived `bosd/odoo-data-flow` repo**
(unmerged PR #11, issue #10) before that repo is deleted, so the work is not lost.

- It was **generated with Jules** and is a **prototype** — treat it as a starting
  point, not finished code. Expect rework.
- Roadmap home: this is the "cleaning-DB orchestrator" — PLAN item **5.7**, tracked
  as [`GetFluvo/addons#1`](https://github.com/GetFluvo/addons/issues/1). It is
  **Core** (it moves/cleans data), so it lives here in the public addons repo.
- Not for production Odoo — it targets a disposable staging/cleaning database.

Rework before real use: manifest metadata (author/website still point at the old
repo), security review, tests, and alignment with the addons-repo conventions
(pre-commit, ruff, pylint).
