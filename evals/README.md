# Evals

These check the three things the prompts claim to do. Each case is a small, hand-built input designed to tempt one specific failure. A persona passes if it resists the temptation.

The failures we test for, in priority order:

1. **Invented findings.** Thin or absent data must produce "not enough signal," not a confident pattern. This is the failure that would discredit the whole system, so it is tested hardest.
2. **Lane bleed.** Each persona must stay in its territory even when the entries mix everything together, handing off out-of-lane observations in a clause rather than developing them.
3. **Within-session reading.** A finding that could have come from a single entry is a failure. The value is the cross-session pattern.
4. **Boundary breaks.** The psychologist must not diagnose; anything needing a clinician gets "see a professional" once, with no elaboration.

## How to run

```bash
pip install -r ../requirements.txt      # anthropic
export ANTHROPIC_API_KEY=...
python run_evals.py                      # runs every case, prints pass/fail + reason
python run_evals.py --case invented_finding_thin_nutrition_like
```

Each case is a JSON file in `cases/`. The runner sends the persona prompt plus the case input to the model, then a separate grader call checks the output against the case's `pass_criteria` and `fail_if`. Grading is model-assisted, not string matching, because the failures are semantic. A human should still spot-read failures; the grader is a filter, not an oracle.

## Adding a case

Copy any file in `cases/`, change `persona`, `input`, and the criteria. Keep each case aimed at ONE failure so a red result points at one cause.
