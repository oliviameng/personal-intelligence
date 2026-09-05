# CLAUDE.md — project context for Claude Code

This repo is a public portfolio artifact. Its job is to demonstrate applied-AI product judgment to a frontier-lab audience. It is not a production service and nobody is expected to run it against a live key. Optimize every decision for "a skeptical reviewer clicks through and gets it in three minutes," not for feature completeness.

## Hard constraints (do not violate)

- **No employer IP, ever.** Nothing about the owner's day job: no product names, internal codenames, stakeholder names, architecture, prompts, configs, or metrics from work. This repo covers personal domains only (tennis, personal knowledge capture).
- **The IP scan hook is mandatory.** `scripts/ip_scan.py` runs as a pre-commit hook (`docs/SETUP_HOOK.md`). Enable it before the first commit: `git config core.hooksPath .githooks`. Keep real names/codenames in `.ip_blocklist.local` (gitignored, never committed).
- **The real journal never enters the repo.** All sample data is fabricated. The owner's actual tennis/second-brain content stays out. `private/` is gitignored for anyone running it on their own life.
- **Personal work only.** Built on personal machine, personal time, personal accounts. Every README carries the no-affiliation line.

## What this system is

An LLM reads a personal session log ACROSS sessions, where a human reads within one. Tennis is the worked example: eleven weeks of practice notes went in, and the system surfaced that the serve problem was trust in a working motion, not mechanics — a pattern no single entry shows. That cross-session read is the entire point; everything else serves it.

Three personas each write one section of a "Staff Report": **coach** (technical), **psychologist** (mental), **tactics** (strategy). An earlier version had five; physio and nutritionist were cut because their data was too thin to earn a standing voice. Cutting a designed role is editorial judgment, and the repo says so.

## Design decisions already made (don't relitigate without reason)

- Three personas, not five. Settled.
- Rigid entry format is a feature: it is the price of cross-session comparison. A looser format would be easier to write and useless to read across.
- Portfolio, not production: static demo data baked in, no GitHub Actions, no secrets, no API key in the repo. The evals ship as evidence of thinking, with real results written up in `evals/RESULTS.md`.
- Dashboard is the owner's "Court Sense" HTML, to be rewired to read fabricated data from a JSON file. Athlete name stays "Olivia" (it's her system); every session, location, and metric is fabricated.

## State of the repo

Done:
- `prompts/` — three personas + `_shared_rules.md` (cross-session rule is the headline) + README with design rationale and boundaries.
- `evals/` — five adversarial cases (invented findings, lane bleed, within-session reading, clinician boundary, felt-vs-actual gap), a model-assisted runner, and a `RESULTS.md` scaffold.
- `scripts/ip_scan.py`, `.githooks/pre-commit`, `.gitignore`, top-level `README.md`.

To do:
1. Run the evals once (needs the owner's API key, local only), paste output into `RESULTS.md`.
2. `ingest/log_session.py` — dump-to-structured-entry, writes to Notion. Reference-quality, readable, not production-hardened.
3. `synthesis/run.py` — prepend `_shared_rules.md` to each persona, feed a block's entries, concatenate three sections into a Staff Report; write `synthesis/output/latest.json` for the dashboard.
4. `sample_data/` — one fabricated athlete: ~12 entries + 2 synthesis reports. Plausible, invented, scrubbed.
5. `dashboard/index.html` — the Court Sense file, rewired to load `latest.json`; label any biometrics as illustrative.
6. Final pass: enable the hook, run the scan, then first commit.

## House style for any prose in this repo

Declarative, no hedging. Authority comes from naming the problem, not from a title. No em-dashes as dramatic pauses, no "not X, it's Y" constructions, no corporate vocabulary (leverage, unlock, seamless, robust). Lead a claim with the outcome. Keep READMEs short.
